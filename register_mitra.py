import flask 
from flask import Flask, jsonify, request
import hashlib 
import json 
from uuid import uuid4
from sql_optima import check_mitra, input_mitra
from waitress import serve
app = Flask(__name__)

@app.route('/optima/mitra/register', methods = ['POST'])
def mitra_register():
    try:
        json_data = flask.request.json
    except ValueError as error :
        hasil = {"message": error}
        respon = jsonify(hasil)
        return respon, 400
    
    if 'nama_mitra' not in json_data or 'nama_pic' not in json_data or 'no_telp' not in json_data or 'email' not in json_data or 'password' not in json_data:
        hasil = {"message": "error request"}
        respon = jsonify(hasil)
        return respon, 401

    else:
        namit = json_data['nama_mitra']
        napi = json_data['nama_pic']
        notel = json_data ['no_telp']
        em = json_data['email']
        p = json_data['password']
        check = input_mitra(namit, napi, notel, em, p)
        if check == False:
            result = {"message":"Regist failed"}
            resp = jsonify(result)
            return resp,208
        else:
            result = {"message":"Regist success"}
            resp = jsonify(result)
            return resp,200 

if __name__ == "__main__":
    #serve(app, host="0.0.0.0", port=6011)
    app.run(port=6011, debug=True)

    