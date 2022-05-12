from flask import Flask, render_template, request, session, redirect

app = Flask(__name__) # generando la app
app.secret_key = "cisco1234" # llave secreta


# Funciones App
@app.route('/')
def index():
    #Inicializamos el juego regresando el template inicial
    return render_template("Ahorcado.html")

# Funcion inicial del ahocardo para poner una palabra  y luego jugar
@app.route('/ahorcado', methods=['POST'])
def iniciar_juego():
    # Variables Session
    session['palabra'] = request.form.get('palabra', None).lower() # Solicitando la palabra dentro del juego
    session['intentos'] = 0                                        # Intento de adivinanza del jugador
    session['palabras_usadas'] = []                                # Lista de letras usadas por el jugador
    session['estado_juego'] = None                                 # Estado del juego (None,true, false)
    # Variable espacios (genera los espacios  para la palabra escondida)
    espacios = ' _ ' * len(session['palabra'])
    palabras_usadas = ' '.join(session['palabras_usadas'])
    return render_template('juego.html', espacio=espacios, usadas=palabras_usadas, intentos=session["intentos"])


# Funcion auxiliar para la funcion juego
def adivinanza(palabra,lista_de_palabras_usadas):
    # Listas
    letrasCorrectas = []
    listaPalabra = []
    listaPalabra[:0] = palabra
    #revisamos
    for letra in listaPalabra:
        if letra in lista_de_palabras_usadas:
            letrasCorrectas.append(letra)
        else:
            # en caso contrario se matiene la letra oculta
            letrasCorrectas.append('_')
    return ' '.join(letrasCorrectas)

# Funcion  con ruta post que nos genera el juego
@app.route('/juego', methods=['POST'])
def juego():
    letra = request.form.get('letra', None).lower()
    # Una vez en juego
    if letra in ''.join(session['palabras_usadas']):
        palabras_usadas = ' '.join(session['palabras_usadas'])
        palabra = adivinanza(session['palabra'], session['palabras_usadas'])
        return render_template('juego.html',  espacio=palabra, palabras_usadas=palabras_usadas, intentos=session["intentos"], estado_juego=session['estado_juego'])

    # Agregamos  y formateamos las letras usadas
    _palabras_usadas1 = [] # lista
    _palabras_usadas1 = session['palabras_usadas'].copy()
    _palabras_usadas1.append(letra)
    session['palabras_usadas'] = list(set(_palabras_usadas1))
    palabras_usadas = ' '.join(session['palabras_usadas'])
    palabra = adivinanza(session['palabra'], session['palabras_usadas'])

    # Si la letra no esta en la palabra , le agregamos un inteto
    if not letra in session['palabra']:
        session['intentos'] += 1

        # Si ya o existen palabras escondidas, entonces se gana el juego
    if not '_' in palabra:
        session['estado_juego'] = True
        return render_template('juego.html', espacio=palabra, palabras_usadas=palabras_usadas,
                               intentos=session["intentos"], estado_juego=session['estado_juego'])

    #Si los intentos son menores a 6, seguimos el juego
    if session['intentos'] < 6:  # Continue game
        return render_template('juego.html', espacio=palabra, palabras_usadas=palabras_usadas, intentos=session["intentos"], estado_juego=session['estado_juego'])


    # Si niguna de las anteriores se cumple,se acaba el juego , perdiendo la partida
    return render_template('juego.html',  espacio=session['palabra'], palabras_usadas=palabras_usadas, intentos=6, estado_juego=session['estado_juego'])


@app.route('/juegonuevo')
def juego_nuevo():
    # Eliminamos y reiniciamos cada variable session
    session.pop("palabra", None)
    session.pop("intentos", None)
    session.pop("palabras_usadas", None)
    session.pop("estado_juego", None)
    return redirect("/")

# main
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
