import shutil

from flask import Flask, escape, request, jsonify
import csv
from tempfile import NamedTemporaryFile

app = Flask(__name__)

OBJECTFIELDSNAMES = ["id", "text"]
OBJECTCSV = "o.csv"
TEMPCSV = "temp.csv"

def checkifExistObjet(mycsv, object, fields):
    with open(mycsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        for row in reader:
            if row['id'] == object['id']:
                print(row['id'], object['id'])
                return False
        return True


def addObject(mycsv, object):
    print(object['id'])
    with open(mycsv, 'a', newline='') as csvfile:
        fieldnames = ['id', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({"id" : object['id'], "text" : object['text']})



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
            print(row)
            if row['id'] == str(object['id']):
                print('updating row', row['id'])
                row['text'] = object['text']
                o = row
            row = {'id': row['id'], 'text': row['text']}
            writer.writerow(row)
    shutil.move(tempfile.name, mycsv)
    return True


def getMax(mycsv):

    with open(mycsv, newline='') as csvfile:
        row_count = sum(1 for row in csvfile)
        return row_count

def getAny(mycsv, objet):
    with open(mycsv, newline='') as csvfile:
        fieldnames = ['id', 'text']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            if row["id"] == objet['id']:
                response = row
                return response
        return False
"""
post method for objects
:parameter =  request with onject in json
"""
@app.route('/objet', methods=['POST'])
def postObjet():
    if request.is_json:
        content = request.get_json()
        if len(content) > 1 :
            return jsonify("invalid Json, too much parameters")
        else:
            if 'text' in content:
                max = getMax(OBJECTCSV) + 1
                content['id'] = max
                addObject(OBJECTCSV, content)
                return jsonify(content)
            else:
                return jsonify("invalid Json, parameter key invalid")

    else:
        return jsonify("Invalid Json given")

"""
return all objects
"""
@app.route('/objetAll', methods=['GET'])
def getAllObjet():
    return jsonify(getAll('o.csv', OBJECTFIELDSNAMES))

"""
get method for objects
:parameter =  id
return an object with the id given or error
"""
@app.route('/objet/<id>', methods=['GET'])
def getObjet(id):
    if id:
        content = {'id' : id}
        if content['id']:
            if getAny(OBJECTCSV, content) == False:
                return jsonify("Object not found")
            else:
                return jsonify(getAny(OBJECTCSV, content))
        else:
            return jsonify("Object given has no Id")
    else:
        return jsonify("Invalid Id given")


@app.route('/objet', methods=['PUT', 'UPDATE'])
def putObject():
    if request.is_json:
        content = request.get_json()
        if len(content) > 2 :
            return jsonify("invalid Json, too much parameters")
        else:
            if 'text' and 'id' in content:
                if checkifExistObjet(OBJECTCSV, content, OBJECTFIELDSNAMES):
                    updateObject(OBJECTCSV, content, OBJECTFIELDSNAMES)
                    return jsonify("succes, updated object")
                else:
                    return jsonify('object doesn\'t exist')
            else:
                return jsonify("invalid Json, key parameter invalid")
    else:
        return jsonify("Invalid Json given")


if __name__ == '__main__':
    app.run(debug=True)
