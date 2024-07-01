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
            "BOSS": "racadm swinventory",
            "IRC": "racadm swinventory",
            "ServiceTag": "racadm get system.serverinfo.servicetag",
            "BIOS.Setup.1-1#ProcSettings": "racadm get BIOS.ProcSettings.proc2brand",
            "HostName": "racadm get system.ServerOS.HostName",
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
                case "BOSS":
                    inventory[key] = extract_boss_version(output)
                case "IRC":
                    inventory[key] = extract_irc_version(output)
                case "ServiceTag":
                    inventory[key] = parse_ServiceTag_output(output)
                case "HostName":
                    inventory[key] = parse_HostName_output(output)
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
                case "BIOS.Setup.1-1#ProcSettings":
                    inventory["CPU"] = parse_cpu_output(output)
                case _:
                    inventory[key] = parse_inventory_output(output)
            
        return inventory

    except Exception as e:
        print(f"Error al conectar al servidor: {e}")
        return None
    finally:
        ssh.close()


def extract_boss_version(sw_inventory_output):
    lines = sw_inventory_output.splitlines()
    boss_info = {}
    capturing = False

    for line in lines:
        line = line.strip()
        
        if line.startswith("ElementName = BOSS-N1 Monolithic"):
            capturing = True
        if capturing:
            if "Rollback Version" in line:
                capturing = False
            if "Current Version" in line:
                boss_info["BOSS-N1 Monolithic"] = line.split(" = ")[1]
                capturing = False
     
    return boss_info if boss_info else "BOSS-N1 Monolithic - not Found"

def extract_irc_version(sw_inventory_output):
    lines = sw_inventory_output.splitlines()
    irc_info = {}
    capturing = False

    for line in lines:
        line = line.strip()
                
        if line.startswith("ElementName = Integrated Remote Access Controller"):
            capturing = True
        if capturing:
            if "Rollback Version" in line:
                capturing = False
            if "Current Version" in line:
                irc_info["Integrated Remote Access Controller Version"] = line.split(" = ")[1]
                capturing = False

    return irc_info if irc_info else "Integrated Remote Access Controller not Found"


def extract_relevant_sw_info(sw_inventory_output):
    relevant_fields = ["ElementName", "Current Version", "FQDD"]
    relevant_info = []

    lines = sw_inventory_output.splitlines()
    for i in range(len(lines)):
        if any(field in lines[i] for field in relevant_fields):
            
            print(lines[i].strip)
            
            if (lines[i].strip) == "BOSS-N1 Monolithic":
                relevant_info.append(lines[i].strip())
                print(relevant_info)
                
            if (lines[i].strip) == "ElementName = Integrated Remote Access Controller":
                 if 'Integrated Remote Access Controller' in line:
                    key, value = line.split('=', 1)
                    key, value = key.strip(), value.strip()
                    if key == "Integrated Remote Access Controller":
                        Integrated[key] = value
                        print(Integrated[key])
                
    return relevant_info

def parse_HostName_output(output):
    hostname = {}
    lines = output.split('\n')
    
    for line in lines:
        if 'HostName=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "HostName":
                hostname[key] = value

    return hostname
    
def parse_ServiceTag_output(output):
    ServiceTag = {}
    lines = output.split('\n')
    
    for line in lines:
        if 'ServiceTag=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "ServiceTag":
                ServiceTag[key] = value

    return ServiceTag

def parse_cpu_output(output):
    cpu_info = {}
    lines = output.split('\n')
    
    for line in lines:
        if 'proc2brand=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "proc2brand":
                cpu_info[key] = value

    return cpu_info
 
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
