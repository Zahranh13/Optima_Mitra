import mysql.connector
from flask import Flask,request,jsonify
from uuid import uuid4
import secrets
import json
from datetime import datetime
import hashlib
app = Flask(__name__)

def connect_to_sql():
    connect = mysql.connector.connect(host = "localhost", username = "root", database ="db_optima_rev(1)", password = "")
    return connect

def input_mitra(nama_mitra,nama_pic,no_telp,email,password):
    database = connect_to_sql()
    cursor = database.cursor()
    id = gen_id()
    password = encrypt_password(password)
    token = generate_token()
    status = 0
    try:
        cursor.execute("INSERT INTO tb_mitra (id, nama_mitra, nama_pic, no_telp, email, password, dt_add, dt_update, dt_last_login, dt_expired, token, status) VALUES (%s,%s,%s,%s,%s,%s,now(),now(),now(),now(),%s,%s)",(id, nama_mitra,nama_pic,no_telp,email,password, token, status))
        database.commit()
        check = True
    except(mysql.connector.Error,mysql.connector.Warning) as error:
        print(error)
        check = False
    if check == False:
        return False
    else:
        return True

def gen_id():
    data = str(uuid4().hex)[:12]
    result = "MTR-" + data
    return result

def generate_token():
    return secrets.token_hex(256)

def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_mitra(im, nm):
    database = connect_to_sql()
    direct = database.cursor()
    direct.execute ("Select id from tb_mitra where email = %s and password = %s", (im, nm))
    np = direct.fetchone()
    if np == None:
        return None
    else:
        return np[0]

