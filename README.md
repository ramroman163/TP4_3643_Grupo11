# API de Python para redes Cisco (Packet Tracer)

Scripts en Python para consultar la API REST del Network Controller de Cisco Packet Tracer (TP N° 4 Integrador de Redes de Computadoras).

Incluye los scripts suministrados por la cátedra y dos scripts propios: `05_change-detector.py` y `Health_Check.py`.

**Autores:** Grupo 11

## Contenido

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Scripts](#scripts-carpeta-src)
- [Uso](#uso)
- [Entorno virtual: selección del intérprete y desactivación](#selección-del-intérprete-en-vs-code)

## Requisitos

- Python 3 (probado con Python 3.10.12)
- Packet Tracer abierto, con el Network Controller activo y su API disponible en `http://localhost:58000`
- Usuario y contraseña de la API configurados en el controlador (por defecto: `cisco` / `cisco`)
- Bibliotecas `requests` y `tabulate` (listadas en `requirements.txt`)

## Instalación

### 1. Clonar el proyecto

```
git clone <URL_del_repositorio> <nombre_de_la_carpeta_de_destino>
cd <nombre_de_la_carpeta_de_destino>
```

Esta carpeta es la raíz del proyecto.

### 2. Crear y activar el entorno virtual

Se crea una carpeta con todas las librerías y dependencias del proyecto. En este ejemplo el entorno se llama `cisco`:

| Sistema | Crear | Activar |
|---|---|---|
| Linux | `python3 -m venv cisco` | `source cisco/bin/activate` |
| Windows | `python -m venv cisco` | `cisco\Scripts\activate` |

Al activarlo, el nombre del entorno aparece entre paréntesis al comienzo de la línea de comandos.

### 3. Instalar las dependencias

Desde la raíz del proyecto y con el entorno activado:

```
pip install -r requirements.txt
```

## Scripts (carpeta `src/`)

### Suministrados por la cátedra

| Script | Qué hace |
|---|---|
| `01_get-ticket.py` | Se autentica contra la API y obtiene el *service ticket* (token) necesario para las demás consultas. |
| `02_get-network-device.py` | Consulta `/network-device` y muestra los equipos de red que ve el controlador: hostname, plataforma e IP de administración. |
| `03_get-host.py` | Consulta `/host` y muestra los hosts de la red: nombre, IP, MAC e interfaz a la que están conectados. |
| `04_tabulate.py` | Obtiene el ticket, consulta equipos y hosts, y los muestra en tablas con la biblioteca `tabulate` (equipos: hostname, número de serie y versión de software; hosts: nombre, tipo e IP). |

### Propios

| Script | Qué hace |
|---|---|
| `05_change-detector.py` | **Detector de cambios.** Guarda una *snapshot* de los equipos y hosts que ve el controlador (`snapshot_red.json`) y, en cada ejecución, la compara con la anterior para informar qué elementos son nuevos, cuáles desaparecieron y cuáles cambiaron de IP. |
| `Health_Check.py` | **Chequeo de salud del controlador.** Agrupa los equipos por categoría (router, switch, switch multicapa) y muestra cuántos están administrados (*Managed*) sobre el total, con su porcentaje. Los equipos sin tipo o con credenciales incorrectas se agrupan como "No Administrados" y se listan con su IP de gestión. Pide la URL, el usuario y la contraseña por teclado (la contraseña no se muestra al escribirla), por lo que no guarda credenciales en el código. |

## Uso

Con el entorno virtual activado, ejecutar desde la raíz del repositorio:

```
python src/01_get-ticket.py
python src/02_get-network-device.py
python src/03_get-host.py
python src/04_tabulate.py
python src/05_change-detector.py
python src/Health_Check.py
```

> **Nota sobre 02 y 03:** estos scripts tienen el *service ticket* escrito en el código (`X-Auth-Token`) y ese ticket vence. Si la API responde con error de autenticación, ejecutar primero `01_get-ticket.py` y reemplazar el valor del token en el script por el nuevo.

### Probar `05_change-detector.py`

1. Ejecutarlo una vez: guarda la snapshot inicial de la red.
2. Hacer un cambio en Packet Tracer (por ejemplo, desconectar o agregar un host).
3. Esperar un momento y volver a ejecutarlo: muestra los elementos nuevos, desaparecidos o con IP distinta.

> **Importante:** el script lee lo que el controlador tiene registrado, no lo que está configurado en Packet Tracer, y el controlador tarda un rato en actualizarse. Si tras un cambio el resultado es "ninguno", esperar unos instantes y ejecutarlo de nuevo.
>
> Cada ejecución sobrescribe `snapshot_red.json` con el estado actual. Por eso, después de informar un cambio, la siguiente corrida compara contra el estado ya actualizado y vuelve a mostrar "ninguno".

Ejemplo de salida cuando se cambió la IP de un host:

```
NUEVOS: ninguno
DESAPARECIDOS: ninguno
CON IP DISTINTA: ['host: PC4']
Snapshot guardada: 16 elementos
```

### Ejemplo de salida de `Health_Check.py`

```
=============================================
   NETCON NETWORK CONTROLLER - HEALTH CHECK
=============================================
Ingrese la URL base [http://localhost:58000/api/v1]:
Usuario del controlador: cisco
Contraseña del controlador:

[+] Autenticación exitosa. Token obtenido correctamente.

=======================================================
CATEGORÍA          | EQUIPOS    | ESTADO DE SALUD
=======================================================
MultiLayerSwitch   | 2/2        | 100% OK
Router             | 4/4        | 100% OK
Switch             | 3/3        | 100% OK
No Administrados   | 1          | 0% OK
=======================================================

[!] DETALLE DE EQUIPOS NO ADMINISTRADOS O FALLIDOS:
    -> Equipo #1 - IP de Gestión: 203.0.113.2
-------------------------------------------------------
```

## Selección del intérprete en VS Code

Para que VS Code use el entorno virtual, seleccionar el intérprete de Python correspondiente:

<img width="881" height="118" alt="image" src="https://github.com/user-attachments/assets/18c41d8e-d338-48b6-953c-b2499c57319f" />

<img width="736" height="412" alt="image" src="https://github.com/user-attachments/assets/2a795fcd-2cf8-47ef-a5a6-d21e09ce967f" />

Como se ve en la figura, se selecciona Python 3.10.12 (cisco), que se muestra como entorno recomendado.

## Desactivar el entorno virtual

Escribir en la línea de comandos:

```
deactivate
```