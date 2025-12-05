from flask import Flask, jsonify, request
from cloudinary_config import cloudinary
from models import Barang, db, Riwayat

from flask_cors import CORS
from config import Config
import os
from cloudinary.uploader import upload


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

UPLOAD_FOLDER = os.path.join(app.root_path, "static/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

with app.app_context():
    db.create_all()


@app.route("/")
def main():
    return "API SEDANG BERJALAN!"


# CRUD BARANG
# GET BARANG
@app.route("/api/barang")
def get_barang():
    barang = Barang.query.all()
    print("cloud name : ", cloudinary.config().cloud_name)
    print("hello world")
    return jsonify([b.to_json() for b in barang])


# CREATE BARANG
@app.route("/api/barang", methods=["POST"])
def create_barang():
    foto_url = None
    if "foto_barang" in request.files:
        file = request.files["foto_barang"]
        link_cloudinary = upload(
            file, folder="barang", use_filename=True, unique_filename=False
        )
        foto_url = link_cloudinary["secure_url"]

    barang_baru = Barang(
        nama_barang=request.form.get("nama_barang"),
        kategori=request.form.get("kategori"),
        jumlah_stok=request.form.get("jumlah_stok"),
        harga=request.form.get("harga"),
        kondisi=request.form.get("kondisi"),
        deskripsi_barang=request.form.get("deskripsi_barang"),
        foto_barang=foto_url,
    )
    db.session.add(barang_baru)
    db.session.commit()
    return jsonify(barang_baru.to_json()), 201


# EDIT BARANG
@app.route("/api/barang/<int:kode_barang>", methods=["PUT"])
def edit_barang(kode_barang):

    barang = Barang.query.get(kode_barang)
    if barang:

        barang.nama_barang = request.form.get("nama_barang", barang.nama_barang)
        barang.kategori = request.form.get("kategori", barang.kategori)
        barang.jumlah_stok = request.form.get("jumlah_stok", barang.jumlah_stok)
        barang.harga = request.form.get("harga", barang.harga)
        barang.kondisi = request.form.get("kondisi", barang.kondisi)
        barang.deskripsi_barang = request.form.get(
            "deskripsi_barang", barang.deskripsi_barang
        )
        barang.foto_barang = request.form.get("foto_barang", barang.foto_barang)

        if "foto_barang" in request.files:
            file = request.files["foto_barang"]
            link_cloudinary = upload(
                file, folder="barang", use_filename=True, unique_filename=False
            )
            barang.foto_barang = link_cloudinary["secure_url"]
    db.session.commit()

    return jsonify(barang.to_json()), 200


# DELETE BARANG
@app.route("/api/barang/<int:kode_barang>", methods=["DELETE"])
def delete_barnag(kode_barang):
    barang = Barang.query.get(kode_barang)
    if barang:
        db.session.delete(barang)
        db.session.commit()
        return jsonify({"message": "Barang berhasil dihapus"})
    return jsonify({"message": "Barang tidak ada"})


@app.route("/api/riwayat")
def get_riwayat():
    riwayat = Riwayat.query.all()
    return jsonify([r.to_json() for r in riwayat])


if __name__ == "__main__":
    app.run(debug=True)
