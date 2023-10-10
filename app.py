import ast
from datetime import datetime, timedelta

from flask import Flask, render_template, url_for, redirect, request, session
from flask_mail import Message, Mail
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import ObjectDeletedError, StaleDataError
from werkzeug.exceptions import NotFound

from data.database import Database
from entity_models.cliente_form import ClienteForm
from entity_models.pedido_form import PedidoForm
from entity_models.categoria_form import CategoriaForm
from entity_models.libro_form import LibroForm
from entity_models.autor_form import AutorForm
from entity_models.cliente_model import Cliente
from entity_models.pedido_model import Pedido
from entity_models.categoria_model import Categoria
from entity_models.libro_model import Libro
from entity_models.autor_model import Autor
from logic.cliente_logic import ClienteLogic
from logic.libro_API_logic import LibroAPILogic
from logic.pedido_logic import PedidoLogic
from logic.categoria_logic import CategoriaLogic
from logic.libro_logic import LibroLogic
from logic.autor_logic import AutorLogic

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Database.configura_conexion()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'konigari'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'konigari2023'
app.config['MAIL_PASSWORD'] = 'nrez dpvc rino mqjw'
app.config['MAIL_DEFAULT_SENDER'] = 'konigari2023@gmail.com'

# Configuración para implementar el carrito de pedidos
# Cada elemento será un diccionario con información del libro
app.config['CARRITO'] = []

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
        return redirect(url_for('home'))

    elif request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        cliente = ClienteLogic.valida_credenciales(nombre_usuario, contraseña)
        if cliente:
            # Guardo al cliente en la sesión, para que se mueva por la página web sin necesidad
            # de loguearse a cada momento.
            session['cliente'] = cliente.to_dict()
            return render_template('home.html', clienteLogueado=cliente)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/home')
def home():
    # Al cliente que guardé en la sesión en el método login(), lo accedo desde este método, el cual
    # es para la página principal
    cliente_data = session.get('cliente')
    if cliente_data:
        cliente = Cliente.from_dict(cliente_data)
        return render_template('home.html', clienteLogueado=cliente)
    else:
        return redirect(url_for('login'))


# Ruta para manejar el cierre de sesión
@app.route('/logout')
def logout():
    # Elimino los datos de la sesión del cliente
    session.pop('cliente', None)
    # Elimino el carrito
    app.config['CARRITO'] = []
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
    return render_template('listado_clientes.html', clientesParam=clientes)


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
    return render_template('alta_cliente.html', cliente_agregar=cliente_form)


@app.route('/eliminar/<int:id>')
def delete_cliente(id):
    try:
        ClienteLogic.delete_cliente(id)
        return redirect(url_for('get_all_clientes'))
    except IntegrityError as e:
        raise e
    except ObjectDeletedError as e:
        raise e
    except StaleDataError as e:
        raise e


@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def update_cliente(id):
    try:
        cliente = ClienteLogic.get_one_cliente(id)
        cliente_form = ClienteForm(obj=cliente)
        if request.method == 'POST':
            if cliente_form.validate_on_submit():
                cliente_form.populate_obj(cliente)
                # El método update_cliente(id) de la capa de lógica devuelve un mensaje de éxito
                mensaje = ClienteLogic.update_cliente(cliente)
                return redirect(url_for('get_all_clientes'))
        return render_template('editar_cliente.html', cliente_editar=cliente_form)
    except NotFound as e:
        raise e


@app.route('/libros/<autor>', methods=['GET'])
def get_libros_by_author(autor):
    libros = LibroAPILogic.get_libros_by_author(autor)
    carrito = app.config['CARRITO']
    # Agregar una bandera 'en_carrito' a cada libro para indicar si está en el carrito o no
    for libro in libros:
        libro['en_carrito'] = any(item['titulo'] == libro['titulo'] for item in carrito)
    if libros is not None:
        return render_template("libros_por_autor.html", librosPorAutor=libros, carrito_de_pedidos=carrito)


@app.route('/libros/genre/<genero>', methods=['GET'])
def get_libros_by_genre(genero):
    libros = LibroAPILogic.get_libros_by_genre(genero)
    if libros is not None:
        return render_template("libros_por_genero.html", librosPorGenero=libros)
    else:
        return "No se encontraron libros para este género"


