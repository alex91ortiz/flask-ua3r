

def result(data):
    sorted_dict = sorted(data, key=lambda d: d['entity'])
    entity_map = list(map(refactorEntity, sorted_dict))
    summary_map = calculateTotal(entity_map)
    return {
        "list_items": entity_map,
        "list_summary": summary_map
    }


def refactorEntity(x):
    nameFile = x["entity"].split(".")[0]
    entity = nameFile.split("_")
    x["entity"] = nameFile
    if entity != None:
        x["entity"] = entity[0]
    return x


def calculateTotal(data):
    g = {}
    entity = ""
    for x in data:
        if entity != x["entity"]:
            entity = x["entity"]
            g[x["entity"]] = 0
        i = list(
                map(
                    lambda value: value["type"] == "NUMBER", x["value"]
                )
        ).index(True)
        g[x["entity"]] += x["value"][i]["value"] if x["value"][i]["value"] != "" else 0.0
    return list(map(lambda x: {"entity": x, "value": g[x] },g.keys()))
