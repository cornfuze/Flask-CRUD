import unittest
from app import app, db, Barang

class CrudTestCase(unittest.TestCase):
    def setUp(self):
        # Setup app dan database untuk testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Bersihkan database setelah test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self):
        # Daftarkan dan login user untuk akses CRUD
        self.app.post('/register', data=dict(username='test', password='test'))
        self.app.post('/login', data=dict(username='test', password='test'))

    def test_tambah_barang(self):
        self.login()
        response = self.app.post('/barang/tambah', data=dict(nama_barang='Pensil', harga_barang='2000'), follow_redirects=True)
        self.assertIn(b'Barang berhasil ditambahkan!', response.data)
        with app.app_context():
            barang = Barang.query.filter_by(nama_barang='Pensil').first()
            self.assertIsNotNone(barang)

    def test_edit_barang(self):
        self.login()
        # Tambah barang dulu
        self.app.post('/barang/tambah', data=dict(nama_barang='Buku', harga_barang='5000'))
        with app.app_context():
            barang = Barang.query.filter_by(nama_barang='Buku').first()
            # Edit barang
            response = self.app.post(f'/barang/edit/{barang.kode_barang}', data=dict(nama_barang='Buku Tulis', harga_barang='6000'), follow_redirects=True)
            self.assertIn(b'Barang berhasil diedit!', response.data)
            barang = db.session.get(Barang, barang.kode_barang)
            self.assertEqual(barang.nama_barang, 'Buku Tulis')

    def test_hapus_barang(self):
        self.login()
        # Tambah barang dulu
        self.app.post('/barang/tambah', data=dict(nama_barang='Penghapus', harga_barang='1000'))
        with app.app_context():
            barang = Barang.query.filter_by(nama_barang='Penghapus').first()
            # Hapus barang
            response = self.app.get(f'/barang/hapus/{barang.kode_barang}', follow_redirects=True)
            self.assertIn(b'Barang berhasil dihapus!', response.data)
            barang = Barang.query.filter_by(nama_barang='Penghapus').first()
            self.assertIsNone(barang)

if __name__ == '__main__':
    unittest.main()