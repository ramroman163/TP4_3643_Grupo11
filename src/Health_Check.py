#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getpass
import requests

class ControllerPT:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.ticket = None
        self.headers = {"Content-Type": "application/json"}
        self._get_ticket()

    def _get_ticket(self):
        url = f"{self.base_url}/ticket"
        payload = {
            "username": self.username,
            "password": self.password
        }
        try:
            resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=5)
            
            if resp.status_code == 200 or resp.status_code == 201:
                response_json = resp.json()
                self.ticket = response_json["response"]["serviceTicket"]
                self.headers["X-Auth-Token"] = self.ticket
                print(f"\n[+] Autenticación exitosa. Token obtenido correctamente.\n")
            else:
                print(f"\n[-] Error de autenticación ({resp.status_code}): El usuario o contraseña son incorrectos.\n")
        except requests.exceptions.ConnectionError:
            print(f"\n[-] Error de conexión: No se pudo establecer comunicación con el controlador.")
            print(f"    Asegúrese de que Cisco Packet Tracer esté abierto y el Network Controller activo.\n")
        except Exception as e:
            print(f"\n[-] Error inesperado al conectar: {e}\n")

    def show_network_health(self):
        if not self.ticket:
            return

        url = f"{self.base_url}/network-device"
        try:
            resp = requests.get(url, headers=self.headers, timeout=5)
            
            if resp.status_code == 200:
                devices = resp.json().get("response", [])
                
                if not devices:
                    print("=" * 55)
                    print("[-] No se encontraron dispositivos en el inventario.")
                    print("=" * 55)
                    return

                categories = {}
                unmanaged_ips = []
                
                for d in devices:
                    cat = d.get("type")
                    status = d.get("collectionStatus", "Unknown")
                    ip = d.get("managementIpAddress", "Sin IP")
                    
                    if not cat or cat.strip() == "" or status == "Wrong Credentials":
                        cat = "No Administrados"
                        unmanaged_ips.append(ip)
                    
                    if cat not in categories:
                        categories[cat] = {"total": 0, "managed": 0}
                    
                    categories[cat]["total"] += 1
                    if status == "Managed":
                        categories[cat]["managed"] += 1

                print("=" * 55)
                print(f"{'CATEGORÍA':<18} | {'EQUIPOS':<10} | {'ESTADO DE SALUD':<15}")
                print("=" * 55)
                
                sorted_categories = sorted(categories.keys(), key=lambda x: (x == "No Administrados", x))
                
                for cat in sorted_categories:
                    data = categories[cat]
                    
                    if cat == "No Administrados":
                        equipos_str = str(data["total"])
                        health_percentage = 0
                    else:
                        equipos_str = f"{data['managed']}/{data['total']}"
                        health_percentage = int((data["managed"] / data["total"]) * 100)
                    
                    print(f"{cat:<18} | {equipos_str:<10} | {health_percentage}% OK")
                    
                print("=" * 55)
                
                if unmanaged_ips:
                    print("\n[!] DETALLE DE EQUIPOS NO ADMINISTRADOS O FALLIDOS:")
                    for idx, ip in enumerate(unmanaged_ips, 1):
                        print(f"    -> Equipo #{idx} - IP de Gestión: {ip}")
                    print("-" * 55)
                    
            else:
                print(f"[-] Error al consultar el inventario ({resp.status_code}): {resp.text}")
        except Exception as e:
            print(f"[-] Fallo al recuperar las métricas de salud: {e}")

if __name__ == "__main__":
    print("=============================================")
    print("   NETCON NETWORK CONTROLLER - HEALTH CHECK   ")
    print("=============================================")
    
    url_input = input("Ingrese la URL base [http://localhost:58000/api/v1]: ").strip() or "http://localhost:58000/api/v1"
    username_input = input("Usuario del controlador: ").strip()
    
    try:
        password_input = getpass.getpass("Contraseña del controlador: ")
    except Exception:
        password_input = input("Contraseña del controlador: ")

    pt = ControllerPT(url_input, username_input, password_input)
    
    if pt.ticket:
        pt.show_network_health()
        
    print("\nProceso finalizado.")
    
    if sys.platform.startswith("win"):
        input("Presione Enter para cerrar esta ventana...")
