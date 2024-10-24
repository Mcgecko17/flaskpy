from todor import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_approved = db.Column(db.Boolean, default=False, nullable=False) 
    
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_approved = False
    
    
    def __repr__(self):
        return f'<User {self.username}>'
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'<Admin {self.username}>'
    
class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    codigo = db.Column(db.String(80), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    
    def __init__(self, nombre,codigo, cantidad, precio):
        self.nombre = nombre
        self.codigo = codigo
        self.cantidad = cantidad
        self.precio = precio
    
    def __repr__(self):
        return f'<Inventario {self.nombre}>'