from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Barang, Transaksi
import locale
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'rahasia'

db.init_app(app)

# format currency
def format_rupiah(value):
    try:
        value = int(value)
        return f"Rp {value:,.0f}".replace(",", ".")
    except:
        return value

app.jinja_env.filters['rupiah'] = format_rupiah

# Home Route
@app.route('/')
@login_required
def home():
    total_barang = Barang.query.count()
    total_transaksi = Transaksi.query.count()
    return render_template('home.html', total_barang=total_barang, total_transaksi=total_transaksi)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Silakan masuk terlebih dahulu."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home')) 
        else:
            flash('Username atau password salah!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrasi berhasil. Silakan login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Routes Barang
@app.route('/barang')
@login_required
def list_barang():
    page = request.args.get('page', 1, type=int)
    barang = Barang.query.paginate(page=page, per_page=5, error_out=False)
    return render_template('barang/list.html', barang=barang)

@app.route('/barang/tambah', methods=['GET', 'POST'])
@login_required
def tambah_barang():
    if request.method == 'POST':
        nama = request.form['nama_barang']
        harga = request.form['harga_barang']
        
        if not nama or not harga or int(harga) <= 0:
            flash("Nama barang tidak boleh kosong dan harga harus lebih besar dari 0", "danger") 
            return redirect(url_for('list_barang'))
        
        new_barang = Barang(nama_barang=nama, harga_barang=int(harga))
        db.session.add(new_barang)
        db.session.commit()
        flash('Barang berhasil ditambahkan!', 'success')
    return redirect(url_for('list_barang'))

@app.route('/barang/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_barang(id):
    barang = db.session.get(Barang, id)
    
    if request.method == 'POST':
        barang.nama_barang = request.form['nama_barang']
        harga = request.form['harga_barang']
        
        if not barang.nama_barang or not harga or int(harga) <= 0:
            flash("Nama barang tidak boleh kosong dan harga harus lebih besar dari 0", "danger")
            return redirect(url_for('list_barang'))
        
        barang.harga_barang = int(harga)
        db.session.commit()
        flash('Barang berhasil diedit!', 'success')
    return redirect(url_for('list_barang'))
    


@app.route('/barang/hapus/<int:id>')
@login_required
def hapus_barang(id):
    barang = db.session.get(Barang, id)
    db.session.delete(barang)
    db.session.commit()
    flash('Barang berhasil dihapus!', 'success')    
    return redirect(url_for('list_barang'))

# Routes Transaksi
@app.route('/transaksi')
@login_required
def list_transaksi():
    barang_list = Barang.query.all()
    page = request.args.get('page', 1, type=int)
    transaksi = Transaksi.query.paginate(page=page, per_page=5, error_out=False)
    return render_template('transaksi/list.html', transaksi=transaksi, barang_list=barang_list)

@app.route('/transaksi/tambah', methods=['POST'])
@login_required
def tambah_transaksi():
    kode_barang = int(request.form['kode_barang'])
    jumlah = request.form['jumlah_barang']

    if not jumlah or not jumlah.isdigit() or int(jumlah) <= 0:
        flash("Jumlah barang harus lebih besar dari 0 dan harus berupa angka yang valid", "danger")
        return redirect(url_for('list_transaksi'))

    jumlah = int(jumlah)
    barang = Barang.query.get(kode_barang)
    if not barang:
        flash("Kode barang tidak ditemukan", "danger")
        return redirect(url_for('list_transaksi'))

    total = jumlah * barang.harga_barang
    new_transaksi = Transaksi(kode_barang=kode_barang, jumlah_barang=jumlah, total_harga=total)
    db.session.add(new_transaksi)
    db.session.commit()
    flash("Transaksi berhasil ditambahkan!", "success")
    return redirect(url_for('list_transaksi'))

@app.route('/transaksi/edit/<int:id>', methods=['POST'])
@login_required
def edit_transaksi(id):
    transaksi = Transaksi.query.get(id)
    if not transaksi:
        flash("Transaksi tidak ditemukan.", "danger")
        return redirect(url_for('list_transaksi'))

    kode_barang = request.form['kode_barang']
    jumlah = request.form['jumlah_barang']

    if not jumlah or not jumlah.isdigit() or int(jumlah) <= 0:
        flash("Jumlah barang harus lebih besar dari 0 dan harus berupa angka yang valid", "danger")
        return redirect(url_for('list_transaksi'))

    barang = Barang.query.get(kode_barang)
    if not barang:
        flash("Barang tidak ditemukan.", "danger")
        return redirect(url_for('list_transaksi'))

    transaksi.kode_barang = int(kode_barang)
    transaksi.jumlah_barang = int(jumlah)
    transaksi.total_harga = transaksi.jumlah_barang * barang.harga_barang
    db.session.commit()
    flash("Transaksi berhasil diedit!", "success")
    return redirect(url_for('list_transaksi'))

@app.route('/transaksi/hapus/<int:id>')
@login_required
def hapus_transaksi(id):
    transaksi = Transaksi.query.get(id)
    db.session.delete(transaksi)
    db.session.commit()
    flash("Transaksi berhasil dihapus!", "success")
    return redirect(url_for('list_transaksi'))

if __name__ == '__main__':
    os.makedirs('templates/barang', exist_ok=True)
    os.makedirs('templates/transaksi', exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)


