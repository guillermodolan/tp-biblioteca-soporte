import ast
from datetime import datetime, timedelta

from flask import Flask, render_template, url_for, redirect, request, session
from flask_mail import Message, Mail
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import ObjectDeletedError, StaleDataError
from werkzeug.exceptions import NotFound
from data.database import Database
from entity_models.persona_model import Persona
from entity_models.registro_form import RegistroForm
from entity_models.pedido_form import PedidoForm
from entity_models.categoria_form import CategoriaForm
from entity_models.libro_form import LibroForm
from entity_models.autor_form import AutorForm
from entity_models.libro_autor_model import LibroAutor
from entity_models.persona_model import Persona
from entity_models.pedido_model import Pedido
from entity_models.categoria_model import Categoria
from entity_models.libro_model import Libro
from entity_models.autor_model import Autor
from graphics.autores_mas_leidos_en_un_mes import AutorMasLeidoEnUnMesGrafico
from logic.libro_API_logic import LibroAPILogic
from logic.libro_autor_logic import LibroAutorLogic
from logic.pedido_logic import PedidoLogic
from logic.categoria_logic import CategoriaLogic
from logic.libro_logic import LibroLogic
from logic.autor_logic import AutorLogic
from logic.persona_logic import PersonaLogic

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
    persona_data = session.get('persona_logueda')
    if persona_data:
        return redirect(url_for('home'))

    elif request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        persona = PersonaLogic.valida_credenciales(nombre_usuario, contraseña)
        if persona:
            # Guardo a la persona en la sesión, para que se mueva por la página web sin necesidad
            # de loguearse a cada rato.
            session['persona_logueda'] = persona.to_dict()
            return render_template('home.html', persona_logueda=persona)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/home')
def home():
    # A la persona que guardé en la sesión en el método login(), lo accedo desde este método, el cual
    # es para la página principal
    persona_data = session.get('persona_logueda')
    if persona_data:
        persona = Persona.from_dict(persona_data)
        return render_template('home.html', persona_logueda=persona)
    else:
        return redirect(url_for('login'))


# Ruta para manejar el cierre de sesión
@app.route('/logout')
def logout():
    # Elimino los datos de la sesión de la persona
    session.pop('persona_logueda', None)
    # Elimino el carrito
    app.config['CARRITO'] = []
    return redirect(url_for('login'))


@app.route('/enviar_correo_dos_dias_antes')
def enviar_correo_dos_dias_antes():
    today = datetime.now()
    two_days_from_now = today + timedelta(days=2)
    two_days_from_now_str = two_days_from_now.strftime('%Y-%m-%d')

    pedidos_a_enviar = PedidoLogic.get_pedidos_2_dias_de_devolucion(two_days_from_now_str)

    for pedido in pedidos_a_enviar:
        persona = Persona.query.get(pedido.id_persona)

        # Crea el mensaje del correo
        asunto = 'Recordatorio de devolución'
        mensaje = 'Recuerda que tu libro debe devolverse en dos días. Gracias por tu preferencia.'
        msg = Message(asunto, recipients=[persona.email])
        msg.body = mensaje

        # Envía el correo
        mail.send(msg)
    return render_template('mensaje.html', mensaje='Correo enviado')


@app.route('/get_all_personas')
def get_all_personas():
    personas = PersonaLogic.get_all_personas()
    return render_template('listado_personas.html', personas_param=personas)


@app.route('/historial_libros')
def historial_libros():
    persona_data = session.get('persona_logueda')
    if persona_data:
        persona = Persona.from_dict(persona_data)
        pedidos = PedidoLogic.get_pedidos_by_persona(persona)
        a_devolver = []
        devueltos = []
        lib_a_dev = []
        lib_dev = []
        aut_a_dev = []
        aut_dev = []
        cat_a_dev = []
        cat_dev = []
        for pedido in pedidos:
            libro = LibroLogic.get_one_libro(pedido.id_libro)
            libro_autor = LibroAutorLogic.get_libro_autor(pedido.id_libro)
            autor = Autor()
            for lib_aut in libro_autor:
                autor = AutorLogic.get_one_autor(lib_aut.id_autor)
            categoria = CategoriaLogic.get_one_categoria(libro.id_categoria)
            if pedido.estado:
                a_devolver.append(pedido)
                lib_a_dev.append(libro)
                aut_a_dev.append(autor)
                cat_a_dev.append(categoria)
            else:
                devueltos.append(pedido)
                lib_dev.append(libro)
                aut_dev.append(autor)
                cat_dev.append(categoria)
        rango_a_dev = range(len(a_devolver))
        rango_dev = range(len(devueltos))
        return render_template('libros_cliente.html', pedADevolver=a_devolver, pedDevueltos=devueltos,
                               libADevolver=lib_a_dev, libDevueltos=lib_dev,
                               autADevolver=aut_a_dev, autDevueltos=aut_dev,
                               catADevolver=cat_a_dev, catDevueltos=cat_dev,
                               rangoADevolver=rango_a_dev, rangoDevueltos=rango_dev)
    else:
        return redirect(url_for('login'))


