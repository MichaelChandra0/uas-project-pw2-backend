from main import app
from models import Barang, db
from datetime import datetime

with app.app_context():
    db.drop_all()
    db.create_all()

    dummy_barang = [
        Barang(
            nama_barang="CAT MINYAK",
            kategori="Peralatan",
            jumlah_stok=45,
            harga=17500,
            kondisi="Baru",
            deskripsi_barang="Cat minyak untuk cat besi, dll",
            foto_barang="https://img.lazcdn.com/g/p/55f861a6c746f27d17ab97490e38c116.jpg_720x720q80.jpg",
            tanggal=datetime(2025, 12, 5, 11, 0),
        )
    ]

    db.session.add_all(dummy_barang)
    db.session.commit()

    print("Berhasil menambahkan data dummy")
