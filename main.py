from flask import Flask, jsonify, request
from cloudinary_config import cloudinary
from models import Barang, db, Riwayat, Admin
from functools import wraps
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
    # db.drop_all()
    db.create_all()


@app.route("/")
def main():
    return "API SEDANG BERJALAN! latest 7 dec 2025"


# MIDDLEWARE CEK API KEY


def cek_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if api_key != Config.SECRET_API_KEY:
            return jsonify({"error": "API KEY tidak valid"})
        return f(*args, **kwargs)

    return decorated


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
        kode_barang=request.form.get("kode_barang"),
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
    riwayat_baru = Riwayat(
        kode_barang=barang_baru.kode_barang,
        nama_barang=request.form.get("nama_barang"),
        kategori=request.form.get("kategori"),
        jumlah_stok=request.form.get("jumlah_stok"),
        harga=request.form.get("harga"),
        kondisi=request.form.get("kondisi"),
        deskripsi_barang=request.form.get("deskripsi_barang"),
        status="Masuk",
        foto_barang=foto_url,
    )
    db.session.add(riwayat_baru)
    db.session.commit()
    return jsonify(barang_baru.to_json()), 201


# EDIT BARANG
@app.route("/api/barang/<int:id>", methods=["PUT"])
def edit_barang(id):

    barang = Barang.query.get(id)
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
@app.route("/api/barang/<int:id>", methods=["DELETE"])
def delete_barnag(id):
    barang = Barang.query.get(id)
    if barang:
        db.session.delete(barang)
        db.session.commit()
        return jsonify({"message": "Barang berhasil dihapus"})
    return jsonify({"message": "Barang tidak ada"})


# CRUD RIWAYAT
# GET RIWAYAT
@app.route("/api/riwayat")
def get_riwayat():
    riwayat = Riwayat.query.all()
    return jsonify([r.to_json() for r in riwayat])


# # CREATE RIWAYAT
# @app.route("/api/riwayat", methods=["POST"])
# def create_riwayat():
#     foto_url = None
#     if "foto_barang" in request.files:
#         file = request.files["foto_barang"]
#         link_cloudinary = upload(
#             file, folder="riwayat", use_filename=True, unique_filename=False
#         )
#         foto_url = link_cloudinary["secure_url"]

#     riwayat_baru = Riwayat(
#         nama_barang=request.form.get("nama_barang"),
#         kategori=request.form.get("kategori"),
#         jumlah_stok=request.form.get("jumlah_stok"),
#         harga=request.form.get("harga"),
#         kondisi=request.form.get("kondisi"),
#         deskripsi_barang=request.form.get("deskripsi_barang"),
#         status="Masuk",
#         foto_barang=foto_url,
#     )
#     db.session.add(riwayat_baru)
#     db.session.commit()
#     return jsonify(riwayat_baru.to_json()), 201


# UPDATE RIWAYAT (Masuk Barang)
@app.route("/api/riwayat/masuk/<int:id>", methods=["POST"])
def masuk_barang(id):
    riwayat = Barang.query.get(id)
    masuk = int(request.form.get("masuk", 0))
    if riwayat:
        riwayat_baru = Riwayat(
            kode_barang=riwayat.kode_barang,
            nama_barang=riwayat.nama_barang,
            kategori=riwayat.kategori,
            jumlah_stok=masuk + riwayat.jumlah_stok,
            harga=riwayat.harga,
            kondisi=riwayat.kondisi,
            deskripsi_barang=riwayat.deskripsi_barang,
            foto_barang=riwayat.foto_barang,
            status="Masuk",
        )
    db.session.add(riwayat_baru)
    db.session.commit()
    return jsonify(riwayat.to_json()), 200


# UPDATE RIWAYAT (Keluar Barang)
@app.route("/api/riwayat/keluar/<int:id>", methods=["POST"])
def keluar_barang(id):
    riwayat = Barang.query.get(id)
    # kode_barang = barang.kode_barang
    # riwayat = Riwayat.query.get(kode_barang)
    if riwayat:
        keluar = int(request.form.get("keluar", 0))
        riwayat_baru = Riwayat(
            kode_barang=riwayat.kode_barang,
            nama_barang=riwayat.nama_barang,
            kategori=riwayat.kategori,
            jumlah_stok=riwayat.jumlah_stok - keluar,
            harga=riwayat.harga,
            kondisi=riwayat.kondisi,
            deskripsi_barang=riwayat.deskripsi_barang,
            foto_barang=riwayat.foto_barang,
            status="Keluar",
        )
    db.session.add(riwayat_baru)
    db.session.commit()
    return jsonify(riwayat.to_json()), 200


@app.route("/api/admin")
def admin():
    admin = Admin.query.all()


if __name__ == "__main__":
    app.run(debug=True)
