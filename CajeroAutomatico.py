import datetime
import hashlib
import re

class Cajero:
    def __init__(self):
        # Lista de cajeros con ubicaciones y billetes predeterminados
        self.cajeros = [
            {"id": 1, "ubicacion": "Chorrillos", "billetes": {200: 10, 100: 17, 50: 15, 20: 20}, "historial": []},
            {"id": 2, "ubicacion": "Los Olivos", "billetes": {200: 8, 100: 17, 50: 15, 20: 30}, "historial": []},
            {"id": 3, "ubicacion": "Surco", "billetes": {200: 6, 100: 10, 50: 13, 20: 40}, "historial": []},
            {"id": 4, "ubicacion": "Huaylas", "billetes": {200: 5, 100: 40, 50: 12, 20: 50}, "historial": []},
            {"id": 5, "ubicacion": "Barranco", "billetes": {200: 20, 100: 30, 50: 19, 20: 25}, "historial": []}
        ]
        self.cajero_seleccionado = None  # Guardará el cajero seleccionado por el usuario
        self.clientes_ordenados = []
        self.clientes = {}  # Diccionario de clientes {id_cliente: {"password": str, "saldo": float, "movimientos": list}}
        self.billetes = {200: 0, 100: 0, 50: 0, 20: 0}  # Denominaciones y su cantidad disponible
        
        # Calculamos el saldo para todos los cajeros cuando se inicializa la clase
        for cajero in self.cajeros:
            cajero['saldo'] = self.calcular_saldo(cajero)
        
    def calcular_saldo(self, cajero):
        """Calcula el saldo total del cajero basado en los billetes que tiene."""
        saldo = sum(denominacion * cantidad for denominacion, cantidad in cajero["billetes"].items())
        return saldo
    
        
    def agregar_cajero(self, ubicacion):
        """Agrega un nuevo cajero a la lista de cajeros con billetes predeterminados."""
        if not self.validar_ubicacion(ubicacion):
            return  # Si la ubicación no es válida, no agregamos el cajero
    
        # Verificar si ya existe un cajero con la misma ubicación
        if any(cajero["ubicacion"].lower() == ubicacion.lower() for cajero in self.cajeros):
            print(f"Ya existe un cajero en la ubicación '{ubicacion}'. Intente con otra ubicación.")
            return

        nuevo_id = len(self.cajeros) + 1  # Asigna un ID nuevo basado en la cantidad de cajeros actuales
        nuevo_cajero = {
            "id": nuevo_id,
            "ubicacion": ubicacion,
            "billetes": {200: 8, 100: 10, 50: 6, 20: 10},
            "historial": []  # Inicializa el historial vacío
        }
        self.cajeros.append(nuevo_cajero)
        print(f"Cajero agregado: ID {nuevo_id}, Ubicación: {ubicacion}, Billetes: {nuevo_cajero['billetes']}")

        
    def mostrar_cajeros(self):
        """Muestra la lista de todos los cajeros disponibles, resaltando el cajero seleccionado en amarillo."""
        if not self.cajeros:
            print("No hay cajeros registrados.")
        else:
            print("\n--- Cajeros Registrados ---")
            for cajero in self.cajeros:
                # Calcula el saldo del cajero dinámicamente
                saldo = self.calcular_saldo(cajero)
            
                # Verifica si este cajero es el seleccionado
                if cajero == self.cajero_seleccionado:
                    # Resalta el cajero seleccionado
                    print(f"\033[93mID: {cajero['id']}, Ubicación: {cajero['ubicacion']}, Billetes disponibles: {cajero['billetes']}, Saldo total: S/.{saldo}\033[0m")
                else:
                    print(f"ID: {cajero['id']}, Ubicación: {cajero['ubicacion']}, Billetes disponibles: {cajero['billetes']}, Saldo total: S/.{saldo}")

                
    def validar_ubicacion(self, ubicacion):
        """Verifica que la ubicación sea válida (no vacía, sin caracteres especiales como @)."""
        if not ubicacion.strip():
            print("La ubicación no puede estar vacía. Intente nuevamente.")
            return False
        if re.match(r'^[a-zA-Z0-9\s]+$', ubicacion) and not ubicacion.strip().isdigit():
            return True
        else:
            print("La ubicación debe contener solo letras, números y espacios, y no puede incluir '@'. Intente nuevamente.")
            return False

    
    def seleccionar_cajero(self):
        """Permite al usuario seleccionar el cajero que desea utilizar al inicio."""
        print("\n--- Selección de Cajero ---")
        for i, cajero in enumerate(self.cajeros, 1):
            print(f"{cajero['ubicacion']} ({i})")
        
        try:
            opcion = int(input("Seleccione el número del cajero que desea utilizar: "))
            if 1 <= opcion <= len(self.cajeros):
                self.cajero_seleccionado = self.cajeros[opcion - 1]
                print(f"\nCajero seleccionado: {self.cajero_seleccionado['ubicacion']}")
            else:
                print("Opción no válida.")
        except ValueError:
            print("Por favor ingrese un número válido.")        
    
    def registrar_transaccion(self, cajero, tipo, detalles):
        """Registra una transacción en el historial del cajero."""
        transaccion = {
            "tipo": tipo,
            "detalles": detalles
        }
        cajero['historial'].append(transaccion)
        
    def mostrar_historial(self):
        if not self.cajero_seleccionado:
            print("No se ha seleccionado un cajero.")
            return
    
        if not self.cajero_seleccionado['historial']:
            print(f"No hay transacciones registradas para el cajero en {self.cajero_seleccionado['ubicacion']}.")
            return
    
        print(f"\nHistorial de transacciones para el cajero en {self.cajero_seleccionado['ubicacion']}:")
        for transaccion in self.cajero_seleccionado['historial']:
            print(f"{transaccion['fecha']} - Tipo: {transaccion['tipo']}, Monto: S/.{transaccion['monto']} (Cliente ID: {transaccion['cliente']})")
    

    def agregar_cliente(self, id_cliente, password, saldo_inicial=0.0):
        # Verificar que el ID del cliente no sea negativo ni vacío
        if not id_cliente or id_cliente.startswith('-'):
            print("El nombre de usuario no puede estar vacío o comenzar con un guion (-). Intenta nuevamente.")
            return
    
        if id_cliente in self.clientes:
            print("Cliente ya existente.")
        else:
            # Guardamos la contraseña como hash
            hashed_password = self.hash_contraseña(password)
            self.clientes[id_cliente] = {
                "password": hashed_password,
                "saldo": saldo_inicial,  # saldo inicial es 0 de forma predeterminada
                "movimientos": []
            }
            
    def hash_contraseña(self, contraseña):
        # Usamos SHA256 para hashear la contraseña
        return hashlib.sha256(contraseña.encode('utf-8')).hexdigest()

    def validar_cliente(self, id_cliente, password):
        # Compara el hash de la contraseña ingresada con el almacenado
        hashed_password = self.hash_contraseña(password)
        return self.clientes.get(id_cliente) and self.clientes[id_cliente]["password"] == hashed_password
    
    def quicksort(self, clientes, key): # Quicksort||
        # Ordena usando quicksort de forma descendente basado en la clave (por ejemplo, saldo)
        if len(clientes) <= 1:
            return clientes
        pivote = clientes[0]
        mayores = [cliente for cliente in clientes[1:] if cliente[key] >= pivote[key]]  # Mayor o igual al pivote
        menores = [cliente for cliente in clientes[1:] if cliente[key] < pivote[key]]  # Menor al pivote
        return self.quicksort(mayores, key) + [pivote] + self.quicksort(menores, key)

    def busqueda_binaria(self, clientes, id_cliente): # Busqueda binaria|| para clientes
        # Aseguramos que la lista esté ordenada por "id"
        clientes_ordenados = sorted(clientes, key=lambda x: x["id"])
    
        izquierda = 0
        derecha = len(clientes_ordenados) - 1
    
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            cliente_actual = clientes_ordenados[medio]["id"]
        
            if cliente_actual == id_cliente:
                return clientes_ordenados[medio]
            elif cliente_actual < id_cliente:
                izquierda = medio + 1
            else:
                derecha = medio - 1
    
        return None  # No se encontró el cliente
    
    def calcular_desglose_billetes(self, cajero, monto):
        """Calcula el desglose de billetes para el monto a retirar utilizando un enfoque voraz con retroceso (Greedy + Backtracking)."""
        denominaciones = sorted(cajero['billetes'].keys(), reverse=True)
        cantidades = {den: cajero['billetes'][den] for den in denominaciones}
        desglose = {}

        def buscar_desglose(monto_restante, indice_actual):
            """Función recursiva para intentar formar el monto con diferentes combinaciones."""
            if monto_restante == 0:  # Si el monto es exacto
                return True
            if indice_actual >= len(denominaciones):  # Si no quedan denominaciones
                return False

            billete = denominaciones[indice_actual]
            max_billetes = min(int(monto_restante // billete), int(cantidades[billete]))

            for cantidad in range(max_billetes, -1, -1):  # Intenta con la mayor cantidad posible
                desglose[billete] = cantidad
                if buscar_desglose(monto_restante - cantidad * billete, indice_actual + 1):
                    return True

            desglose.pop(billete, None)  # Eliminar si no funciona esta denominación
            return False

        if buscar_desglose(monto, 0):
            return {den: cantidad for den, cantidad in desglose.items() if cantidad > 0}

        return {}  # No se puede cubrir el monto exacto



    def buscar_cajero_fuerza_bruta(self, ubicacion): # Fuerza Bruta||
        """Busca un cajero por su ubicación."""
        for cajero in self.cajeros:
            if cajero['ubicacion'].lower() == ubicacion.lower():
                print(f"Cajero encontrado: ID {cajero['id']}, Ubicación: {cajero['ubicacion']}")
                print(f"Billetes disponibles: {cajero['billetes']}")
                return cajero
        print(f"No se encontró un cajero con la ubicación: {ubicacion}")
        return None
        
    def retirar(self, id_cliente, password, monto):
        if not self.validar_cliente(id_cliente, password):
            print("Cliente o contraseña incorrectos.")
            return

        # Validación para asegurar que el monto sea un número positivo
        if not isinstance(monto, (int, float)) or monto <= 0:
            print("El monto debe ser un número positivo y mayor que cero.")
            return

        if self.clientes[id_cliente]["saldo"] < monto:
            print("Saldo insuficiente en la cuenta.")
            return

        # Asegúrate de que un cajero esté seleccionado
        if not self.cajero_seleccionado:
            print("No se ha seleccionado un cajero válido.")
            return

        # Calculamos el desglose de billetes
        desglose_billetes = self.calcular_desglose_billetes(self.cajero_seleccionado, monto)

        # Verificamos si el cajero tiene suficientes billetes para el retiro
        if not desglose_billetes:
            print("Monto no disponible en el dispensador.")
            return

        for denominacion, cantidad in desglose_billetes.items():
            if self.cajero_seleccionado['billetes'][denominacion] < cantidad:
                print(f"No hay suficientes billetes de S/.{denominacion} para cubrir el retiro.")
                return

        # Actualizar dispensador (restamos los billetes usados)
        for denominacion, cantidad in desglose_billetes.items():
            self.cajero_seleccionado['billetes'][denominacion] -= cantidad

        # Actualizar saldo del cliente y registrar el movimiento
        self.clientes[id_cliente]["saldo"] -= monto
        self.clientes[id_cliente]["movimientos"].append((datetime.datetime.now(), f"Retiro: -S/.{monto}"))
    
        # Agregar la transacción al historial del cajero
        self.cajero_seleccionado['historial'].append({
            "fecha": datetime.datetime.now(),
            "tipo": "Retiro",
            "monto": monto,
            "cliente": id_cliente
        })
    
        print(f"Retiro exitoso de S/.{monto}")
        print(f"Desglose de billetes: {desglose_billetes}")

        
    def depositar(self, id_cliente, password, billetes_depositados):
        if not self.validar_cliente(id_cliente, password):
            print("Cliente o contraseña incorrectos.")
            return
    
        total_deposito = sum(denominacion * cantidad for denominacion, cantidad in billetes_depositados.items())
    
        for denominacion, cantidad in billetes_depositados.items():
            if denominacion in self.billetes:
                self.billetes[denominacion] += cantidad
    
        self.clientes[id_cliente]["saldo"] += total_deposito
        self.clientes[id_cliente]["movimientos"].append((datetime.datetime.now(), f"Depósito: +S/.{total_deposito}"))
    
        # Agregar la transacción al historial del cajero seleccionado
        if self.cajero_seleccionado:
            self.cajero_seleccionado['historial'].append({
                'fecha': datetime.datetime.now(),
                'tipo': 'Depósito',
                'monto': total_deposito,
                'cliente': id_cliente
            })
    
        print(f"Depósito exitoso de S/.{total_deposito}")


    def transferir(self, id_origen, password, id_destino, monto):
        if not self.validar_cliente(id_origen, password):
            print("Cliente o contraseña incorrectos.")
            return

        if id_destino not in self.clientes:
            print("Cuenta destino no encontrada.")
            return

        if self.clientes[id_origen]["saldo"] < monto:
            print("Saldo insuficiente para la transferencia.")
            return
    
        self.clientes[id_origen]["saldo"] -= monto
        self.clientes[id_destino]["saldo"] += monto
        self.clientes[id_origen]["movimientos"].append((datetime.datetime.now(), f"Transferencia a {id_destino}: -S/.{monto}"))
        self.clientes[id_destino]["movimientos"].append((datetime.datetime.now(), f"Transferencia de {id_origen}: +S/.{monto}"))
    
        # Agregar las transacciones al historial del cajero seleccionado
        if self.cajero_seleccionado:
            self.cajero_seleccionado['historial'].append({
                'fecha': datetime.datetime.now(),
                'tipo': 'Transferencia',
                'monto': monto,
                'cliente': id_origen
            })
    
        print(f"Transferencia de S/.{monto} a {id_destino} realizada con éxito.")


    def consultar_movimientos(self, id_cliente, password):
        if not self.validar_cliente(id_cliente, password):
            print("Cliente o contraseña incorrectos.")
            return

        movimientos = self.clientes[id_cliente]["movimientos"]

        if not movimientos:
            print("No se encontraron movimientos.")
            return

        # Mostrar los movimientos con la ubicación del cajero
        print("Movimientos:")
        for fecha, operacion in movimientos:
            # Cambiar el formato de fecha
            fecha_formateada = fecha.strftime('%Y-%m-%d %H:%M:%S')
            color = "\033[91m" if "-" in operacion else "\033[94m"
        
            # Obtener la ubicación del cajero si hay un cajero seleccionado
            if self.cajero_seleccionado:
                ubicacion_cajero = self.cajero_seleccionado['ubicacion']
            else:
                ubicacion_cajero = "Cajero no seleccionado"

            print(f"{color}{fecha_formateada} - {operacion} (Cajero: {ubicacion_cajero})\033[0m")

    def pagar_servicio(self, id_cliente, password, monto, servicio):
        if not self.validar_cliente(id_cliente, password):
            print("Cliente o contraseña incorrectos.")
            return

        if self.clientes[id_cliente]["saldo"] < monto:
            print("Saldo insuficiente para el pago del servicio.")
            return

        self.clientes[id_cliente]["saldo"] -= monto
        self.clientes[id_cliente]["movimientos"].append((datetime.datetime.now(), f"Pago de servicio '{servicio}': -S/.{monto}"))
    
        # Agregar la transacción al historial del cajero seleccionado
        if self.cajero_seleccionado:
            self.cajero_seleccionado['historial'].append({
                'fecha': datetime.datetime.now(),
                'tipo': 'Pago de servicio',
                'monto': monto,
                'cliente': id_cliente,
                'servicio': servicio
            })
    
        print(f"Pago de servicio '{servicio}' realizado exitosamente por S/.{monto}")

    
    def mostrar_menu(self):
        """Muestra el menú principal para elegir entre cliente o administrador."""
        # Primero seleccionamos el cajero
        self.seleccionar_cajero()
        
        if self.cajero_seleccionado is None:
            print("No se ha seleccionado un cajero válido. Cerrando el sistema.")
            return

        while True:
            print("\n--- Cajero Automático Multifunción ---")
            print("1. Iniciar sesión como cliente")
            print("2. Iniciar sesión como administrador")
            print("3. Cambiar de cajero")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                id_cliente = input("Ingrese su ID de cliente: ").lower()  # Mantiene espacios, convierte a minúsculas
                password = input("Ingrese su contraseña: ")
                if self.validar_cliente(id_cliente, password):
                    self.menu_cliente(id_cliente, password)
                else:
                    print("Cliente o contraseña incorrectos.")
                    
            elif opcion == "2":
                admin_password = input("Ingrese la contraseña de administrador: ")
                if admin_password == "admin123":
                    while True:
                        print("\n--- Menú de Administrador ---")
                        print("1. |Vista Reabastecer billetes|")
                        print("2. |Vista clientes|")
                        print("3. Buscar cajero por ubicación")
                        print("4. Agregar nuevo cajero")
                        print("5. Ver cajeros disponibles")
                        print("6. Ver historial de cajero")
                        print("7. Cerrar sesión")
                        sub_opcion = input("Seleccione una opción: ")
                        
                        if sub_opcion == "1":
                            self.menu_reabastecer()
                        elif sub_opcion == "2":
                            self.menu_ver_clientes()
                        elif sub_opcion == "3":
                            ubicacion_a_buscar = input("Ingrese la ubicación del cajero a buscar: ")
                            cajero_encontrado = self.buscar_cajero_fuerza_bruta(ubicacion_a_buscar)
                            if cajero_encontrado:
                                saldo = self.calcular_saldo(cajero_encontrado)
                                print("Saldo total: S/.", saldo)
                            else:
                                print("No se encontró un cajero en esa ubicación.")
                        elif sub_opcion == "4":
                            while True:
                                ubicacion_nueva = input("Ingrese la ubicación del nuevo cajero: ")
                                if self.validar_ubicacion(ubicacion_nueva):
                                    self.agregar_cajero(ubicacion_nueva)
                                    break  # Sale del ciclo si la ubicación es válida
                        elif sub_opcion == "5":
                            self.mostrar_cajeros()  # Llamar al método que muestra todos los cajeros disponibles
                        elif sub_opcion == "6":
                            if self.cajero_seleccionado:
                                self.mostrar_historial()
                            else:
                                print("No se ha seleccionado un cajero.")

                        elif sub_opcion == "7":
                            print("Cerrando sesión de administrador.")
                            break  # Sale del ciclo y regresa al menú principal
                        else:
                            print("Opción no válida.")
                else:
                    print("Contraseña incorrecta.")
            elif opcion == "3":
                self.seleccionar_cajero()
            elif opcion == "4":
                print("Gracias por usar el cajero automático.")
                break  # Sale del ciclo y termina el programa
            else:
                print("Opción no válida.")
                
    def menu_cliente(self, id_cliente, password):
        print("¡Bienvenido "+id_cliente+"!")
        while True:
            print("--- Menú de Operaciones ---")
            print("1. Consultar saldo")
            print("2. Retirar dinero")
            print("3. Depositar dinero")
            print("4. Transferir dinero")
            print("5. Consultar movimientos")
            print("6. Pagar servicios")
            print("7. Cerrar sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                    print(f"Saldo actual: S/.{self.clientes[id_cliente]['saldo']}")
            
            elif opcion == "2":
                try:
                    monto = float(input("Ingrese el monto a retirar: "))
                    if monto <= 0:
                        print("El monto debe ser mayor que cero.")
                        continue
                    if self.menu_decision("retirar dinero"):
                        self.retirar(id_cliente, password, monto)
                except ValueError:
                    print("Por favor ingrese un monto válido.")
                
            elif opcion == "3":
                print("Ingrese la cantidad de billetes a depositar:")
                billetes_depositados = {}
            
                for denominacion in self.billetes:
                    while True:
                        try:
                            cantidad = input(f"Billetes de S/.{denominacion}: ")
                            cantidad = int(cantidad)
                        
                            if cantidad < 0:
                                print("La cantidad debe ser positiva. Intente nuevamente.")
                            else:
                                billetes_depositados[denominacion] = cantidad
                                break
                        except ValueError:
                            print("Por favor ingrese un número válido para la cantidad de billetes.")
                        
                if sum(billetes_depositados.values()) > 0:
                    if self.menu_decision("depositar dinero"):
                        self.depositar(id_cliente, password, billetes_depositados)
                else:
                    print("No se ha depositado ninguna cantidad válida. La operación ha sido cancelada.")
            
            elif opcion == "4":
                try:
                    id_destino = input("Ingrese el ID del destinatario: ")
                    if id_destino == id_cliente:
                        print("No puedes transferir dinero a tu propia cuenta.")
                        continue
                
                    monto = float(input("Ingrese el monto a transferir: "))
                    if monto <= 0:
                        print("El monto debe ser mayor que cero.")
                        continue
                    if self.menu_decision("transferir dinero"):
                        self.transferir(id_cliente, password, id_destino, monto)
                except ValueError:
                    print("Por favor ingrese un monto válido.")
                
            elif opcion == "5":
                    self.consultar_movimientos(id_cliente, password)
            
            elif opcion == "6":

                while True:
                    servicio = input("Ingrese el nombre del servicio: ")

                    # Verificar que el servicio no sea un número
                    if servicio.isdigit():
                        print("Error: El nombre del servicio no puede ser un número. Por favor, intente nuevamente.")
                        continue  # Volver a pedir el nombre del servicio si es un número

                    while True:  # Bucle para validar el monto
                        try:
                            monto = float(input(f"Ingrese el monto para pagar el servicio '{servicio}': "))
                
                            # Validar que el monto sea mayor que cero
                            if monto <= 0:
                                print("El monto debe ser mayor que cero. Por favor, intente nuevamente.")
                                continue  # Volver a pedir el monto si es inválido

                            # Si pasa la validación, confirmar la operación
                            if self.menu_decision("pagar el servicio"):
                                self.pagar_servicio(id_cliente, password, monto, servicio)
                                break  # Salir del bucle una vez realizada la operación
                            else:
                                break  # Salir del bucle si la decisión es no

                        except ValueError:
                            # En caso de que el monto no sea un número válido
                            print("Error: Por favor ingrese un monto válido (un número positivo).")
        
                    break

            elif opcion == "7":
                print("Cerrando sesión...")
                break
            else:
                print("Opción no válida.")
            
    def menu_decision(self, accion):
        while True:
            decision = input(f"¿Está seguro de que desea {accion}? (s/n): ").lower()
            if decision == 's':
                return True  # Sale del bucle y devuelve True
            elif decision == 'n':
                print("Operación cancelada.")
                return False  # Sale del bucle y devuelve False
            else:
                print("Opción no válida. Por favor, ingrese 's' para sí o 'n' para no.")
                
    def menu_reabastecer(self):
        while True:
            print("--- Menú de Reabastecimiento y Gestión ---")
            print("1. Reabastecer billetes")
            print("2. Mostrar desglose de billetes y saldo total del cajero")
            print("3. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.reabastecer_billetes()
            elif opcion == "2":
                self.mostrar_desglose_billetes()
            elif opcion == "3":
                break
            else:
                print("Opción no válida.")
                
    def reabastecer_billetes(self):
        if not self.cajero_seleccionado:
            print("No se ha seleccionado un cajero.")
            return

        while True:
            print(f"--- Reabastecimiento de Billetes para el cajero en {self.cajero_seleccionado['ubicacion']} ---")
            for denominacion, cantidad in self.cajero_seleccionado["billetes"].items():
                print(f"Billetes de S/.{denominacion}: {cantidad}")

            try:
                denominacion = int(input("Ingrese la denominación de los billetes a reabastecer (200, 100, 50, 20): "))
                # Verificar que la denominación sea válida antes de proceder
                if denominacion not in self.cajero_seleccionado["billetes"]:
                    print("Denominación no válida. Intente nuevamente.")
                    continue

                cantidad = int(input(f"Ingrese la cantidad de billetes de S/.{denominacion}: "))
                # Verificar que la cantidad no sea negativa
                if cantidad < 0:
                    print("La cantidad no puede ser negativa. Intente nuevamente.")
                    continue

                # Si la denominación y la cantidad son válidas, actualizamos el contador
                self.cajero_seleccionado["billetes"][denominacion] += cantidad
                print(f"Billetes de S/.{denominacion} reabastecidos correctamente.")
            except ValueError:
                print("Por favor ingrese una cantidad válida.")
        
            # Preguntar si desea continuar
            decision = input("¿Desea reabastecer otra denominación? (s/n): ").lower()
            if decision != "s":
                break


    def mostrar_desglose_billetes(self):
        if not self.cajero_seleccionado:
            print("No se ha seleccionado un cajero.")
            return

        print(f"--- Desglose de Billetes para el cajero en {self.cajero_seleccionado['ubicacion']} ---")
        total_cajero = 0
        for denominacion, cantidad in self.cajero_seleccionado["billetes"].items():
            subtotal = denominacion * cantidad
            total_cajero += subtotal
            print(f"Billetes de S/.{denominacion}: {cantidad} (Subtotal: S/.{subtotal})")
        print(f"\nSaldo total del cajero: S/.{total_cajero}")
     
        
    def menu_ver_clientes(self):
        # Menú para ver y gestionar clientes desde el administrador
        while True:
            print("\n--- Gestión de Clientes ---")
            print("1. Ver todos los clientes")
            print("2. Ordenar clientes por saldo (Quicksort)")
            print("3. Buscar cliente por ID (Búsqueda binaria)")
            print("4. Crear nuevo cliente")
            print("5. Volver")
            opcion = input("Seleccione una opción: ")

            # Obtener una lista de clientes con su información
            clientes_lista = [{"id": id, **info} for id, info in self.clientes.items()]

            if opcion == "1":
                if not clientes_lista:
                    print("No hay clientes registrados.")
                else:
                    if self.clientes_ordenados:  # Si ya está ordenado, mostrarlo
                        print("--- Todos los Clientes (Ordenados) ---")
                        for cliente in self.clientes_ordenados:
                            print(f"ID: {cliente['id']}, Saldo: S/.{cliente['saldo']}")
                    else:  # Si no está ordenado, mostrar la lista sin ordenar
                        print("--- Todos los Clientes (Sin Ordenar) ---")
                        for cliente in clientes_lista:
                            print(f"ID: {cliente['id']}, Saldo: S/.{cliente['saldo']}")

            elif opcion == "2":
                # Ordenar clientes por saldo usando quicksort y guardar el resultado
                self.clientes_ordenados = self.quicksort(clientes_lista, "saldo")
                print("\nClientes ordenados por saldo y guardados.")
                for cliente in self.clientes_ordenados:
                    print(f"ID: {cliente['id']}, Saldo: S/.{cliente['saldo']}")

            elif opcion == "3":
                # Buscar cliente por ID
                clientes_ordenados = self.quicksort(clientes_lista, "id")
                id_cliente = input("Ingrese el ID del cliente a buscar: ")
                resultado = self.busqueda_binaria(clientes_ordenados, id_cliente)
                if resultado:
                    print(f"Cliente encontrado: ID: {resultado['id']}, Saldo: S/.{resultado['saldo']}")
                else:
                    print("Cliente no encontrado.")
                    
            elif opcion == "4":
                # Opción para crear un nuevo cliente
                while True:
                    id_cliente = input("Ingrese el ID del nuevo cliente: ")
                
                    # Validar que el ID no empiece con un signo negativo
                    if id_cliente.startswith('-'):
                        print("El ID no puede comenzar con un signo negativo. Intente nuevamente.")
                        continue
                
                    # Validar que el ID sea único
                    if id_cliente in self.clientes:
                        print(f"Ya existe un cliente con el ID '{id_cliente}'. Elija otro ID.")
                        continue
                
                    # Si el ID es válido, pedir la contraseña
                    password = input("Ingrese la contraseña del cliente: ")
                
                    # Agregar el cliente
                    self.agregar_cliente(id_cliente, password)
                    print(f"Cliente '{id_cliente}' creado con éxito.")
                    break  # Salir del ciclo de creación de cliente        
            
            elif opcion == "5":
                break
            else:
                print("Opción no válida.")



# Crear una instancia del Cajero y mostrar el menú
cajero = Cajero()

# Agregar algunos clientes con sus respectivas contraseñas y saldos iniciales
cajero.agregar_cliente("manuel", "123", 2000)
cajero.agregar_cliente("wilbert", "345", 800)
cajero.agregar_cliente("jesus", "456", 500)
cajero.agregar_cliente("harold", "234", 1500)

# Mostrar el menú del cajero
cajero.mostrar_menu()