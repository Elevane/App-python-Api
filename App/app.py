from flask import Flask, escape, request, jsonify
import csv

app = Flask(__name__)

OBJECTFIELDSNAMES = ["id", "text"]
"""
check if a given object exist in given csv file



def checkifExistObjet(mycsv, object):
    with open(mycsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['id'] == object['id']:
                print(row['id'], object['id'])
                return False
        return True
"""

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
                max = getMax("o.csv") + 1
                content['id'] = max
                addObject("o.csv", content)
                return jsonify(content)
            else:
                return jsonify("invalid Json, parameter key invalid")

    else:
        return jsonify("Invalid Json given")


@app.route('/objetAll', methods=['GET'])
def getAllObjet():
    return jsonify(getAll('o.csv', OBJECTFIELDSNAMES))


@app.route('/objet/<id>', methods=['GET'])
def getObjet(id):
    if id:
        content = {'id' : id}
        if content['id']:
            if getAny("o.csv", content) == False:
                return jsonify("Object not found")
            else:
                return jsonify(getAny("o.csv", content))
        else:
            return jsonify("Object given has no Id")
    else:
        return jsonify("Invalid Id given")


if __name__ == '__main__':
    app.run(debug=True)
