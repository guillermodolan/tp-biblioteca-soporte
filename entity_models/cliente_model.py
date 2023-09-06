from werkzeug.security import generate_password_hash, check_password_hash
from data.database import Database

db = Database.db

#Defino una clase de modelo. Esta clase para que se considere una clase de modelo,
#vamos a utilizar nuestro objeto 'db', y vamos a extender de la clase Model
class Cliente(db.Model):
    id_cliente = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(150))
    apellido = db.Column(db.String(150))
    email = db.Column(db.String(100))
    nombre_usuario = db.Column(db.String(80), nullable = False)
    contraseña = db.Column(db.Text, nullable = False)
    telefono = db.Column(db.String(25))
    usuario_telegram = db.Column(db.String(50))

    def establece_contraseña(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def valida_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)