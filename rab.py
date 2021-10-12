import flask 
from flask import Flask, jsonify, request
import json 
from sql_optima import check_get_rab, input_target_rab, edit_rab, check_id, get_tgl_target
from convert_rupiah import transfrom_to_rupiah_format
import decimal
from waitress import serve
app = Flask(__name__)

@app.route('/optima/rab&target/mitra/input', methods = ['POST'])
def input_rab():
    json_data = flask.request.json
    if json_data == None:
        hasil = {"message": "process failed"}
        respon = jsonify(hasil)
        return respon, 400
    else:
        if 'id' not in json_data or 'nama_project' not in json_data:
            hasil = {"message": "error request"}
            respon = jsonify(hasil)
            return respon, 401
        else:
            id = json_data ['id']
            np = json_data['nama_project']
            cost = json_data['biaya']
            target = json_data['target']
            doc = json_data['document']
            ab = json_data['add_by']
            ub = json_data['update_by']
            s = json_data ['status']
            cek_id = check_id(id)
            if cek_id == False:
                hasil = {"message": "Forbidden"}
                respon = jsonify(hasil)
                return respon, 403
            else:
                rab_check = check_get_rab(np, id)
                if rab_check != None:
                    hasil = {"message" : "Already exist"}
                    respon = jsonify(hasil)
                    return respon, 208
                else:
                    a = input_target_rab(id, np, cost, target, doc, ab, ub, s)
                    if a == False:
                        hasil = {"message": "input failed"}
                        respon = jsonify(hasil)
                        return respon, 204
                    else:
                        hasil = {"message": "input success"}
                        respon = jsonify(hasil)
                        return respon, 200

@app.route('/optima/rab/show', methods = ['POST'])
def show_rab():
    json_data = request.json
    if json_data == None:
        hasil = {"message": "process failed"}
        respon = jsonify(hasil)
        return respon, 400
    else:
        if 'id' not in json_data or 'nama_project' not in json_data:
            hasil = {"message": "error request"}
            respon = json.dumps(hasil)
            return respon, 401
        else:
            id = json_data ['id']
            np = json_data['nama_project']
            cek_id = check_id(id)
            if cek_id == False:
                hasil = {"message": "Forbidden"}
                respon = jsonify(hasil)
                return respon, 403
            else:
                rab_check = check_get_rab(id, np)
                if rab_check == None:
                    hasil = {"message": "No-content"}
                    respon = jsonify(hasil)
                    return respon, 204
                else:
                    go = float(rab_check)
                    go = "{:.2f}".format(go)
                    go = transfrom_to_rupiah_format(decimal.Decimal(go))
                    hasil = {"message": go}
                    respon = jsonify(hasil)
                    return respon, 200

@app.route('/optima/rab/mitra/edit', methods = ['POST'])
def rab_edit():
    json_data = request.json
    if json_data == None:
        hasil = {"message": "process failed"}
        respon = jsonify(hasil)
        return respon, 400
    else:
        if 'id' not in json_data or 'nama_project' not in json_data or 'biaya' not in json_data:
            hasil = {"message": "error request"}
            respon = json.dumps(hasil)
            return respon, 401
        else:
            id = json_data ['id']
            np = json_data['nama_project']
            ub = json_data ['update_by']
            cost = json_data['biaya']
            cek_idm = check_id(id)
            if cek_idm == False:
                hasil = {"message": "Forbidden"}
                respon = jsonify(hasil)
                return respon, 403
            else:
                rab_check = check_get_rab(id, np)
                if rab_check == None:
                    hasil = {"message": "No-content"}
                    respon = jsonify(hasil)
                    return respon, 204
                else:
                    e_r = edit_rab(cost, ub, np, id)
                    if e_r == False:
                        hasil = {"message": "Update failed"}
                        respon = jsonify(hasil)
                        return respon, 203
                    else:
                        hasil = {"message": "Update success"}
                        respon = jsonify(hasil)
                        return respon, 200

@app.route('/optima/target/show', methods = ['POST'])
def show_target():
    json_data = request.json
    if json_data == None:
        hasil = {"message": "process failed"}
        respon = jsonify(hasil)
        return respon, 400
    else:
        if 'id' not in json_data or 'nama_project' not in json_data:
            hasil = {"message": "error request"}
            respon = jsonify(hasil)
            return respon, 401
        else:
            id = json_data ['id']
            np = json_data['nama_project']
            t = get_tgl_target(id, np)
            if t == None:
                hasil = {"message": "No-content"}
                respon = jsonify(hasil)
                return respon, 204
            else:
                hasil = {"message": t}
                respon = jsonify(hasil)
                return respon, 200

if __name__ == "__main__":
    #serve(app, host="0.0.0.0", port=6012)
    app.run(port=6015, debug=True)