
import logging
import re
from datetime import date
from werkzeug.utils import secure_filename
from bucket import get_byte_objfile, list_files
from process import match_image_invoice
from response import result
import json
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generatePaymentDetail(files):
    dateProcess = date.today().strftime("%Y%m%d")
    data = []
    for f in files:
        if f and allowed_file(f.filename):
            nameFile = secure_filename(f.filename)
            fileContent = f.read()
            caps = list_files()
            for cap in caps:
                fileBytes, nameCap = get_byte_objfile(cap)
                listData = match_image_invoice(fileContent, fileBytes)
                if len(listData) > 0:
                    value = prepareDataStructure(listData)
                    if len(value) > 0:
                        logging.info(value)
                        content = {
                            "image": nameFile,
                            "entity": nameCap,
                            "date": dateProcess,
                            "value": value
                        }
                        data.append(content)
    return result(data)

def prepareDataStructure(listData, id = "DEFAULT"):
    f = open("parameters.json")
    parameters = json.load(f)
    x = 0
    list_field = []
    for data in listData:
        p = list(
                map(
                    lambda value: value["index"] == x, parameters[id]["positions"]
                )
            ).index(True)

        field  = parameters[id]["positions"][p]
        if data is not None:
            if field["type"] == "NUMBER":
                data = re.sub('[^0-9\.0-9\,]', '', data)
                data = data.replace(",", "")
                data = data.replace(".", "")
                if data != "":
                    field["value"] = float(data)/100
            else:
                field["value"] = data.strip()
            list_field.append(field)
        x = x + 1
    return list_field