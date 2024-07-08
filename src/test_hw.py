import paramiko
import json

def get_hwinventory(ip, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, username=username, password=password)
        command = "racadm hwinventory"
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if error:
            print(f"Error al ejecutar {command}: {error}")
            return None

        inventory = parse_hwinventory_output(output)
        return inventory

    except Exception as e:
        print(f"Error al conectar al servidor: {e}")
        return None
    finally:
        ssh.close()

def parse_hwinventory_output(output):
    inventory = {}
    lines = output.splitlines()
    current_section = None

    for line in lines:
        if line.startswith('FQDD ='):
            current_section = line.split('FQDD =')[1].strip()
            inventory[current_section] = {}
        elif '=' in line and current_section is not None:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            inventory[current_section][key] = value

    return inventory

def save_inventory_to_json(inventory, filename):
    with open(filename, 'w') as json_file:
        json.dump(inventory, json_file, indent=4)

def filter_inventory(inventory, keys_of_interest):
    filtered_inventory = {}

    for section, details in inventory.items():
        filtered_details = {key: value for key, value in details.items() if key in keys_of_interest}
        if filtered_details:
            filtered_inventory[section] = filtered_details

    return filtered_inventory

if __name__ == "__main__":
    ip = "192.168.0.138"
    username = "root"
    password = "P@ssw0rd"

    inventory = get_hwinventory(ip, username, password)
    if inventory:
        save_inventory_to_json(inventory, 'hwinventory.json')
        print("Inventario guardado en hwinventory.json")

        # Define las claves que te interesan
        keys_of_interest = ["ElementName", "Current Version", "FQDD", "Status"]

        # Filtrar el inventario
        filtered_inventory = filter_inventory(inventory, keys_of_interest)

        # Imprimir el inventario filtrado
        for section, details in filtered_inventory.items():
            print(f"\n=== {section} ===")
            for key, value in details.items():
                print(f"{key}: {value}")
    else:
        print("No se pudo obtener el inventario.")