def check_mitra(id):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute ("SELECT id from tb_mitra where nama_mitra = %s", (id, ))
        check = direct.fetchone()
    except (mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        check = None
    if check == None:
        return False
    else:
        return check[0]

def check_id(im):    
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT id from tb_mitra WHERE id=%s", (im))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]

def get_id():
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute ("SELECT id from tb_mitra WHERE nama_mitra = %s")
        r = [x for x in direct]
        c = [x[0] for x in direct.description]
    except (mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        r = []
        c = []    
    d = []
    for row in r:
        data ={}
        for p, val in zip(c, r):
            data[p] = val
        d.append(data)
    Jsonresult = json.dumps(d)
    return Jsonresult

def insert_request (im, nm, np, nt):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("INSERT INTO permintaan (nodin, pemohon, perihal, tanggal) VALUES (%s, %s, %s, %s)", (im, nm, np, nt))
        database.commit()
        check = True
    except (mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
    if check == False:
        return False
    else:
        return True

def check_center(im, nm):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT nama_project, id From tb_center WHERE nama_project = %s and id = %s", (im, nm))
        check = direct.fetchone()
    except (mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
    if check == None:
        return False
    else:
        return True

def update_status_pada_center(im, nm, np, nt):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("UPDATE center SET dt_add=%s, status =%s WHERE nama_project = %s and id = %s", (im, nm, np, nt))
        database.commit()
        check = True
    except (mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
    if check == None:
        return False
    else:
        return True

def check_project(im):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT nama_project From tb_center WHERE nama_project = %s", (im, ))
        z = direct.fetchone()
    except (mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return False
    else:
        return True

def get_nama_mitra(im):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT nama_mitra FROM tb_mitra WHERE id = %s", (im))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
    if z == None:
        return None
    else:
        return z[0]

def check_id(im):    
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT id from tb_mitra WHERE id=%s", (im))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]

def insert_progress(id, np, ab, ub, l, k, s, da, du, b, d):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute ("INSERT INTO progress (id, nama_project, add_by, update_by, level, keterangan, status, dt_add, dt_update, bukti, deskripsi) VALUES (%s, %s, %s, %s, %s, %s, %s, now(), now(), %s, %s)", (id, np, ab, ub, l, k, s, da, du, b, d))
        database.commit()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)   

def get_keterangan():
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT keterangan FROM tb_progress WHERE nama_project=%s", )
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]

def update_status(z, y, x, w, v, u, t, s):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute ( "UPDATE progress SET status = %s, bukti = %s., tanggal=%s, deskripsi=%s WHERE id _mitra and nama+project=%s and level =%s and keterangan = %s", (z, y, x, w, v, u, t, s))
        database.commit()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None

def show_progress(z):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.excecute( "SELECT nama_project, nama_mitra, status, FROM tb_progress ps JOIN mitra mt ON ps.id = mt.id WHERE status = %s", (z, ))
        r = [x for x in direct]
        c = [x[0] for x in direct.description]
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
        r = []
        c = []
    d = []
    for row in r:
        data ={}
        for p, val in zip(c, r):
            data[p] = val
        d.append(data)
    Jsonresult = json.dumps(d)
    return Jsonresult

def check_progress(z):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT nama_project, id FROM tb_progress WHERE nama_project=%s and id=%s", (z))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]

def show_progress_desc(z, y):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.excecute( "SELECT nama_project, status FROM tb_progress WHERE keterangan = %s and level = %s", (z, y, ))
        r = [x for x in direct]
        c = [x[0] for x in direct.description]
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        r = []
        c = []
    d = []
    for row in r:
        data ={}
        for p, val in zip(c, r):
            data[p] = val
        d.append(data)
    Jsonresult = json.dumps(d)
    return Jsonresult

def check_level_progress_desc(nama_project, level, keterangan):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT nama_project, level, keterangan FROM tb_progress WHERE nama_project=%s and level=%s and id=%s", (nama_project, level, keterangan))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]

def insert_progress_persiapan(z, y, x):
    level = "persiapan"
    keterangan = ["Survei Lokasi", "Perijinan", "Sitac"]
    status = "belum"
    bukti = "kosong"
    deskripsi = "kosong"
    for i in keterangan:
        check = check_level_progress_desc(z, y, x)
        if check == True:
            insert_progress(z, y, level, bukti, i, status, x, deskripsi)

def insert_progress_instalasi(z, y, x):
    level = "instalasi"
    keterangan = ["Material Delivery", "Penarikan Kabel", "Pemasangan ODP", "Penanaman Tiang", "Pemasangan ODC"]
    status = "belum"
    bukti = "kosong"
    deskripsi = "kosong"
    for i in keterangan:
        check = check_level_progress_desc(z, y, x)
        if check == True:
            insert_progress(z, y, level, bukti, i, status, x, deskripsi)

def insert_progress_go_live(z, y, x):
    level = "go live"
    keterangan = ["Main Core", "Redaman"]
    status = "belum"
    bukti = "kosong"
    deskripsi = "kosong"
    for i in keterangan:
        check = check_level_progress_desc(z, y, x)
        if check == True:
            insert_progress(z, y, level, bukti, i, status, x, deskripsi)

def check_selesai_progress_persiapan(x, y):
    database = connect_to_sql()
    direct = database.cursor()
    level = "persiapan"
    status = "selesai"
    direct.execute("SELECT COUNT(keterangan) FROM tb_progress WHERE id = %s and nama_project = %s and level = %s and status = %s", (x, y, level, status))
    z = direct.fetchone()
    try:
        j = int(z[0])
        if j >= 2:
            return True
        else:
            return False
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)

def check_selesai_progress_instalasi(x, y):
    database = connect_to_sql()
    direct = database.cursor()
    level = "instalasi"
    status = "selesai"
    try:
        direct.execute("SELECT COUNT(keterangan) FROM tb_progress WHERE id = %s and nama_project = %s and level = %s and status = %s", (x, y, level, status))
        z = direct.fetchone()
        j = int(z[0])
        if j >= 4:
            return True
        else:
            return False
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)

def check_selesai_progress_go_live(x, y):
    database = connect_to_sql()
    direct = database.cursor()
    level = "go live"
    status = "selesai"
    direct.execute("SELECT COUNT(keterangan) FROM tb_progress WHERE id = %s and nama_project = %s and level = %s and status = %s", (x, y, level, status))
    try:
        z = direct.fetchone()
        j = int(z[0])
        if j >= 4:
            return True
        else:
            return False
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)

def count_progress(x, y):
    persiapan_check = check_selesai_progress_persiapan(x, y)
    instalasi_check = check_selesai_progress_instalasi(x, y)
    go_live_check = check_selesai_progress_go_live(x, y)
    try:
        if persiapan_check == True and instalasi_check == True and go_live_check == True:
            hasil = "100"
            return hasil
        elif persiapan_check == True and instalasi_check == True and go_live_check == False:
            hasil = "66.6"
            return hasil
        elif persiapan_check == True and instalasi_check == False and go_live_check == False:
            hasil = "33.3"
            return hasil
        else:
            hasil = "0"
            return hasil
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)

