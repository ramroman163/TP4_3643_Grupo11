import json
import os
import requests

BASE = "http://localhost:58000/api/v1"
ARCHIVO = "snapshot_red.json"

# Obtenemos nuevo ticket
headers = {"Content-Type": "application/json"}
body = json.dumps({"username": "cisco", "password": "cisco"})
ticket = requests.post(BASE + "/ticket", data=body, headers=headers).json()["response"]["serviceTicket"]
auth = {"X-Auth-Token": ticket}

# Obtenemos equipos actuales
equipos = requests.get(BASE + "/network-device", headers=auth).json()["response"]
hosts = requests.get(BASE + "/host", headers=auth).json()["response"]

actual = {}
for e in equipos:
    if "hostname" in e:
        actual["equipo: " + e["hostname"]] = e.get("managementIpAddress", "")
for h in hosts:
    actual["host: " + h.get("hostName", "?")] = h.get("hostIp", "")

# Comparamos con el archivo anterior, si existe, si hubieron cambios
if os.path.exists(ARCHIVO):
    with open(ARCHIVO, encoding="utf-8") as f:
        anterior = json.load(f)

    nuevos = [k for k in actual if k not in anterior]
    perdidos = [k for k in anterior if k not in actual]
    cambiados = [k for k in actual if k in anterior and actual[k] != anterior[k]]

    print("NUEVOS:", nuevos or "ninguno")
    print("DESAPARECIDOS:", perdidos or "ninguno")
    print("CON IP DISTINTA:", cambiados or "ninguno")
else:
    print("Primera ejecución: se guarda la snapshot inicial.")

# Guardamos los equipos actuales
with open(ARCHIVO, "w", encoding="utf-8") as f:
    json.dump(actual, f, indent=2, ensure_ascii=False)

print(f"Snapshot guardada: {len(actual)} elementos")