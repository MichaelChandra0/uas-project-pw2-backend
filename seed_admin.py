from main import app
from models import Admin, db

with app.app_context():
    admin = [
        Admin(username="dervin", password="12345678"),
        Admin(username="fachtur", password="12345678"),
        Admin(username="michael", password="12345678"),
    ]

    db.session.add_all(admin)
    db.session.commit()

    print("Berhasil menambahkan data admin")