def count_progress_level(x, y):
    database = connect_to_sql()
    direct = database.cursor()
    status = "selesai"
    try:
        direct.execute ("SELECT COUNT(keterangan) FROM tb_progress WHERE nama_project=%s and level = %s and status = %s", (x, y, status))
        z  = direct.fetchone()
        j = int(z[0])
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
    if y == "persiapan":
        percentage = float((j/2)*100)
        return str(percentage)
    elif y == "instalasi":
        percentage = float((j/4)*100)
        return str(percentage)
    elif y == "go live":
        percentage = float((j/1)*100)
        return str(percentage)   

def get_filebukti(z, y, x):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT bukti FROM tb_progress WHERE nama_project = %s and level = %s and status = %s", (z, y, x))
        d = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        d = None
    if d == None:
        return None
    else:
        return d
    

def input_target_rab(z, y, x, w):
    database = connect_to_sql()
    direct = database.cursor()
    try: 
        direct.execute ( "INSERT INTO rab (nama_project, id, biaya, tgl_target VALUES (%s, %s, %s, %s)", (z, y, x, w))
        database.commit()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)

def check_get_rab(z, y):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT biaya FROM tb_rab WHERE id =%s and nama_project = %s", (z,y))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]

def edit_rab(z, y, x):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("UPDATE rab SET biaya = %s WHERE nama_project = %s and id = %s", (z, y, x))
        database.commit()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)

def get_progress_project():
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute ("SELECT nama_project, status, nama_mitra, center.id From tb_center INNER JOIN mitra ON center.id = mitra.id")
        r = [x for x in direct]
        c = [x[0] for x in direct.description]
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        r = []
        c = []
    d = []
    for row in r:
        data ={}
        for p, val in zip(c, r):
            data[p] = val
        d.append(data)
    Jsonresult = json.dumps(d)
    return Jsonresult   
   
def search_get_progress_project(nama_project):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT nama_project, status, nama_mitra, center.id From tb_center INNER JOIN mitra ON center.id = mitra.id WHERE nama_project LIKE %s", ("%" + nama_project +"%",))
        r = [x for x in direct]
        c = [x[0] for x in direct.description]
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        r = [] 
        c = []
    d = []
    for row in r:
        data ={}
        for p, val in zip(c, r):
            data[p] = val
        d.append(data)
    Jsonresult = json.dumps(d)
    return Jsonresult
    
def project_desc(nama_project, level, keterangan):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT deskripsi FROM tb_progress WHERE nama_project = %s and level = %s and keterangan = %s", (nama_project, level, keterangan))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]
    

def get_tgl_project(status, nama_project, id):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT tanggal From tb_center WHERE status=%s AND nama_project=%s AND id=%s", (status, nama_project, id))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]

def get_tgl_project_selesai (nama_project, id):
    status = "selesai"
    z = get_tgl_project(status, nama_project, id)
    return z

def get_tgl_target(nama_project, id):
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT tgl_target From tb_rab WHERE nama_project=%s AND id=%s", (nama_project, id))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]

def count_center_status_belum_project(id):
    database = connect_to_sql()
    direct = database.cursor()
    status = "belum"
    try:
        direct.execute("SELECT COUNT(nama_project) From tb_center WHERE id=%s AND status = %s", (id, status))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]

def count_center_status_proses_project(id):
    database = connect_to_sql()
    direct = database.cursor()
    status = "proses"
    try:
        direct.execute("SELECT COUNT(nama_project) From tb_center WHERE id=%s AND status = %s", (id, status))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]

def count_center_status_selesai_project(id):
    database = connect_to_sql()
    direct = database.cursor()
    status = "selesai"
    try:
        direct.execute("SELECT COUNT(nama_project) From tb_center WHERE id=%s AND status = %s", (id, status))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        z = None
    if z == None:
        return None
    else:
        return z[0]

def get_all_mitra_with_status():
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute ("SELECT id, nama_mitra From tb_mitra")
        ro = [x for x in direct]
        co = [x[0] for x in direct.description]
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)
        ro = []
        co = []
    datas =[]
    for row in ro:
        data = {}
        for prop, val in zip(co, ro):
            data[prop] = val
        datas.append(data)
    dataJson = json.dumps(datas)

    for i in range (len(datas)):
        datas[i]['belum'] = count_center_status_belum_project(datas[i]['id'])
        datas[i]['proses'] = count_center_status_proses_project(datas[i]['id'])
        datas[i]['selesai'] = count_center_status_selesai_project(datas[i]['id'])

    datajson = json.dumps(datas)
    return datajson

