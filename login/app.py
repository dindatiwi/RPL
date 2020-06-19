from flask import Flask, render_template, session, request, url_for, redirect
from flask_mysqldb import MySQL,MySQLdb
app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rentalps'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# login form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'petugas' in request.form:
        petugas = request.form['petugas']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM petugas WHERE namaPetugas=%s",(petugas,))
        user = cur.fetchone()
        cur.close()
        if user:
            session['namaPetugas'] = user['namaPetugas']
            return redirect(url_for('home'))
        else:
            return "Anda Bukan Admin"
    return render_template('index.html')

# crud tabel transaksi
@app.route('/home',methods=['GET', 'POST'])
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM rental_main")
    rv = cur.fetchall()
    cur.close()
    return render_template('home.html', rental=rv)

@app.route('/simpan',methods=['GET', 'POST'])
def simpan():
    notv = request.form['tv']
    nops = request.form['ps']
    kode_rm = request.form['id']
    tgl = request.form['tgl']
    durasi = request.form['durasi']
    petugas = request.form['petugas']
    cur = mysql.connection.cursor()
    biaya = int(durasi)*5000
    cur.execute("INSERT INTO rental_main (kode_rm,no_inv_tv,no_inv_ps,kodePetugas,tanggal,lama_main,biaya) VALUES (%s,%s,%s,%s,%s,%s,%s)",(kode_rm,notv,nops,petugas,tgl,durasi,biaya,))
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    kode_rm = request.form['id']
    notv = request.form['tv']
    nops = request.form['ps']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE rental_main SET no_inv_tv=%s,no_inv_ps=%s WHERE kode_rm=%s", (notv,nops,kode_rm,))
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/hapus/<string:id_data>',methods=['GET', 'POST'])
def hapus(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM rental_main WHERE kode_rm=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('home'))

#crud tabel master
@app.route("/inventory",methods=['GET', 'POST'])
def inventory():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM inv_tv")
    inv = cur.fetchall()
    cur.close()
    return render_template('inventory.html', tv=inv)

@app.route('/updateinv', methods=['GET', 'POST'])
def updateinv():
    notv = request.form['id']
    tv = request.form['tv']
    kondisi = request.form['kondisi']
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE inv_tv SET kode_jenis_tv=%s,kondisi=%s,status=%s WHERE no_inv_tv=%s", (tv,kondisi,status,notv))
    mysql.connection.commit()
    return redirect(url_for('inventory'))

@app.route('/simpaninv',methods=['GET', 'POST'])
def simpaninv():
    notv = request.form['id']
    tv = request.form['tv']
    kondisi = request.form['kondisi']
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO inv_tv (no_inv_tv,kode_jenis_tv,kondisi,status) VALUES (%s,%s,%s,%s)",(notv,tv,kondisi,status,))
    mysql.connection.commit()
    return redirect(url_for('inventory'))

@app.route('/hapusinv/<string:no_inv_tv>',methods=['GET', 'POST'])
def hapusinv(no_inv_tv):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM inv_tv WHERE no_inv_tv=%s", (no_inv_tv,))
    mysql.connection.commit()
    return redirect(url_for('inventory'))

@app.route('/laporan',methods=['GET', 'POST'])
def laporan():
    return render_template('laporan.html')

@app.route('/lapor',methods=['GET', 'POST'])
def lapor():
    tgls = request.form['tgls']
    tgld = request.form['tgld']
    cur = mysql.connection.cursor()
    cur.execute("SELECT tanggal,biaya FROM rental_main WHERE tanggal>%s and tanggal<=%s", (tgls,tgld,))
    mysql.connection.commit()
    rv = cur.fetchall()
    return render_template('laporan.html', st=rv)


if __name__ == '__main__':
    app.run(debug=True)