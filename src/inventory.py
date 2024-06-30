import paramiko
from prettytable import PrettyTable

def get_inventory(ip, username, password):
    # Crear un cliente SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Conectar al servidor
        ssh.connect(ip, username=username, password=password)

        # Comandos para obtener información de la BIOS y el firmware
        commands = {
           # "SetGlobal0": "racadm set iDRAC.Users.GlobalUserSetting 0",
            "BIOS": "racadm getversion -f bios",
            "iDRAC": "racadm getversion -f idrac",
            "Lifecycle Controller": "racadm getversion -f lc",
            "CPLD Version": "racadm getversion -c",
            "License": "racadm license view"
        }

        inventory = {}

        for key, command in commands.items():
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if error:
                print(f"Error al ejecutar {command}: {error}")
                continue

            match key:
                case "SetGlobal0":
                    inventory[key] = parse_setglobal0_output(output)
                case "iDRAC":
                    inventory[key] = parse_idrac_output(output)
                case "BIOS":
                    inventory[key] = parse_bios_output(output)
                case "Lifecycle Controller":
                    inventory[key] = parse_Lifecycle_output(output)
                case "CPLD Version":
                    inventory[key] = parse_cpld_output(output)
                case "License":
                    inventory[key] = parse_license_output(output)
                case _:
                    inventory[key] = parse_inventory_output(output)

        return inventory

    except Exception as e:
        print(f"Error al conectar al servidor: {e}")
        return None
    finally:
        ssh.close()


def parse_Lifecycle_output(output):
    Lifecycle_info = {}
    lines = output.split('\n')
    
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "Lifecycle Controller Version":
                Lifecycle_info[key] = value

    return Lifecycle_info


def parse_cpld_output(output):
    cpdl_info = {}
    lines = output.split('\n')
    
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "CPLD Version":
                cpdl_info[key] = value

    return cpdl_info


def parse_idrac_output(output):
    idrac_info = {}
    lines = output.split('\n')
    
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "iDRAC Version":
                idrac_info[key] = value

    return idrac_info


def parse_bios_output(output):
    bios_info = {}
    lines = output.split('\n')
    
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "Bios Version":
                bios_info[key] = value

    return bios_info

def parse_license_output(output):
    license_info = {}
    lines = output.split('\n')
    
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            
            match key:
                case "Unique Identifier":
                    license_info[key] = value
                case "License Type":
                    license_info[key] = value
                case "Status":
                    license_info[key] = value
                case "License Description":
                    license_info[key] = value

    return license_info

def parse_inventory_output(output):
    inventory_info = {}
    lines = output.split('\n')
    
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            inventory_info[key] = value

    return inventory_info

def display_inventory(inventory):
    for section, data in inventory.items():
        print(f"\n=== {section} ===")
        table = PrettyTable()
        table.field_names = ["Clave", "Valor"]
        
        for key, value in data.items():
            table.add_row([key, value])
        
        print(table)

def get_ip_suffix():
    while True:
        ip_suffix = input("Por favor, ingrese los últimos dígitos de la IP (entre 1 y 255): ").strip()
        if ip_suffix.isdigit() and 1 <= int(ip_suffix) <= 255:
            return ip_suffix
        else:
            print("Entrada inválida. Asegúrese de ingresar un número entre 1 y 255.")

if __name__ == "__main__":
    base_ip = "192.168.0."
    ip_suffix = get_ip_suffix()
    ip = base_ip + ip_suffix
    username = "root"
    password = "P@ssw0rd"

    inventory = get_inventory(ip, username, password)
    if inventory:
        display_inventory(inventory)
