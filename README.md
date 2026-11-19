# API de Python para redes Cisco (Packet Tracer)

Scripts en Python para consultar la API REST del Network Controller de Cisco Packet Tracer (TP N° 4 Integrador de Redes de Computadoras).

Incluye los scripts suministrados por la cátedra y un script propio (`05_change-detector.py`).

## Requisitos

- Python 3
- Packet Tracer abierto, con el Network Controller activo y su API disponible en `http://localhost:58000`
- Usuario y contraseña de la API configurados en el controlador (en los scripts: `cisco` / `cisco`)

## Instalación

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Scripts (carpeta `src/`)

| Script | Qué hace |
|---|---|
| `01_get-ticket.py` | Se autentica contra la API y obtiene el *service ticket* (token) necesario para las demás consultas. |
| `02_get-network-device.py` | Consulta `/network-device` y muestra los equipos de red que ve el controlador: hostname, plataforma e IP de administración. |
| `03_get-host.py` | Consulta `/host` y muestra los hosts de la red: nombre, IP, MAC e interfaz a la que están conectados. |
| `04_tabulate.py` | Pide el ticket, consulta equipos y hosts, y los muestra en tablas ordenadas usando la biblioteca `tabulate`. |
| `05_change-detector.py` | **Script propio.** Detector de cambios: guarda una "foto" de los equipos y hosts que ve el controlador (`foto_red.json`) y, en cada ejecución, la compara con la anterior para informar qué elementos son nuevos, cuáles desaparecieron y cuáles cambiaron de IP. |

## Uso

Con el entorno virtual activado, ejecutar desde la raíz del repositorio:

```
python src/01_get-ticket.py
python src/02_get-network-device.py
python src/03_get-host.py
python src/04_tabulate.py
python src/05_change-detector.py
```

Los scripts 01 a 04 son los suministrados.

### Cómo probar el script 05

1. Ejecutarlo una vez: guarda la foto inicial de la red.
2. Hacer un cambio en Packet Tracer (por ejemplo, desconectar o agregar un host).
3. Volver a ejecutarlo: muestra los elementos nuevos, desaparecidos o con IP distinta.

## Autores

Grupo 11

# Entorno de virtualización Python

# Pasos de instalación en Linux:

## 1. Clonación del proyecto

Desde la terminal ejecutar:

**git clone** <URL_del_repositorio> <nombre_de_la_carpeta_de_destino>

Luego ejecutar **cd** <nombre_de_la_carpeta_de_destino>. Esta carpeta será la raíz de nuestro proyecto en Python.

## 2. Creación del entorno virtual

Supongamos que el nombre que le damos al entorno virtual es **cisco**, entonces se creará una carpeta **cisco** con todas las librerías y dependencias necesarias paea nuestro proyecto. 

La manera de realizarlo es la siguiente:

# python3 -m venv <nombre_del_entorno>
Ejemplo: python3 -m venv cisco

Para activar el entorno escribimos **source cisco/bin/activate**, en la carpeta raíz del proyecto. El nombre del entorno virtual aparecerá entre paréntesis ().

## 3. Instalación de las dependencias, en este caso las librerías requests y tabulate

En la carpeta raíz de nuestro proyecto y dentro del entorno virtual escribimos: **pip install -r requirements.txt**

## 4. Selección del intérprete Python para nuestro entorno virtual

<img width="881" height="118" alt="image" src="https://github.com/user-attachments/assets/18c41d8e-d338-48b6-953c-b2499c57319f" />

<img width="736" height="412" alt="image" src="https://github.com/user-attachments/assets/2a795fcd-2cf8-47ef-a5a6-d21e09ce967f" />

Tal como se ve en la figura seleccionamos Python 3.10.12 (cisco) que se mostrará como entorno recomendado.

## 5. Desactivación del entorno virtual

Simplemente escribimos en la línea de comandos: **deactivate**


