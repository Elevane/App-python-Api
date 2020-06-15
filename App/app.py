import shutil

from flask import Flask, escape, request, jsonify
import csv
from tempfile import NamedTemporaryFile

app = Flask(__name__)

RESSOURCEFIELDSNAME = ["id", "name", "quantity", "unity", "user"]
RESSOURCEFIELDSNAMEPOST = ["name", "quantity", "unity", "user"]

OBJECTCSV = "ressource.csv"
TEMPCSV = "temp.csv"


@app.route("/clean/<name>")
def cleanCsv(mycsv):
    mycsv = mycsv + ".csv"
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open(mycsv, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(tempfile)
        for row in reader:
            row = {}
            writer.writerow(row)
    shutil.move(tempfile.name, mycsv)
    return True


def checkifExistObjet(mycsv, object, fields):
    with open(mycsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        for row in reader:
            if row['id'] == object['id']:
                return True
        return False


def addObject(mycsv, object, fields):

    with open(mycsv, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow({"id": object['id'],
                         "name": object['name'],
                         "quantity": object['quantity'],
                         "unity": object['unity'],
                         "user": object['user'],
                         })


def getAll(mycsv, fdlsN):
    o = []
    with open(mycsv, newline='') as csvfile:
        fieldnames = fdlsN
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            o.append(row)
        return o


def updateObject(mycsv, object, fieldsnames):
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fields = fieldsnames

    with open(mycsv, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['id'] == str(object['id']):
                for f in fieldsnames:
                    row[f] = object[f]
                o = row
                i = 0
                for r in o:
                    print(o)
                    row[fieldsnames[i]] =  o[fieldsnames[i]]
                    i = i + 1
            """row = {"id": row['id'],
                         "name": row['name'],
                         "quantity": row['quantity'],
                         "unity": row['unity'],
                         "user": row['user'],
                         }"""
            writer.writerow(row)
    shutil.move(tempfile.name, mycsv)
    return True


def getMax(mycsv):
    with open(mycsv, newline='') as csvfile:
        row_count = sum(1 for row in csvfile)
        return row_count


def getAny(mycsv, objet, fields):
    with open(mycsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        for row in reader:
            if row["id"] == objet['id']:
                response = row
                return response
        return False


"""
post method for objects
:parameter =  request with onject in json
"""


@app.route('/ressource', methods=['POST'])
def postResource():
    if request.is_json:
        content = request.get_json()
        if len(content) > 4:
            return jsonify("invalid Json, too much parameters")
        else:
            if 'name' and "quantity" and "unity" and "user" in content:
                max = getMax(OBJECTCSV) + 1
                content['id'] = max
                addObject(OBJECTCSV, content, RESSOURCEFIELDSNAME)
                return jsonify(content)
            else:
                missing = []
                keys = list(content.keys())
                for re in RESSOURCEFIELDSNAMEPOST:
                    if re not in keys:
                        missing.append(re)
                return jsonify("invalid Json, parameter key invalid, missing: ", missing)
                # return le missing parameters

    else:
        return jsonify("Invalid Json given")


"""
return all objects
"""


@app.route('/ressourceAll', methods=['GET'])
def getAllRessource():
    return jsonify(getAll('ressource.csv', RESSOURCEFIELDSNAME))


"""
get method for ressources
:parameter =  id
return a ressource with the id given or error
"""


@app.route('/ressource/<id>', methods=['GET'])
def getRessource(id):
    if id:
        content = {'id': id}
        if content['id']:
            if getAny(OBJECTCSV, content, RESSOURCEFIELDSNAME) == False:
                return jsonify("Ressource not found")
            else:
                return jsonify(getAny(OBJECTCSV, content))
        else:
            return jsonify("ressource given has no Id")
    else:
        return jsonify("Invalid Id given")


@app.route('/objet', methods=['PUT', 'UPDATE'])
def putObject():
    if request.is_json:
        content = request.get_json()
        if len(content) > 5:
            return jsonify("invalid Json, too much parameters")
        else:
            if 'id' and 'name' and "quantity" and "unity" and "user" in content:

                if checkifExistObjet(OBJECTCSV, content, RESSOURCEFIELDSNAME):

                    updateObject(OBJECTCSV, content, RESSOURCEFIELDSNAME)
                    return jsonify("succes, updated object")
                else:
                    missing = []
                    keys = list(content.keys())
                    for re in RESSOURCEFIELDSNAME:
                        if re not in keys:
                            missing.append(re)
                    return jsonify("invalid Json, parameter key invalid, missing: ", missing)
                    # return le missing parameters

            else:
                return jsonify("invalid Json, key parameter invalid")
    else:
        return jsonify("Invalid Json given")


if __name__ == '__main__':
    app.run(debug=True)
