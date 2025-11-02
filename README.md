# PFO 3: Rediseño como Sistema Distribuido (Cliente-Servidor)

## Objetivo del Proyecto
Implementar un sistema distribuido con arquitectura Cliente-Servidor utilizando sockets TCP en Python para demostrar la concurrencia a través de un Pool de Hilos.

## Diagrama de Arquitectura Conceptual
Aunque la implementación se centra en los módulos Cliente y Servidor de Entrada, el diseño completo del sistema es el siguiente:


1.  **Clientes**: Inician la petición (Implementado por client.py).
2.  **Balanceador de Carga (Nginx/HAProxy)**: Distribuye la carga al Servidor de Entrada.
3.  **Servidor de Entrada (server.py):** Recibe la conexión, utiliza Pool de Hilos para la concurrencia, y en un sistema real, enviaría la tarea a RabbitMQ.
**Cola de Mensajes (RabbitMQ):)**: Actúa como buffer asíncrono.
**Servidores Workers**: Consumen tareas y procesan la lógica.
**Almacenamiento Distribuido (PostgreSQL, S3):):** Persistencia de datos.

## Estructura

PFO3/ 
│
├── client/ 
│ └── client.py # Código del Cliente
├── server/ 
│ └── server.py # Código del Servidor (con ThreadPoolExecutor) 
└── README.md # Documentación del proyecto y ejecución

## Componentes Implementados

| Archivo | Rol | Descripción Técnica |
| :--- | :--- | :--- |
| server/server.py | **Servidor de Entrada** | Crea un socket TCP, acepta conexiones y utiliza un **concurrent.futures.ThreadPoolExecutor** (Pool de Hilos) para manejar hasta 10 clientes simultáneamente. Simula el tiempo de procesamiento (3 segundos). |
| client/client.py | **Cliente** | Crea un socket TCP, se conecta al servidor, envía una cadena de texto (la tarea) y espera sincrónicamente la respuesta final. |


## Instrucciones de Ejecución

El objetivo de demostrar la concurrenciaa concurrencia** al iniciar varios clientes y verificar que el servidor los atiende a todos a la vez.

### Requisitos
* Python 3.x
* Entorno de terminal (VSC, PowerShell, CMD, etc.)

### Paso 1: Iniciar el Servidor (Terminal 1)

Abre la primera terminal en la raíz del proyecto (PFO3-Distribuido/) y ejecuta el servidor:

`bash
python server/server.py

Resultado esperado: El servidor indicará que está escuchando en el puerto 65432.

### Paso 2: Ejecutar Clientes Concurrentes (Terminal 2 y 3)
Abre dos o tres terminales nuevas (puedes usar la función "Dividir Terminal" de VSC) y ejecuta los clientes lo más rápido posible para que lleguen al servidor a la vez.

Cliente A (Terminal 2):
python client/client.py "Generar Informe Financiero"

Cliente B (Terminal 3)
python client/client.py "Generar Facturas"

**Verificación de Concurrencia**
En la Terminal 1 (Servidor), se debe observar que ambas tareas (Informe Financiero y Generar Facturas) son iniciadas por hilos separados y terminan aproximadamente al mismo tiempo (después de 3 segundos), lo cual confirma que el Pool de Hilos funciona correctamente y evita el bloqueo.

