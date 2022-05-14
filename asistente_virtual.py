import time
import re
import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# Opciones de voz / idiomas
id1 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0'
nombre = 'Yafel'


# Escuchar microfono y devolver el audio como texto
def transformar_audio_a_texto():
    # Almacenar recognizer en variable
    r = sr.Recognizer()

    # Configurar microfono
    with sr.Microphone() as origen:
        # tiempo de espera
        r.pause_threshold = 0.8

        # Informar que ha comenzado la grabacion
        print('Ya puedes hablar')

        # Guardar lo que se escuche como audio
        audio = r.listen(origen)

        try:
            # Buscar en google lo que haya escuchado
            pedido = r.recognize_google(audio, language='es-MX')
            # Prueba de que pudo ingresar
            print('Has dicho: ' + pedido)
            # Devolver pedido
            return pedido
        # En caso de que no lo comprenda
        except sr.UnknownValueError:
            # Prueba de que no comprendio
            print('Uppss, no he entendido')
            # Devolver error
            return 'Sigo esperando'
        # En caso de no resolver el pedido
        except sr.RequestError:
            # Prueba de que no comprendio
            print('Uppss, no hay servicio')
            # Devolver error
            return 'Sigo esperando'
        # Error inesperado
        except:
            # Prueba de que no comprendio
            print('Uppss, algo ha salido mal')
            # Devolver error
            return 'Sigo esperando'


# Funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)
    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# Informar dia de la semana
def pedir_dia():
    # Crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # Crear variable para el dia de la semana
    dia_semana = dia.weekday()
    mes_actual = dia.month
    print(mes_actual)

    # Diccionario con nombes de dias y meses
    meses = {0: 'Enero',
             1: 'Febrero',
             2: 'Marzo',
             3: 'Abril',
             4: 'Mayo',
             5: 'Junio',
             6: 'Julio',
             7: 'Agosto',
             8: 'Septiembre',
             9: 'Octubre',
             10: 'Noviembre',
             11: 'Diciembre',
             }
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo',
                  }

    # Mencionar dia de la semana
    hablar(f'Hoy es:{calendario[dia_semana]} {dia.day} de {meses[mes_actual - 1]}')


# Informar que hora es
def pedir_hora():
    # Crear variable con el tiempo actual
    hora = datetime.datetime.now()
    if hora.hour >= 24 or hora.hour < 12:
        dia = 'de la mañana'
    elif 12 < hora.hour < 20:
        dia = 'de la tarde'
    else:
        dia = 'de la noche'
    # Decir hora
    hablar(f'Son las {hora.hour} {dia} con {hora.minute} minutos')


# Saludo inicial
def saludo_inicial():
    # Crear variable para la hora
    hora = datetime.datetime.now()
    if hora.hour <= 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 12:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'
    # Saludar
    hablar(f'Hola {nombre},{momento}, te habla sabina, tu asistente personal, en que te puedo ayudar hoy?')


def volver_hacer():
    time.sleep(1)
    hablar('¿Que más deseas hacer?')


# Funcion cental del asistente

def pedir_cosas():
    # Activar saludo inicial
    saludo_inicial()
    # Variable de corte
    comenzar = True
    # Loop
    while comenzar:
        dic = ['abrir youtube', 'abrir navegador', 'qué día es hoy', 'qué hora es', 'busca en wikipedia',
               'busca en internet', 'escuchar', 'chiste', 'enviar mensaje', 'controlar pc', 'tomar captura',
               'precio de las acciones', 'me voy a dormir']
        # activar microfono y guardar el pedido en string
        pedido = transformar_audio_a_texto().lower()
        if 'qué puedes hacer' in pedido:
            hablar(f'Por ahora puedes decir: {dic}')
        elif dic[0] in pedido:
            hablar('Entendido, abriendo YouTube')
            webbrowser.open('https://youtube.com')
            volver_hacer()
            continue
        elif dic[1] in pedido:
            hablar('Entendido, abriendo navegador')
            webbrowser.open('https://google.com')
            volver_hacer()
            continue
        elif dic[2] in pedido:
            pedir_dia()
            volver_hacer()
            continue
        elif dic[3] in pedido:
            pedir_hora()
            volver_hacer()
            continue
        elif dic[4] in pedido:
            pedido = pedido.replace('busca en wikipedia', '')
            hablar(f'Buscando, {pedido} en wikipedia')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Encontre esto en wikipedia:')
            hablar(resultado)
            volver_hacer()
            continue
        elif dic[5] in pedido:
            hablar('Entendido.')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            volver_hacer()
            continue
        elif dic[6] in pedido:
            pedido = pedido.replace(dic[6], '')
            hablar(f'Genial, reproduciendo {pedido}')
            pywhatkit.playonyt(pedido)
            volver_hacer()
            continue
        elif dic[7] in pedido:
            hablar(pyjokes.get_joke('es'))
            volver_hacer()

            continue
        elif dic[8] in pedido:
            patron = re.compile(r'\s+')

            hablar('¿A que número?.Incluye el codigo del país seguido del número')
            numero = transformar_audio_a_texto()
            hablar(f'¿Dijiste: {numero} ?')
            sentencia = re.sub(patron, '', numero)
            resp = transformar_audio_a_texto().lower()
            if resp == 'sí':
                hablar('Cual es tu mensaje?')
                mensaje = transformar_audio_a_texto()
                hablar('Enviando mensaje')
                pywhatkit.sendwhatmsg_instantly(sentencia, mensaje)
                volver_hacer()
            continue
        elif dic[9] in pedido:
            hablar('Iniciando servidor...  Te veo en tu dispositivo')
            pywhatkit.start_server(8000)
            volver_hacer()
        elif dic[10] in pedido:
            hablar('Tomando captura, te la mostrare en un momento.')
            pywhatkit.take_screenshot('mi_captura')
            volver_hacer()
        elif dic[11] in pedido:
            accion = pedido.split('de')[-1].strip()
            pedido = pedido.replace('precio de las', '')
            hablar(f'Buscando {pedido}, un momento por favor')
            cartera = {'apple': 'AAPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL',
                       'netflix': 'NFLX'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'Lo he encontrado, el precio de {accion} es {precio_actual}')
                volver_hacer()
                continue
            except:
                hablar('Lo siento, no he podido encontrarla')
                continue
        elif 'adiós' in pedido:
            hablar(f'Oki {nombre}, me retiro, puedes volver a llamarme si necesitas algo.')
            break
        elif dic[12] in pedido:
            hablar(f'Descansa {nombre} dulces sueños')
            break
        else:
            hablar('Lo siento, no te he entendido')


pedir_cosas()