@app.route('/eliminar_persona/<int:id>')
def delete_persona(id):
    try:
        PersonaLogic.delete_persona(id)
        return redirect(url_for('get_all_personas'))
    except IntegrityError as e:
        raise e
    except ObjectDeletedError as e:
        raise e
    except StaleDataError as e:
        raise e


@app.route('/agregar_persona', methods=['GET', 'POST'])
def add_persona():
    persona = Persona()
    registro_form = RegistroForm(obj=persona)
    if request.method == 'POST':
        contraseña = request.form['contraseña']
        if registro_form.validate_on_submit():
            Persona.establece_contraseña(persona, contraseña)
            registro_form.populate_obj(persona)
            PersonaLogic.add_persona(persona)
        return redirect(url_for('get_all_personas'))
    return render_template('alta_persona.html', persona_agregar=registro_form)


@app.route('/editar_persona/<int:id>', methods=['GET', 'POST'])
def update_persona(id):
    try:
        persona = PersonaLogic.get_one_persona(id)
        registro_form = RegistroForm(obj=persona)
        if request.method == 'POST':
            if registro_form.validate_on_submit():
                registro_form.populate_obj(persona)
                # El método update_cliente(id) de la capa de lógica devuelve un mensaje de éxito
                mensaje = PersonaLogic.update_persona(persona)
                return redirect(url_for('get_all_personas'))
        return render_template('editar_persona.html', persona_editar=registro_form)
    except NotFound as e:
        raise e


@app.route('/libros/<autor>', methods=['GET'])
def get_libros_by_author(autor):
    libros = LibroAPILogic.get_libros_by_author(autor)
    carrito = app.config['CARRITO']
    cant_libros_carrito = len(carrito)

    # Obtener la persona actual
    persona_data = session.get('persona_logueda')
    persona = Persona.from_dict(persona_data)

    # Obtener pedidos realizados por el cliente con estado True
    pedidos_realizados = PedidoLogic.get_pedidos_by_persona(persona)

    cant_pedidos_realizados = 0

    for ped in pedidos_realizados:
        if ped.estado:
            cant_pedidos_realizados = cant_pedidos_realizados + 1

    total_libros = cant_libros_carrito + cant_pedidos_realizados

    # Agregar una bandera 'en_carrito' a cada libro para indicar si está en el carrito o no
    for libro in libros:
        libro['en_carrito'] = any(item['titulo'] == libro['titulo'] for item in carrito)
    if libros is not None:
        return render_template("libros_por_autor.html", librosPorAutor=libros, carrito_de_pedidos=carrito,
                               cant_pedidos_cliente=total_libros)


@app.route('/libros/genre/<genero>', methods=['GET'])
def get_libros_by_genre(genero):
    libros = LibroAPILogic.get_libros_by_genre(genero)
    carrito = app.config['CARRITO']

    cant_libros_carrito = len(carrito)

    # Obtener la persona actual
    persona_data = session.get('persona_logueda')
    persona = Persona.from_dict(persona_data)

    # Obtener pedidos realizados por el cliente con estado True
    pedidos_realizados = PedidoLogic.get_pedidos_by_persona(persona)

    cant_pedidos_realizados = 0

    for ped in pedidos_realizados:
        if ped.estado:
            cant_pedidos_realizados = cant_pedidos_realizados + 1

    total_libros = cant_libros_carrito + cant_pedidos_realizados

    # Agregar una bandera 'en_carrito' a cada libro para indicar si está en el carrito o no
    for libro in libros:
        libro['en_carrito'] = any(item['titulo'] == libro['titulo'] for item in carrito)
    if libros is not None:
        return render_template("libros_por_genero.html", librosPorGenero=libros, carrito_de_pedidos=carrito,
                               cant_pedidos_cliente=total_libros)


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
    categoria = libro_info['categoria']
    isbn = libro_info['isbn']

    # Agrego el libro al carrito de pedidos
    app.config['CARRITO'].append({'titulo': titulo, 'autores': autores, 'categoria': categoria, 'isbn': isbn})
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


