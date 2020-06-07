from flask import Flask, escape, request, jsonify

app = Flask(__name__)
objets = []


@app.route('/objet', methods=['POST'])
def postObjet():
    if request.is_json:
        content = request.get_json()
        return jsonify(content)


if __name__ == '__main__':
    app.run(debug=True)