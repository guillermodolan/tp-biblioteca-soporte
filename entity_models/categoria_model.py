from data.database import Database
db = Database.db

#Defino una clase de modelo. Esta clase para que se considere una clase de modelo,
#vamos a utilizar nuestro objeto 'db', y vamos a extender de la clase Model
class Categoria(db.Model):
    id_categoria = db.Column(db.Integer, primary_key = True)
    descripcion = db.Column(db.String(100))