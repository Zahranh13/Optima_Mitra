import flask 
from flask import Flask, jsonify, request
import hashlib 
import json 
import uuid
from sql_optima import login_mitra
from waitress import serve
app = Flask(__name__)

@app.route("/optima/mitra/login", methods = ['POST'])
def mitralogin():
    json_data = flask.request.json
    if json_data == None:
        hasil = {"message": "process failed"}
        respon = jsonify (hasil)
        return respon, 400
    else:
        if 'email' not in json_data or 'password' not in json_data:
            hasil = {"message": "error request"}
            respon = jsonify(hasil)
            return respon, 401
        else:
            em = json_data['email']
            psw = json_data['password']
            pw = hashlib.sha256(psw.encode()).hexdigest()
            check = login_mitra(em,pw)
            if check == None:
                hasil = {"message": "Unregistered account"}
                respon = jsonify(hasil)
                return respon, 203
            else:
                hasil = {"message": check}
                respon = jsonify(hasil)
                return respon, 200

if __name__ == "__main__":
    #serve(app, host="0.0.0.0", port=6002)
    app.run (port=6012, debug=True)