import socket
import json
import os
import time

# Configuración del servidor
HOST = '172.20.10.2'  # Dirección en la que el servidor escucha
PORT = 65432        # Puerto de escucha del servidor

# Archivo para el log de transacciones
log_file = "transaction_log.json"

# Estado inicial del sistema
estado_sistema = {
    "cliente_id": 2,
    "balance": 1000
}

# Cargar el último estado desde el archivo log (si existe)
def cargar_estado():
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            lines = file.readlines()
            if lines:
                last_log = json.loads(lines[-1])  # Último estado guardado
                estado_sistema["cliente_id"] = last_log["cliente_id"]
                estado_sistema["balance"] = last_log["balance"]
                print("Estado restaurado desde el log:", estado_sistema)

# Función para registrar una transacción en el log
def registrar_transaccion(transaccion):
    with open(log_file, "a") as file:
        file.write(json.dumps(transaccion) + "\n")

# Función para procesar la transacción y simular una caída del servidor
def procesar_transaccion(transaccion):
    # Actualizar balance
    estado_sistema["balance"] += transaccion["cantidad"]
    registrar_transaccion(estado_sistema)
    
    # Simular una falla en medio de una transacción importante
    if transaccion["cantidad"] == -500:  # Ejemplo de condición para simular falla
        print("Simulando una falla del servidor...")
        time.sleep(1)  # Pausa breve para simular un procesamiento
        os._exit(1)  # Terminar el programa abruptamente
    
    return f"Transacción realizada: Nuevo balance: {estado_sistema['balance']}"

# Iniciar el servidor y cargar el último estado si existe
cargar_estado()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Conexión establecida con {addr}")
            # Recibir datos del cliente
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            # Procesar la transacción recibida
            transaccion = json.loads(data)
            respuesta = procesar_transaccion(transaccion)
            # Enviar respuesta al cliente
            conn.sendall(respuesta.encode('utf-8'))
            print("Respuesta enviada al cliente:", respuesta)