@app.route('/alquiler_libros')
def alquiler_libros():
    return render_template('alquiler_libros.html')


@app.route('/busca_libros', methods=['GET', 'POST'])
def busca_libros():
    if request.method == 'POST':
        busca = request.form['buscador']
        opcion = request.form['opcion']
        if opcion == 'autor':
            return redirect(url_for('get_libros_by_author', autor=busca))
        elif opcion == 'genero':
            return redirect(url_for('get_libros_by_genre', genero=busca))
    else:
        return render_template('alquiler_libros.html')


@app.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    libro = request.form['libro']
    libro_info = ast.literal_eval(libro)

    # Acceder a los atributos
    titulo = libro_info['titulo']
    autores = libro_info['autores']
    isbn = libro_info['isbn']

    # Agrego el libro al carrito de pedidos
    app.config['CARRITO'].append({'titulo': titulo, 'autores': autores, 'isbn': isbn})
    return redirect(url_for('mostrar_carrito'))


@app.route('/eliminar_del_carrito/<titulo>')
def eliminar_libro_carrito(titulo):
    # Encuentra el índice del libro en el carrito por su título
    index_to_remove = None
    for i, libro in enumerate(app.config['CARRITO']):
        if libro['titulo'] == titulo:
            index_to_remove = i
            libro_a_remover = LibroLogic.get_libros_by_titulo(titulo)
            # Verifico que el libro exista en la base de datos
            if libro_a_remover is None:
                lib = Libro()
                lib.titulo = libro['titulo']
                lib.existencia = True
                lib.isbn = libro['isbn']
                LibroLogic.add_libro(lib)
                print(f'Título: {lib.titulo}')
            else:
                libro_a_remover.existencia = True
                LibroLogic.update_existencia()
            break

    # Si se encontró el libro, elimínalo del carrito
    if index_to_remove is not None:
        app.config['CARRITO'].pop(index_to_remove)

    return redirect(url_for('mostrar_carrito'))


# Ruta para mostrar el carrito de pedidos de un cliente
@app.route('/carrito')
def mostrar_carrito():
    carrito = app.config['CARRITO']
    return render_template('carrito_de_pedidos.html', carrito_de_pedidos=carrito)


@app.route('/confirmar_pedido', methods=['POST'])
def confirmar_pedido():
    if request.method == 'POST':
        carrito = app.config['CARRITO']
        for elem in carrito:
            # PARTE DE VALIDACIÓN
            # Verifico que los libros que están en el carrito no estén creados en la base de datos
            libro_buscado = LibroLogic.get_libros_by_titulo(elem['titulo'])
            if libro_buscado is None:
                libro = Libro()
                libro.titulo = elem['titulo']
                libro.existencia = True
                libro.isbn = elem['isbn']
                LibroLogic.add_libro(libro)
        for elem in carrito:
            pedido = Pedido()
            # PARTE DE VALIDACIÓN
            # Por regla de negocio 3 en el documento 'Narrativa TPI', validamos que el libro que
            # se quiere alquilar no esté ya alquilado.
            libro_con_existencia = LibroLogic.valida_existencia_libro(elem['titulo'])

            if libro_con_existencia is not None:
                pedido.id_libro = libro_con_existencia.id_libro
                # Cambio la existencia del libro a False dado que se está por alquilar
                libro_con_existencia.existencia = False
                pedido.estado = True
                # Obtener la fecha del día en formato datetime
                fecha_actual = datetime.now()
                # Convertir la fecha a una cadena (string) en un formato específico
                fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')

                # Agrega 7 días a la fecha actual
                fecha_devolucion = fecha_actual + timedelta(days=7)
                fecha_devolucion_str = fecha_devolucion.strftime('%Y-%m-%d')

                pedido.fecha_pedido = fecha_actual_str
                pedido.fecha_devolucion = fecha_devolucion_str

                # Agrego el id del cliente al pedido
                cliente_data = session.get('cliente')
                cliente_id = cliente_data.get('id_cliente')
                pedido.id_cliente = cliente_id
                PedidoLogic.add_pedido(pedido)
        return 'Pedido realizado exitosamente'
    else:
        return ''
