import flask
from flask import Flask, jsonify, request
from sql_optima import insert_center, check_mitra, get_center, check_id, get_id, update_status_pada_center
import json
from waitress import serve
app = Flask(__name__)

@app.route('/optima/center/input', methods = ['POST'])
def input_project():
    json_data = flask.request.json
    if json_data == None:
        hasil = {"message": "process failed"}
        respon = jsonify(hasil)
        return respon, 400
    else:
        if 'id' not in json_data:
            hasil = {"message": "error request"}
            respon = jsonify(hasil)
            return respon, 401
        else:
            id = json_data ['id']
            np = json_data ['nama_project']
            mitra = json_data ['mitra']
            ab = json_data ['add_by']
            ub = json_data ['update_by']
            cek_mitra = check_mitra(id)
            if cek_mitra == False:
                hasil = {"message": "Forbidden"}
                respon = jsonify(hasil)
                return respon, 403
            else:
                go = insert_center(id, np, mitra, ab, ub)
                if go == False:
                    hasil = {"message": "Input failed"}
                    respon = jsonify(hasil)
                    return respon, 204
                else:    
                    hasil = {"message": "Input success"}
                    respon = jsonify(hasil)
                    return respon, 200

@app.route('/optima/center/show/belum', methods = ['POST'])
def show_center_belum():
    json_data = flask.request.json
    if json_data == None:
        hasil = []
        respon = json.dumps(hasil)
        return respon, 400
    else:
        if 'id' not in json_data:
            hasil = []
            respon = json.dumps(hasil)
            return respon, 401
        else:
            id = json_data['id']
            st = "belum"
            id_check = check_id(id)
            if id_check == False:
                hasil = []
                respon = json.dumps (hasil)
                return respon, 203
            else:
                respon = get_center(id, st)
                if get_center == False:
                    hasil = []
                    respon = json.dumps(hasil)
                    return respon, 204
                else:
                    hasil = []
                    respon = json.dumps(hasil)
                    return respon, 200

@app.route ('/optima/center/show/proses', methods = ['POST'])
def show_center_proses():
    json_data = flask.request.json
    if json_data == None:
        hasil = []
        respon = json.dumps(hasil)
        return respon, 400
    else:
        if 'id' not in json_data:
            hasil = []
            respon = json.dumps(hasil)
            return respon, 401
        else:
            id = json_data['id']
            st = "proses"
            id_check = check_id(id)
            if id_check == False:
                hasil = []
                respon = json.dumps (hasil)
                return respon, 403
            else:
                respon = get_center(id, st)
                return respon, 200
    
@app.route ('/optima/center/show/selesai', methods = ['POST'])
def show_center_selesai():
    json_data = flask.request.json
    if json_data == None:
        hasil = []
        respon = json.dumps(hasil)
        return respon, 400
    else:
        if 'id' not in json_data:
            hasil = []
            respon = json.dumps(hasil)
            return respon, 401
        else:
            id = json_data['id']
            st = "selesai"
            id_check = check_id(id)
            if id_check == False:
                hasil = []
                respon = json.dumps (hasil)
                return respon, 403
            else:
                respon = get_center(id, st)
                return respon, 200 

@app.route ('/optima/center/update', methods = ['POST'])
def update_center():
    json_data = flask.request.json
    if json_data == None:
        hasil = {"message": "process failed"}
        respon = jsonify(hasil)
        return respon, 400
    else:
        if 'id' not in json_data or 'nama_project' not in json_data or 'status' not in json_data:
            hasil = {"message": "error request"}
            respon = jsonify(hasil)
            return respon, 401
        else:
            id = json_data['id']
            np = json_data['nama_project']
            stat = json_data['status']
            ub = json_data ['update_by']
            id_check = check_id(id)
            if id_check == False:
                hasil = {"message": "Forbidden"}
                respon = jsonify(hasil)
                return respon, 403
            else:
                update_status_pada_center(stat, ub, np ,id)
                hasil = {"message" :"Update success"}
                respon = jsonify(hasil)
                return respon, 200

if __name__ == "__main__":
    #serve (app, host="0.0.0.0", port=6008)
    app.run(port=6014, debug=True)