@app.route('/carrito')
def mostrar_carrito():
    carrito = app.config['CARRITO']
    cant_libros_carrito = len(carrito)

    # Obtener el cliente actual
    persona_data = session.get('persona_logueda')
    persona = Persona.from_dict(persona_data)

    # Obtener pedidos realizados por el cliente con estado True
    pedidos_realizados = PedidoLogic.get_pedidos_by_persona(persona)

    cant_pedidos_realizados = 0

    for ped in pedidos_realizados:
        if ped.estado:
            cant_pedidos_realizados = cant_pedidos_realizados + 1

    total_libros = cant_libros_carrito + cant_pedidos_realizados

    return render_template('carrito_de_pedidos.html', carrito_de_pedidos=carrito, cant_libros_totales=total_libros)


@app.route('/confirmar_pedido', methods=['POST'])
def confirmar_pedido():
    if request.method == 'POST':
        libro_autor = LibroAutor()
        carrito = app.config['CARRITO']
        for elem in carrito:
            # PARTE DE VALIDACIÓN
            libro = Libro()
            categoria_buscada = CategoriaLogic.get_categoria_by_desc(str(elem['categoria']).strip("[]'"))
            if categoria_buscada is None:
                categoria = Categoria()
                categoria.descripcion = str(elem['categoria']).strip("[]'")
                CategoriaLogic.add_categoria(categoria)

                categoria_a_relacionar = CategoriaLogic.get_categoria_by_desc((str(elem['categoria']).strip("[]'")))
                if categoria_a_relacionar is not None:
                    libro.id_categoria = categoria_a_relacionar.id_categoria
            else:
                libro.id_categoria = categoria_buscada.id_categoria
            # Verifico que los libros que están en el carrito no estén creados en la base de datos
            libro_buscado = LibroLogic.get_libros_by_titulo(elem['titulo'])
            if libro_buscado is None:
                libro.titulo = elem['titulo']
                libro.existencia = True
                libro.isbn = elem['isbn']
                LibroLogic.add_libro(libro)
                # Busco el libro que se creó en la base de datos, para guardar su id
                # en la relacion Libro_Autor
                libro_a_relacionar = LibroLogic.get_libros_by_titulo(elem['titulo'])
                # Valido que exista el libro que se acaba de crear en la base de datos
                if libro_a_relacionar is not None:
                    libro_autor.id_libro = libro_a_relacionar.id_libro
            else:
                libro_autor.id_libro = libro_buscado.id_libro
            autor_buscado = AutorLogic.get_author_by_name(str(elem['autores']).strip("[]'"))
            if autor_buscado is None:
                autor = Autor()
                autor.nombre = str(elem['autores']).strip("[]'")
                AutorLogic.add_autor(autor)
                # Busco el autor que se creó en la base de datos, para guardar su id
                # en la relacion Libro_Autor
                autor_a_relacionar = AutorLogic.get_author_by_name(str(elem['autores']).strip("[]'"))
                # Valido que exista el autor que se acaba de crear en la base de datos
                if autor_a_relacionar is not None:
                    libro_autor.id_autor = autor_a_relacionar.id_autor
            else:
                libro_autor.id_autor = autor_buscado.id_autor
            LibroAutorLogic.add_libro_autor(libro_autor)
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
                # fecha_devolucion = fecha_actual + timedelta(days=7)

                # LA LÍNEA DE ABAJO ES PARA HACER PRUEBAS PARA PROBAR EL ENVÍO DEL
                # CORREO ELECTRÓNICO
                fecha_devolucion = fecha_actual + timedelta(days=2)

                fecha_devolucion_str = fecha_devolucion.strftime('%Y-%m-%d')

                pedido.fecha_pedido = fecha_actual_str
                pedido.fecha_devolucion = fecha_devolucion_str

                # Agrego el id del cliente al pedido
                persona_data = session.get('persona_logueda')
                persona_id = persona_data.get('id')
                pedido.id_persona = persona_id
                PedidoLogic.add_pedido(pedido)
                # Elimino el carrito
                app.config['CARRITO'] = []
        return render_template('mensaje.html', mensaje='Pedido realizado exitosamente')
    else:
        return render_template('mensaje.html', mensaje='')


@app.route('/autor_mas_leido')
def autor_mas_leido():
    mes = 11
    año = 2023
    AutorMasLeidoEnUnMesGrafico.crea_grafico(mes, año)
    return render_template('mensaje.html', mensaje='Hecho')
