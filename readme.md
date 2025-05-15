# Flask CRUD App

Aplikasi CRUD sederhana berbasis Flask untuk manajemen Barang dan Transaksi, dilengkapi autentikasi user, validasi, notifikasi SweetAlert, dan pengujian unit test.

## Fitur

- **Autentikasi User**: Login, register, dan logout.
- **CRUD Barang**: Tambah, edit (dengan modal), hapus, dan daftar barang dengan paginasi.
- **CRUD Transaksi**: Tambah, edit (dengan modal), hapus, dan daftar transaksi dengan paginasi.
- **Validasi Input**: Validasi backend untuk semua form.
- **Notifikasi SweetAlert**: Feedback sukses/gagal dengan SweetAlert.
- **Unit Test**: Pengujian otomatis untuk fitur CRUD barang.
- **Responsive UI**: Menggunakan Bootstrap 5.

## Instalasi

1. **Clone repo**
   ```sh
   git clone https://github.com/cornfuze/Flask-CRUD.git
   cd Flask-CRUD

2. **Buat virtual environment & install dependencies**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install flask flask_sqlalchemy flask_login werkzeug
   ```

3. **Jalankan aplikasi**
   ```sh
   python app.py
   ```

4. **Akses di browser**
   ```
   http://localhost:5000
   ```

## Struktur Folder

```
├── app.py
├── models.py
├── test_app.py
├── templates/
│   ├── base.html.j2
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── barang/
│   │   └── list.html
│   └── transaksi/
│       └── list.html
├── .gitignore
├── readme.md
```

## Pengujian

Jalankan unit test:
```sh
python test_app.py
```

## Catatan

- File database (`database.db`) otomatis dibuat saat pertama kali dijalankan.
- File dan folder seperti `.venv/`, `__pycache__/`, dan file database sudah diabaikan oleh `.gitignore`.
