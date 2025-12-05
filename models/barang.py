from models.extension import db
from datetime import datetime, timezone


class Barang(db.Model):
    kode_barang = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(80), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    jumlah_stok = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    kondisi = db.Column(db.String(50), nullable=False)
    deskripsi_barang = db.Column(db.String(255), nullable=False)
    foto_barang = db.Column(db.String(255), nullable=False)
    tanggal = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def to_json(self):
        return {
            "kode_barang": self.kode_barang,
            "nama_barang": self.nama_barang,
            "kategori": self.kategori,
            "jumlah_stok": self.jumlah_stok,
            "harga": self.harga,
            "kondisi": self.kondisi,
            "deskripsi_barang": self.deskripsi_barang,
            "foto_barang": self.foto_barang,
            "tanggal": self.tanggal,
        }
