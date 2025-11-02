import socket
import sys

# --- CONFIGURACIÓN DEL SERVIDOR ---
HOST = '127.0.0.1'
PORT = 65432

def enviar_tarea(tarea):
    """
    Establece conexión, envía la tarea, y espera el resultado del servidor.
    """
    try:
        # Crea un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Cliente: Conectando a {HOST}:{PORT}...")
            s.connect((HOST, PORT)) 

            # 1. Envía la tarea
            print(f"Cliente: Enviando tarea: '{tarea}'")
            s.sendall(tarea.encode('utf-8'))

            # 2. Espera y recibe la respuesta
            resultado = s.recv(1024)
            
            # 3. Muestra el resultado
            print(f"Cliente: Resultado del Servidor: {resultado.decode('utf-8')}")

    except ConnectionRefusedError:
        print("Cliente: ERROR: Conexión rechazada. Asegúrate de que el servidor esté corriendo en el puerto correcto.")
    except Exception as e:
        print(f"Cliente: Ocurrió un error de conexión: {e}")

if __name__ == "__main__":
    # La tarea se toma del argumento de línea de comandos (sys.argv)
    if len(sys.argv) > 1:
        tarea_a_enviar = " ".join(sys.argv[1:])
    else:
        tarea_a_enviar = "Tarea de Procesamiento Estándar"
        print("Usando tarea de ejemplo. Para personalizar, ejecuta: python client.py \"Mi tarea.\"")

    enviar_tarea(tarea_a_enviar)