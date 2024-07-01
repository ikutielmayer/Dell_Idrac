import paramiko
import os

def export_support_collection(ip, username, password, output_file):
    # Crear un cliente SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Conectar al servidor
        ssh.connect(ip, username=username, password=password)

        # Comando para exportar el SupportAssist Collection log
        command = f"racadm supportassist collect -f {output_file}"

        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if error:
            print(f"Error al ejecutar {command}: {error}")
            return False
        else:
            print(f"Support collection log exportado exitosamente a {output_file}")

            # Descargar el archivo generado al PC local
            sftp = ssh.open_sftp()
            remote_path = f"/root/{output_file}"  # Cambia esto según la ubicación remota
            local_path = os.path.join(os.getcwd(), output_file)

            sftp.get(remote_path, local_path)
            sftp.close()
            print(f"Archivo descargado exitosamente a {local_path}")
            return True

    except Exception as e:
        print(f"Error al conectar al servidor: {e}")
        return False
    finally:
        ssh.close()

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
    password = "P@ssw0rd"  # Asegúrate de usar la contraseña correcta
    output_file = "support_collection.zip"

    export_support_collection(ip, username, password, output_file)
