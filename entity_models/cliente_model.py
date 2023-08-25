from data.database import Database

db = Database.db

#Defino una clase de modelo. Esta clase para que se considere una clase de modelo,
#vamos a utilizar nuestro objeto 'db', y vamos a extender de la clase Model
class Cliente(db.Model):
    id_cliente = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(150))
    apellido = db.Column(db.String(150))
    email = db.Column(db.String(100))
    nombre_usuario = db.Column(db.String(60))
    contraseña = db.Column(db.String(25))
    telefono = db.Column(db.String(25))
    usuario_telegram = db.Column(db.String(50))