import shutil
from flask import Flask, request, jsonify, make_response
import csv
from flask_cors import CORS, cross_origin
import tempfile


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

RESSOURCEFIELDSNAME = ["id", "name", "quantity", "unity", "user"]
RESSOURCEFIELDSNAMEPOST = ["name", "quantity", "unity", "user"]
USERFIELDSNAME = ["id", "name", "login", "password"]
USERFIELDSNAMEPOST = ["name", "login", "password"]

FIELDSNAMES = {'ressource': RESSOURCEFIELDSNAME,
               'resourcepost': RESSOURCEFIELDSNAMEPOST}

RESSOURCECSV = "ressource.csv"
USERCSV = "user.csv"


"""
clear a csv file 
name = csv filename 
"""


@app.route("/clean/<name>")
def cleancsv(name):
    mycsv = name + ".csv"
    f = open(mycsv, "w+")
    f.close()
    return jsonify("file cleaned")

"""
mycsv = csv filename 
ob = object to get 
fieldsnames = names of the given object' fields
"""


def checkifexistobject(mycsv, ob, fields):
    with open(mycsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        for row in reader:
            if row['id'] == ob['id']:
                return True
        return False

"""
Add an object to the csv file
mycsv = csv filename 
ob = object to get 
fieldsnames = names of the given object' fields
"""


def addobject(mycsv, ob, fields):
    with open(mycsv, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        o = {}
        for f in fields:
            o[f] = ob[f]
        writer.writerow(o)

"""
give a list of all object in the csv file
mycsv = csv filename 
ob = object to get 
fieldsnames = names of the given object' fields
"""


def getall(mycsv, fieldnames):
    o = []
    with open(mycsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            o.append(row)
        return o


"""
update an row inside a given csv file
mycsv = csv filename 
ob = object to get 
fieldsnames = names of the given object' fields
"""


def updateobject(mycsv, ob, fieldsnames):
    temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
    fields = fieldsnames

    with open(mycsv, 'r') as csvfile, temp:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(temp, fieldnames=fields)
        for row in reader:
            if row['id'] == str(ob['id']):
                for f in fieldsnames:
                    row[f] = ob[f]
                o = row
                i = 0
                for r in o:
                    row[fieldsnames[i]] = o[fieldsnames[i]]
                    i = i + 1
            writer.writerow(row)
    shutil.move(temp.name, mycsv)
    return True

"""
get the highest id inside a csv file'list to prevent doubles
mycsv = csv filename 
fieldsnames = names of the given object' fields
"""


def getmax(mycsv, fieldnames):
    with open(mycsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        o = []
        for row in reader:
            o.append(row)
        try:
            return int(o[-1].get('id'))
        except IndexError:
            return 0

"""
get a row from a given "id" inside teh csv file
mycsv = csv filename 
ob = object to get 
fieldsnames = names of the given object' fields
"""


def getany(mycsv, ob, fieldsnames):
    with open(mycsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldsnames)
        for row in reader:
            if row["id"] == ob['id']:
                response = row
                return response
        return False



"""
copy the content of the csv given without the row with specific id in temp file the copy then temp file in teh csv file.
"""

def deleteRes(mycsv, ob, fieldsnames):
    temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
    fields = fieldsnames

    with open(mycsv, 'r') as csvfile, temp:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(temp, fieldnames=fields)
        for row in reader:
            if row['id'] != str(ob['id']):
                writer.writerow(row)
    shutil.move(temp.name, mycsv)
    return True


""""
             _____    _____   _____   _____   _____   _   _   _____    _____   _____  
            |  _  \  | ____| /  ___/ /  ___/ /  _  \ | | | | |  _  \  /  ___| | ____| 
            | |_| |  | |__   | |___  | |___  | | | | | | | | | |_| |  | |     | |__   
            |  _  /  |  __|  \___  \ \___  \ | | | | | | | | |  _  /  | |     |  __|  
            | | \ \  | |___   ___| |  ___| | | |_| | | |_| | | | \ \  | |___  | |___  
            |_|  \_\ |_____| /_____/ /_____/ \_____/ \_____/ |_|  \_\ \_____| |_____| 

"""

"""
post method for objects
:parameter =  request with onject in json
"""


@app.route('/ressource', methods=['POST'])
def postresource():
    print(request.get_json())
    if request.is_json:
        content = request.get_json()
        if len(content) > 4:
            return jsonify("invalid Json, too much parameters")
        else:
            if 'name' and "quantity" and "unity" and "user" in content:
                maxi = getmax(RESSOURCECSV, RESSOURCEFIELDSNAME) + 1
                content['id'] = maxi
                addobject(RESSOURCECSV, content, RESSOURCEFIELDSNAME)
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
return all ressources
"""


@app.route('/ressourceAll', methods=['GET'])
def getallressource():
    return jsonify(getall('ressource.csv', RESSOURCEFIELDSNAME))


"""
get method for ressources
:parameter =  id
return a ressource with the id given or error
"""


@app.route('/ressource/<id>', methods=['GET'])
def getressource(id):
    if id:
        content = {'id': id}
        if content['id']:
            if not getany(RESSOURCECSV, content, RESSOURCEFIELDSNAME):
                return jsonify("Ressource not found")
            else:
                return jsonify(getany(RESSOURCECSV, content, RESSOURCEFIELDSNAME))
        else:
            return jsonify("ressource given has no Id")
    else:
        return jsonify("Invalid Id given")

""""
put method for ressources
update the ressource given in the db
"""


@app.route('/objet', methods=['PUT', 'UPDATE'])
def putobject():
    if request.is_json:
        content = request.get_json()
        if len(content) > 5:
            return jsonify("invalid Json, too much parameters")
        else:
            if 'id' and 'name' and "quantity" and "unity" and "user" in content:

                if checkifexistobject(RESSOURCECSV, content, RESSOURCEFIELDSNAME):

                    updateobject(RESSOURCECSV, content, RESSOURCEFIELDSNAME)
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



"""
delete method of ressource
:parameter = id of the object to delete
delete the object in teh csv file according to the id given
"""


@app.route('/object/<id>', methods=['DELETE'])
@cross_origin()
def delobjet(id):
    if id:
        content = {'id': id}
        if content['id']:
            if not getany(RESSOURCECSV, content, RESSOURCEFIELDSNAME):
                return jsonify("Ressource not found")
            else:
                deleteRes(RESSOURCECSV, content, RESSOURCEFIELDSNAME)
                return jsonify("ressource deleted")
        else:
            return jsonify("ressource given has no Id")
    else:
        return jsonify("Invalid Id given")

"""
                    _   _   _____   _____   _____   
                    | | | | /  ___/ | ____| |  _  \  
                    | | | | | |___  | |__   | |_| |  
                    | | | | \___  \ |  __|  |  _  /  
                    | |_| |  ___| | | |___  | | \ \  
                    \_____/ /_____/ |_____| |_|  \_\ 

"""

"""
post method for users
:parameter =  request with users in json
"""


@app.route('/user', methods=['POST'])
def postuser():
    if request.is_json:
        content = request.get_json()
        if len(content) > len(USERFIELDSNAMEPOST):
            return jsonify("invalid Json, too much parameters")
        else:
            if "name" and "login" and "password" in content:
                maxi = getmax(USERCSV, USERFIELDSNAME) + 1
                content['id'] = maxi
                addobject(USERCSV, content, USERFIELDSNAME)
                return jsonify(content)
            else:
                missing = []
                keys = list(content.keys())
                for re in USERFIELDSNAMEPOST:
                    if re not in keys:
                        missing.append(re)
                return jsonify("invalid Json, parameter key invalid, missing: ", missing)
                # return le missing parameters

    else:
        return jsonify("Invalid Json given")


""""
put method for user
update the user given in the db
"""


@app.route('/user', methods=['PUT', 'UPDATE'])
def putuser():
    if request.is_json:
        content = request.get_json()
        if len(content) > 5:
            return jsonify("invalid Json, too much parameters")
        else:
            if 'id' and 'name' and "login" and "password" in content:

                if checkifexistobject(USERCSV, content, USERFIELDSNAME):
                    updateobject(USERCSV, content, USERFIELDSNAME)
                    return jsonify("succes, updated object")
                else:
                    return jsonify("object not in database")
                    # return le missing parameters

            else:
                return jsonify("invalid Json, key parameter invalid")
    else:
        return jsonify("Invalid Json given")


"""
return all users
"""


@app.route('/userAll', methods=['GET'])
def getalluser():
    return jsonify(getall(USERCSV, USERFIELDSNAME))


"""
get method for ressources
:parameter =  id
return a ressource with the id given or error
"""


@app.route('/user/<identifier>', methods=['GET'])
def getuser(identifier):
    if id:
        content = {'id': identifier}
        if content['id']:
            if not getany(USERCSV, content, USERFIELDSNAME):
                return jsonify("User not found")
            else:
                return jsonify(getany(USERCSV, content, USERFIELDSNAME))
        else:
            return jsonify("user given has no Id")
    else:
        return jsonify("Invalid Id given")


if __name__ == '__main__':
    app.run(debug=True)
