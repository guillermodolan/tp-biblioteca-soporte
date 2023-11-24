from werkzeug.security import generate_password_hash, check_password_hash

from data.database import Database

db = Database.db


class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150))
    apellido = db.Column(db.String(150))
    email = db.Column(db.String(100))
    nombre_usuario = db.Column(db.String(80), nullable=False)
    contraseña = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(25))
    tipo_persona = db.Column(db.String(40))

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'nombre_usuario': self.nombre_usuario,
            'contraseña': self.contraseña,
            'telefono': self.telefono,
            'tipo_persona': self.tipo_persona
        }

    # Método usado para deserializar el objeto JSON, y convertirlo a Cliente
    @classmethod
    def from_dict(cls, data):
        persona = cls()
        persona.id = data['id']
        persona.nombre = data['nombre']
        persona.apellido = data['apellido']
        persona.email = data['email']
        persona.nombre_usuario = data['nombre_usuario']
        persona.contraseña = data['contraseña']
        persona.telefono = data['telefono']
        persona.tipo_persona = data['tipo_persona']
        return persona

    def establece_contraseña(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def valida_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)
