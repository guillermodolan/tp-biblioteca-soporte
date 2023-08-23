from flask import Flask, render_template
from flask_migrate import Migrate
from database import Database
from data_cliente import DataCliente


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Database.configura_conexion()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'konigari'


Database.db.init_app(app)


#######################CONFIGURACIÓN FLASK MIGRATE################################################
#Agreo la configuración de Flask Migrate para que podamos realizar las migraciones, y
#se pueda crear el mapeo de la clase Persona (desarrollada más abajo) hacia la
#tabla de base de datos que se debe de crear

#1- Creo un objeto Migrate
migrate = Migrate()
#2- Inicializo el objeto migrate. Le paso los valores de app, y db
migrate.init_app(app, Database.db)
#######################CONFIGURACIÓN FLASK MIGRATE################################################


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def get_all_clientes():
    clientes = DataCliente.get_all_clientes()
    return render_template('index.html', clientesParam = clientes)