def count_project_stat_belum(tahun):
    database = connect_to_sql()
    direct = database.cursor()
    status = "belum"
    try:
        direct.execute("SELECT COUNT(nama_project) From tb_center WHERE YEAR(tanggal) = %s AND status=%s", (tahun, status))
        z = direct.fetchone()
    except (mysql.connector.Error,mysql.connector.Warning) as e:
        print(e)
        z = None
    if z == None:
        return "0"
    else:
        return z[0]

def count_project_stat_proses(tahun):
    database = connect_to_sql()
    direct = database.cursor()
    status = "proses"
    try:
        direct.execute("SELECT COUNT(nama_project) From tb_center WHERE YEAR(tanggal)=%s AND status=%s", (tahun, status))
        z = direct.fetchone()
    except (mysql.connector.Error, mysql.connector.Warning) as e:
        print(e)
        z = None
    if z == None:
        return "0"
    else:
        return z[0]

def count_project_stat_selesai(tahun):
    database = connect_to_sql()
    direct = database.cursor()
    status = "selesai"
    try:
        direct.execute("SELECT COUNT(nama_project) From tb_center WHERE YEAR(tanggal)=%s AND status=%s", (tahun, status))
        z = direct.fetchone()
    except(mysql.connector.Error, mysql.connector.Warning) as e:
        print(e)
        z = None
    if z == None:
        return "0"
    else:
        return z[0]

def list_tahun_center():
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT YEAR(tanggal) as tahun From tb_center")
        ro = [x for x in direct]
        co = [ x[0] for x in direct.description]
    except(mysql.connector.Error, mysql.connector.Warning) as e:
        print(e)
        ro = []
        co = []
    datas = []
    for row in ro:
        data = {}
        for prop, val in zip(co, ro):
            data[prop] = val
        datas.append(data)
    dataJson = json.dumps(datas)
    return dataJson

def count_progress(x, y):
    persiapan_check = check_selesai_progress_persiapan(x, y)
    instalasi_check = check_selesai_progress_instalasi(x, y)
    go_live_check = check_selesai_progress_go_live(x, y)
    try:
        if persiapan_check == True and instalasi_check == True and go_live_check == True:
            hasil = "100"
            return hasil
        elif persiapan_check == True and instalasi_check == True and go_live_check == False:
            hasil = "66.6"
            return hasil
        elif persiapan_check == True and instalasi_check == False and go_live_check == False:
            hasil = "33.3"
            return hasil
        else:
            hasil = "0"
            return hasil
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)

def count_progress_level(x, y):
    database = connect_to_sql()
    direct = database.cursor()
    status = "selesai"
    try:
        direct.execute ("SELECT COUNT(keterangan) FROM tb_progress WHERE nama_project=%s and level = %s and status = %s", (x, y, status))
        z  = direct.fetchone()
        j = int(z[0])
        if y == "persiapan":
            percentage = float((j/2)*100)
            return str(percentage)
        elif y == "instalasi":
            percentage = float((j/4)*100)
            return str(percentage)
        elif y == "go live":
            percentage = float((j/1)*100)
            return str(percentage)
    except(mysql.connector.Error, mysql.connector.Warning) as error :
        print(error)

def show_level_progress():
    database = connect_to_sql()
    direct = database.cursor()
    try:
        direct.execute("SELECT  DISTINCT `level` FROM `progress` WHERE nama_project=%")
        ro = [x for x in direct]
        co = [ x[0] for x in direct.description]
    except(mysql.connector.Error, mysql.connector.Warning) as e:
        print(e)
        ro = []
        co = []
    datas = []
    for row in ro:
        data = {}
        for prop, val in zip(co, ro):
            data[prop] = val
        datas.append(data)
    dataJson = json.dumps(datas)
    return dataJson
    
def show_level_progress_percentage(z):
    d = show_level_progress()
    for i in range (len(d)):
        d[i]['persentase'] = count_progress_level(z,d[i]['level'])
    Jsonresult = json.dumps(d)
    return Jsonresult
