from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Barang(db.Model):
    kode_barang = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(100))
    harga_barang = db.Column(db.Integer)


class Transaksi(db.Model):
    kode_transaksi = db.Column(db.Integer, primary_key=True)
    kode_barang = db.Column(db.Integer, db.ForeignKey('barang.kode_barang'))
    jumlah_barang = db.Column(db.Integer)
    total_harga = db.Column(db.Integer)

    barang = db.relationship('Barang', backref='transaksi', lazy='joined')
