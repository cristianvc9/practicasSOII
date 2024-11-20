import socket
import json

# Configuración del cliente
HOST = '172.20.10.11'  # Dirección del servidor
PORT = 65432        # Puerto del servidor

# Función para enviar transacciones al servidor
def enviar_transaccion(cliente_id, cantidad):
    transaccion = {
        "cliente_id": cliente_id,
        "cantidad": cantidad
    }
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(transaccion).encode('utf-8'))
        respuesta = s.recv(1024).decode('utf-8')
        print("Respuesta del servidor:", respuesta)

# Iniciar cliente y permitir entrada de transacciones en la terminal
print("Cliente iniciado. Conectándose al servidor...")

cliente_id = 1  # Puedes cambiar el cliente_id si deseas simular múltiples clientes

while True:
    # Pedir al usuario que ingrese el tipo y monto de la transacción
    tipo = input("Ingresa el tipo de transacción (retiro/ingreso) o 'salir' para finalizar: ").strip().lower()
    if tipo == "salir":
        print("Finalizando cliente...")
        break

    try:
        cantidad = float(input("Ingresa la cantidad de la transacción: "))
        if tipo == "retiro":
            cantidad = -abs(cantidad)  # Se asegura de que sea negativo
        elif tipo == "ingreso":
            cantidad = abs(cantidad)   # Se asegura de que sea positivo
        else:
            print("Tipo de transacción no válido. Intenta de nuevo.")
            continue

        # Enviar la transacción al servidor
        enviar_transaccion(cliente_id=cliente_id, cantidad=cantidad)

    except ValueError:
        print("Cantidad no válida. Asegúrate de ingresar un número.")
