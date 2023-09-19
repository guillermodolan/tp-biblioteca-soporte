from flask import Flask, render_template, url_for, redirect, request, session
from flask_mail import Message, Mail
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import ObjectDeletedError, StaleDataError
from werkzeug.exceptions import NotFound
from data.database import Database
from entity_models.cliente_form import ClienteForm
from entity_models.cliente_model import Cliente
from logic.cliente_logic import ClienteLogic
from logic.libro_API_logic import LibroAPILogic


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Database.configura_conexion()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'konigari'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'konigari2023'
app.config['MAIL_PASSWORD'] = 'nrez dpvc rino mqjw'
app.config['MAIL_DEFAULT_SENDER'] = 'konigari2023@gmail.com'

mail = Mail(app)


Database.db.init_app(app)

migrate = Migrate()
migrate.init_app(app, Database.db)

@app.route('/')
@app.route('/inicio')
def inicio():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    cliente_data = session.get('cliente')
    if cliente_data:
        #cliente = Cliente.from_dict(cliente_data)
        return redirect(url_for('home'))

    elif request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        cliente = ClienteLogic.valida_credenciales(nombre_usuario, contraseña)
        if cliente:
            #Guardo al cliente en la sesión, para que se mueva por la página web sin necesidad
            #de loguearse a cada momento.
            session['cliente'] = cliente.to_dict()
            return render_template('home.html', clienteLogueado = cliente)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/home')
def home():
    #Al cliente que guardé en la sesión en el método login(), lo accedo desde este método, el cual
    #es para la página principal
    cliente_data = session.get('cliente')
    if cliente_data:
        cliente = Cliente.from_dict(cliente_data)
        return render_template('home.html', clienteLogueado = cliente)
    else:
        return redirect(url_for('login'))


#Ruta para manejar el cierre de sesión
@app.route('/logout')
def logout():
    #Elimino los datos de la sesión del cliente
    session.pop('cliente', None)
    return redirect(url_for('login'))



@app.route('/enviar_correo')
def enviar_correo():
    destinatario = 'eneasparatore@gmail.com'
    asunto = 'Prueba de mensaje'
    mensaje = 'Hi! Mr Eneas. I want you!'

    msg = Message(asunto, recipients=[destinatario])
    msg.body = mensaje

    try:
        mail.send(msg)
        return 'Correo electrónico enviado con éxito'
    except Exception as e:
        return f'Error al enviar el correo electrónico: {str(e)}'


@app.route('/get_all_clientes')
def get_all_clientes():
    clientes = ClienteLogic.get_all_clientes()
    return render_template('listado_clientes.html', clientesParam = clientes)
@app.route('/eliminar/<int:id>')
def delete_cliente(id):
    try:
        #El método delete_cliente(id) de la capa de lógica devuelve un mensaje de éxito
        mensaje = ClienteLogic.delete_cliente(id)
        return redirect(url_for('get_all_clientes'))
    except IntegrityError as e:
        raise e
    except ObjectDeletedError as e:
        raise e
    except StaleDataError as e:
        raise e
@app.route('/agregar_cliente', methods=['GET', 'POST'])
def add_cliente():
    cliente = Cliente()
    cliente_form = ClienteForm(obj=cliente)
    if request.method == 'POST':
        contraseña = request.form['contraseña']
        if cliente_form.validate_on_submit():
            Cliente.establece_contraseña(cliente, contraseña)
            cliente_form.populate_obj(cliente)
            ClienteLogic.add_cliente(cliente)
        return redirect(url_for('get_all_clientes'))
    return render_template('alta_cliente.html', cliente_agregar = cliente_form)
@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def update_cliente(id):
    try:
        cliente = ClienteLogic.get_one_cliente(id)
        cliente_form = ClienteForm(obj = cliente)
        if request.method == 'POST':
            if cliente_form.validate_on_submit():
                cliente_form.populate_obj(cliente)
                # El método update_cliente(id) de la capa de lógica devuelve un mensaje de éxito
                mensaje = ClienteLogic.update_cliente(cliente)
                return redirect(url_for('get_all_clientes'))
        return render_template('editar_cliente.html', cliente_editar = cliente_form)
    except NotFound as e:
        raise e





#Método que obtiene libros de una API, mediante un autor, que lo recibe como parámetro
@app.route('/libros/<autor>', methods=['GET'])
def get_libros_by_author(autor):
    libros = LibroAPILogic.get_libros_by_author(autor)
    if libros is not None:
        return render_template("libros_por_autor.html", librosPorAutor = libros)
    else:
        return "No se encontraron los libros"





#Esta ruta es la que lleva a la página para que un cliente pueda alquilar un libro
@app.route('/alquiler_libros')
def alquiler_libros():
    return render_template('alquiler_libros.html')


#MÉTODO INCOMPLETO. ESTARÁ TERMINADO CUANDO SE HAYA IMPLEMENTADO LA BÚSQUEDA POR GÉNERO.
#Método que se ejecuta cuando se busca un libro, ya sea por autor o por género,
#en el buscador ubicado en el archivo 'alquiler_libros.html'
@app.route('/busca_libros', methods=['POST'])
def busca_libros():
    if request.method == 'POST':
        busca = request.form['buscador']
        return redirect(url_for('get_libros_by_author', autor = busca))