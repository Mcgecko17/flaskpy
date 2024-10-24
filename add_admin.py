from werkzeug.security import generate_password_hash
from todor import create_app, db
from todor.models import Admin

app = create_app()

with app.app_context():
    # Crear un nuevo administrador
    new_admin = Admin(username='augustosanchezcopa', password=generate_password_hash('13093507'))
    db.session.add(new_admin)
    db.session.commit()
    print('Administrador añadido con éxito.')