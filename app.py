from flask import Flask, render_template, url_for, redirect, request, session
from flask_migrate import Migrate
from data.database import Database
from entity_models.cliente_form import ClienteForm
from entity_models.cliente_model import Cliente
from entity_models.login_form import LoginForm
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


@app.route('/', methods=['GET', 'POST'])
def inicio():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            cliente = ClienteLogic.get_cliente_by_user(login_form.nombre_usuario, login_form.contrasenia)
            app.logger.debug(f'Nombre de usuario: {cliente.nombre_usuario}')
            app.logger.debug(f'Contraseña: {cliente.contraseña}')
        # ACA SE VA A LANZAR LA EXCEPCIÓN EN CASO DE QUE FALLE
            #return render_template('listado_clientes.')
    return "nada"



@app.route('/get_all_clientes')
def get_all_clientes():
    clientes = ClienteLogic.get_all_clientes()
    return render_template('listado_clientes.html', clientesParam = clientes)

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

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def update_cliente(id):
    cliente = ClienteLogic.get_one_cliente(id)
    cliente_form = ClienteForm(obj = cliente)

    if request.method == 'POST':
        if cliente_form.validate_on_submit():
            cliente_form.populate_obj(cliente)
            ClienteLogic.update_cliente(cliente)
            return redirect(url_for('get_all_clientes'))
    return render_template('editar_cliente.html', cliente_editar = cliente_form)