from bson import json_util
from bson.objectid import ObjectId
from flask import Flask, request, Response, jsonify, url_for, flash
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from flask_mongoengine import MongoEngine
import os
import urllib.request
app = Flask(__name__)
app.secret_key = 'desafio'
app.config["MONGO_URI"] = "mongodb://localhost:27017/desafio"
mongo = PyMongo(app)


UPLOAD_FOLDER = 'static/img'
app.config ['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '_' in filename and filename.rsplit('_', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/cliente', methods=['POST'])
def cria_cliente():
    nome = request.json['nome']
    email = request.json['email']
    telefone = request.json['telefone']
    profissao = request.json['profissao']

    if nome and email:
        mongo.db.cliente.insert_one({'nome': nome, 'email': email, 'telefone': telefone, 'profissao': profissao})
    else:
        {'message': 'recebida'}
    return{'message': 'recebida'}

@app.route('/cliente', methods=['GET'])
def lista_cliente():
    cliente = mongo.db.cliente.find()
    response = json_util.dumps(cliente)
    return Response(response, mimetype='application/json')

@app.route('/cliente/<id>', methods=['GET'])
def lista_cliente_id(id):
    cliente = mongo.db.cliente.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(cliente)
    return Response(response, mimetype='application/json')

@app.route('/cliente/<id>', methods=['DELETE'])
def deleta_cliente(id):
    mongo.db.cliente.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Cliente' + id + 'deletado com sucesso'})
    return response

@app.route("/upload", methods=["POST"])
def save_upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        mongo.db.upload.save_file({'file': file})
        return {'message': 'Arquivo enviado corretamente'}
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
    return {'message': 'recebida'}

if __name__== "__main__":
    app.run(debug=True)