import socket
import time
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURACIÓN DE LA RED ---
HOST = '127.0.0.1'  # Interfaz local
PORT = 65432        # Puerto
MAX_WORKERS = 10    # Límite de conexiones concurrentes

# Inicialización del Pool de Hilos (executor)
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
print(f"Servidor: Pool de hilos configurado con un máximo de {MAX_WORKERS} workers.")


def procesar_tarea_simulada(tarea, addr):
    """
    Simula el trabajo del Servidor Worker que iría a RabbitMQ en un sistema real.
    """
    tarea_str = tarea.decode('utf-8').strip()
    print(f"[WORKER] Procesando tarea '{tarea_str}' de {addr}...")
    
    # Simulación de tiempo de procesamiento (3 segundos)
    time.sleep(3) 
    
    # Resultado simulado
    resultado = f"TAREA PROCESADA: '{tarea_str}' (Tiempo: 3s)."
    return resultado.encode('utf-8')


def manejar_cliente(conn, addr):
    """
    Función que gestiona la conexión de un único cliente, ejecutada por un hilo del Pool.
    """
    print(f"[{addr}] Conexión aceptada. Hilo en ejecución.")
    try:
        # 1. Recepción de la tarea
        tarea = conn.recv(1024)
        if not tarea:
            return

        print(f"[{addr}] Tarea recibida: {tarea.decode('utf-8').strip()}")

        # 2. Delegación y Procesamiento (Simulado)
        # En la arquitectura real, aquí se publicaría en RabbitMQ.
        resultado = procesar_tarea_simulada(tarea, addr)

        # 3. Envío del resultado
        conn.sendall(resultado)
        print(f"[{addr}] Resultado enviado.")

    except Exception as e:
        print(f"[{addr}] Error al manejar cliente: {e}")
    finally:
        # Cierre de la conexión
        conn.close()
        print(f"[{addr}] Conexión cerrada.")


def iniciar_servidor():
    """
    Configura y corre el bucle principal del servidor de sockets.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Opción para reutilizar la dirección rápidamente
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        s.bind((HOST, PORT))
        s.listen() 

        print(f"\nServidor de Entrada escuchando en TCP {HOST}:{PORT}...")

        while True:
            # Acepta la conexión entrante
            conn, addr = s.accept()
            
            # Asigna la gestión de la conexión al ThreadPoolExecutor
            executor.submit(manejar_cliente, conn, addr)

if __name__ == "__main__":
    try:
        iniciar_servidor()
    except KeyboardInterrupt:
        print("\nServidor apagado por el usuario (Ctrl+C).")
        executor.shutdown(wait=True)