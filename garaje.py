from machine import ADC, Pin
import network
import urequests
import json
import time
import socket
import uselect

# Pines de entrada
proxiAdc = ADC(Pin(2))
sensorPir = Pin(41, Pin.IN)
fotore = Pin(1, Pin.IN)
sensorObstaculo = Pin(18, Pin.IN)

# Pines de salida 
porton = Pin(4, Pin.OUT)
lucesM = Pin(5, Pin.OUT)
luces = Pin(42, Pin.OUT)
ledVerde = Pin(17, Pin.OUT)
ledAzul = Pin(16, Pin.OUT)   
ledRojo = Pin(7, Pin.OUT)

# configurar ADC para voltaje 3v
proxiAdc.atten(ADC.ATTN_11DB)

# tiempo de espera en segundos (10 minutos = 600 segundos)
tiempo_espera = 60

# Variables de control
senal_activa = False
tiempo_inicio_deteccion = 0
tiempo_actual = 0
tipoSensor = ""        # que sensor se activo
pir = "0"          # detecta movimiento
sensorLaser = "0"        # el ingreso esta obstaculizado


# WiFi
#wifi_config = {'ssid': 'Estudiantes', 'password': 'Estudiantes'}
wifi_config = {'ssid': 'Tech_D0008381', 'password': 'UZCMVZPD'}
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_config['ssid'], wifi_config['password'])
while not wlan.isconnected():
    time.sleep(1)
print("Conectado a WiFi")
print("IP:", wlan.ifconfig()[0])

# configurar ADC para voltaje 3v
proxiAdc.atten(ADC.ATTN_11DB)

# registro de ingresos
def registro_ingresos():
    global pir, tipoSensor
    tipoSensor = "registro_ingresos"
    pir = 1
    url = "http://192.168.0.15/tareaWeb/proyectoFinal/esp32Conexion.php"
    data = {"tabla": tipoSensor, "pir": pir}
    headers = {'Content-Type': 'application/json'}

    response = urequests.post(url, json=data, headers=headers)
    
    print("Respuesta del servidor:")
    print(response.text)

    datos = response.json()
    response.close()

    if "ID" in datos:
        ID_Ingreso = datos["ID"]
        Hora = datos["HORA"]
        print("Se registro ingreso:", ID_Ingreso, Hora)

    elif "mensaje" in datos:
        print("Mensaje:", datos["mensaje"])

    elif "error" in datos:
        print("Error:", datos["error"])

    else:
        print("Respuesta inesperada:", datos)
        

# registro de ostaculo
def registro_obstaculo():
    global sensorLaser, tipoSensor
    tipoSensor = "registro_obstaculo"
    sensorLaser = 1
    url = "http://192.168.0.15:8080/tareaWeb/proyectoFinal/esp32Conexion.php"
    #url = "http://192.168.56.1/garaje/esp32Conexion.php"
    data = {"tabla": tipoSensor, "laser": sensorLaser}
    headers = {'Content-Type': 'application/json'}
    
    import json
    print("Payload JSON:", json.dumps(data))
    response = urequests.post(url, json=data, headers=headers)
    
    print("Respuesta del servidor:")
    print(response.text)

    datos = response.json()
    response.close()

    if "ID_Obstaculo" in datos:
        ID_Obstaculo = datos["ID_Ostaculo"]
        Hora = datos["Hora"]
        print("Se registro ingreso:", ID_Ostaculo, Hora)

    elif "mensaje" in datos:
        print("Mensaje:", datos["mensaje"])

    elif "error" in datos:
        print("Error:", datos["error"])

    else:
        print("Respuesta inesperada:", datos)
        
                
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
s.setblocking(False)  # modo no-bloqueante

poller = uselect.poll()
poller.register(s, uselect.POLLIN)

def revisar_web():
    # Configurar socket web
    def web_page(msg):
        return """... <p>Estado: {}</p> ...""".format(msg) 
    
    
    # Retorna True si hubo y manejó una conexión web
    events = poller.poll(0)  # timeout 0 = no bloqueante
    if not events:
        return False
    for sock, event in events:
        if sock is s:
            try:
                cl, addr = s.accept()
            except OSError:
                return False
            req = cl.recv(1024).decode('utf-8')
            # acá tu lógica de control luces/portón
            if 'GET /luz_on' in req:
                luces.value(1)
                response = web_page("LED encendido")
            elif 'GET /luz_off' in req:
                luces.value(0)
                response = web_page("LED apagado")
            elif 'GET /porton_abierto' in req:
                porton.value(1)
                response = web_page("Portón abierto")
            elif 'GET /porton_cerrado' in req:
                porton.value(0)
                response = web_page("Portón cerrado")
            else:
                response = web_page("Sin cambio")
            cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
            return True
    return False

        
# Bucle principal
while True:
    #sensor pir y fotoresistencia
    if sensorPir.value() == 1:
        #registro_ingresos()
        print("deteccion")
        time.sleep(1)
        if fotore.value() == 1:
            lucesM.value(1)
            print("luz encendida")
        else:
            lucesM.value(0)
            
    else:
        lucesM.value(0)
    
    # Comprueba si el sensor ha detectado obstaculo
    if sensorObstaculo.value() == 1:
        if not senal_activa:
            senal_activa = True
            tiempo_inicio_deteccion = time.time()
            print("Señal detectada. Iniciando temporizador...")
    else:
        if senal_activa:
            senal_activa = False
            print("Señal desactivada. Temporizador reiniciado.")

    if senal_activa:
        tiempo_actual = time.time()
        if tiempo_actual - tiempo_inicio_deteccion > tiempo_espera:
            #registro_obstaculo()
            print("Temporizador reiniciado")
            senal_activa = False
            
    time.sleep(0.2)
    
    #control de luces y porton
    #revisar_web()
        

    #  convertir voltaje a binario = voltaje entrada * resolucion del exp32(2^12bits) / voltaje de comparacion
    V = proxiAdc.read()
    print(V)
    time.sleep(0.2)

    if V <= 1000:
        ledVerde.value(0)
        ledAzul.value(0)
        ledRojo.value(0)

    elif 1001 < V <= 2500:
        ledVerde.value(1)
        ledAzul.value(0)
        ledRojo.value(0)

    elif 2501 <= V <= 4000:
        ledVerde.value(0)
        ledAzul.value(1)
        ledRojo.value(0)

    elif 4001 <= V:
        ledVerde.value(0)
        ledAzul.value(0)
        ledRojo.value(1)
        

  