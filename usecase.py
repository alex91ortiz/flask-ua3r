
import re
from datetime import date
from werkzeug.utils import secure_filename
from bucket import get_byte_objfile, list_files
from process import match_image_invoice
from response import result

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generatePaymentDetail(files):
    dateProcess = date.today().strftime("%d%m%Y %H%m")
    data = []
    for f in files:
        if f and allowed_file(f.filename):
            nameFile = secure_filename(f.filename)
            fileContent = f.read()
            caps = list_files()
            for cap in caps:
                fileBytes, nameCap = get_byte_objfile(cap)
                total = match_image_invoice(fileContent, fileBytes)
                if total != None:
                    total = re.sub('[^0-9\.0-9\,]', '', total)
                    total = total.replace(".", "").replace(",", ".")
                    content = {"image": nameFile,
                            "entity": nameCap,
                            "date": dateProcess,
                            "value": total}
                    data.append(content)

    return result(data)