from flask import Flask, escape, request, jsonify
import csv

app = Flask(__name__)
objets = []


def checkifExistObjet(object):

    with open('o.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['id'] == object['id']:
                print(row['id'] , object['id'])
                return False
        return True


def addObject(object):
    with open('o.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'test']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'id': object['id'], 'test': object['test']})

def getAll():
    o = []
    with open('o.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            o.append(row)
        return o


@app.route('/objet', methods=['POST'])
def postObjet():
    if request.is_json:
        content = request.get_json()
        if content['id']:
            if checkifExistObjet(content):
                addObject(content)
                return jsonify(content)
            return jsonify("Object already exist")

        else:
            return jsonify("Object given has no Id")
    else:
        return jsonify("Invalid Json given")


@app.route('/objet', methods=['GET'])
def getObjet():
    return jsonify(getAll())


if __name__ == '__main__':
    app.run(debug=True)
