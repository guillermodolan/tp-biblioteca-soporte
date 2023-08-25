from flask import Flask, render_template, url_for, redirect, request
from flask_migrate import Migrate
from data.database import Database
from entity_models.cliente_form import ClienteForm
from entity_models.cliente_model import Cliente
from logic.cliente_logic import ClienteLogic


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/get_all_clientes.html')
def get_all_clientes():
    clientes = ClienteLogic.get_all_clientes()
    return render_template('get_all_clientes.html', clientesParam = clientes)

@app.route('/eliminar/<int:id>')
def delete_cliente(id):
    ClienteLogic.delete_cliente(id)
    return redirect(url_for('get_all_clientes'))

@app.route('/agregar_cliente', methods=['GET', 'POST'])
def add_cliente():
    cliente = Cliente()
    cliente_form = ClienteForm(obj = cliente)
    if request.method == 'POST':
        if cliente_form.validate_on_submit():
            cliente_form.populate_obj(cliente)
            ClienteLogic.add_cliente(cliente)
        return redirect(url_for('get_all_clientes'))
    return render_template('alta_cliente.html', cliente_agregar = cliente_form)