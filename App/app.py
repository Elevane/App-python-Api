from flask import Flask, escape, request, jsonify

app = Flask(__name__)
objets = []


@app.route('/objet/', methods=['POST'])
def postobjet():
    req = request.get_json()
    return jsonify({"you sent" : req})


@app.route('/test')
def test():
    return "zqqzf"


if __name__ == '__main__':
    app.run(debug=True)