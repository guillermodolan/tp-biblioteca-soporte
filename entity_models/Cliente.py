from werkzeug.security import check_password_hash, generate_password_hash


class Cliente():
    def __init__(self, id_cliente, nombre, apellido, email, nombre_usuario, contraseña,
                telefono, usuario_telegram):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.telefono = telefono
        self.usuario_telegram = usuario_telegram

    def establece_contraseña(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def valida_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)