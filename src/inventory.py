import paramiko
from prettytable import PrettyTable
import time
import tkinter as tk
from tkinter import messagebox, ttk

ServiceTag = ""

def load_config(app_name):
    config = {}
    config_path = f"C:/Dell/{app_name}.txt"

    try:
        with open(config_path, "r") as file:
                for line in file:
                    key, value = line.strip().split(" = ")
                    config[key] = value
    except:
        messagebox.showerror("Error", "Please, Select P/N")
  
    return config

class inventory():
    def get_inventory(ip, username, password, config, pn, progress_text):
        if pn == "APP-R760XL-RMS":
            idrac_service = config['idrac_service'] 
            backplane0 = config['backplane0'] 
            backplane1 = config['backplane1']
            broadcom  = config['broadcom']
            perc = config['perc']
            netxtreme = config['netxtreme']
            identity = config['identity']
            bios = config['bios']
            driverpack = config['driverpack']
            idrac = config['idrac']
            diagnostic = config['diagnostic']
            cpld = config['cpld']
            lifecycle = config['lifecycle']
            license = config['License']
             # Comandos para obtener información de la BIOS y el firmware
            commands = {
                "Idrac Service Module": "racadm swinventory",
                "Backplane 0": "racadm swinventory",
                "Backplane 1": "racadm swinventory",
                "Broadcom Adv. Dual 10GBASE-T Ethernet 1": "hwinventory NIC.Integrated.1-1-1",
                "Broadcom Adv. Dual 10GBASE-T Ethernet 2": "hwinventory NIC.Integrated.1-2-1",
                "Perc H755 Adapter": "racadm swinventory",
                "BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 1": "hwinventory NIC.Integrated.1-1-1",
                "BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 2": "hwinventory NIC.Integrated.1-2-1",
                "Identity Module(YF71J)": "racadm swinventory",
                "BIOS": "racadm getversion -f bios",
                "Dell OS Driver Pack": "racadm swinventory",
                "Integrated Remote Access Controller": "racadm swinventory",
                "Dell 64 Bit uEFI Diagnostics": "racadm swinventory",
                "Lifecycle Controller": "racadm getversion -f lc",
                "CPLD Version": "racadm getversion -c",
                "License": "racadm license view",
                "HostName": "racadm get system.ServerOS.HostName"
            }
            
        if pn == "APP-R760XL-PR10st":
            boss = config['boss']
            irc = config['irc'] 
            bios = config['bios']
            driverpack = config['driverpack'] 
            idrac = config['idrac']
            backplane = config['backplane'] 
            cpld = config['cpld'] 
            lifecycle = config['lifecycle'] 
            license = config['License'] 
            broadcom = config['broadcom'] 
            netxtreme = config['netxtreme'] 
            
             # Comandos para obtener información de la BIOS y el firmware
            commands = {
                "Idrac Service Module": "racadm swinventory",
                "Backplane 0": "racadm swinventory",
                "Backplane 1": "racadm swinventory",
                "ServiceTag": "racadm get system.serverinfo.servicetag",
                "BOSS": "racadm swinventory",
                "iDRAC": "racadm getversion -f idrac",
                "Backplane 1": "racadm swinventory", 
                "Broadcom Adv. Dual 25Gb Ethernet 1": "hwinventory NIC.Slot.6-1-1",
                "Broadcom Adv. Dual 25Gb Ethernet 2": "hwinventory NIC.Slot.6-2-1",
                "Broadcom NetXtreme Gigabit Ethernet (BCM5720) 1": "hwinventory NIC.Embedded.1-1-1",
                "Broadcom NetXtreme Gigabit Ethernet (BCM5720) 2": "hwinventory NIC.Embedded.2-1-1",
                "IRC": "racadm swinventory",
                "HostName": "racadm get system.ServerOS.HostName",
                "BIOS": "racadm getversion -f bios",
                "Dell OS Driver Pack": "racadm swinventory",
                "Lifecycle Controller": "racadm getversion -f lc",
                "CPLD Version": "racadm getversion -c",
                "License": "racadm license view"
            }
            
        # Crear un cliente SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Conectar al servidor
            ssh.connect(ip, username=username, password=password)
            progress_text.insert(tk.END, "Connected to server...\n")
            progress_text.see(tk.END)
            progress_text.update_idletasks()
            
           

            inventory = {}
                
            for key, command in commands.items():
                stdin, stdout, stderr = ssh.exec_command(command)
                output = stdout.read().decode().strip()
                error = stderr.read().decode().strip()

                progress_text.insert(tk.END, f"Executing {key} command...\n")
                progress_text.see(tk.END)
                progress_text.update_idletasks()
                time.sleep(0.5)    
            
                if error:
                    progress_text.insert(tk.END, f"Error executing {command}: {error}\n")
                    progress_text.see(tk.END)
                    progress_text.update_idletasks()
                    continue

                match key:
                    case "Dell 64 Bit uEFI Diagnostics":
                        inventory[key] = parse_Diagnostics_output(output, diagnostic)
                    case "Idrac Service Module":
                        inventory[key] = parse_idrac_service_output(output, idrac_service)
                    case "Backplane 0":
                       inventory[key] = parse_backplane0_output(output, backplane0)
                    case "Backplane 1":
                        inventory[key] = parse_backplane1_output(output, backplane1)
                    case "Perc H755 Adapter":
                        inventory[key] = parse_perc_output(output, perc)  
                    case "Identity Module(YF71J)":
                        inventory[key] = parse_identity_output(output, identity)
                    case "Broadcom Adv. Dual 10GBASE-T Ethernet 1":
                        inventory[key] = extract_Broadcom10_version1(output, broadcom)  
                    case "Broadcom Adv. Dual 10GBASE-T Ethernet 2":
                        inventory[key] = extract_Broadcom10_version2(output, broadcom)  
                             
                    case "Broadcom Adv. Dual 25Gb Ethernet 1":
                        inventory[key] = extract_Broadcom_version1(output, broadcom)
                    case "Broadcom Adv. Dual 25Gb Ethernet 2":
                        inventory[key] = extract_Broadcom_version2(output, broadcom)
                    case "BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 1":
                        inventory[key] = extract_BCM57416_version1(output, netxtreme)
                    case "BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 2":
                        inventory[key] = extract_BCM57416_version2(output, netxtreme)    
                    case "Broadcom NetXtreme Gigabit Ethernet (BCM5720) 1":
                        inventory[key] = extract_NetXtreme_version1(output, netxtreme)
                    case "Broadcom NetXtreme Gigabit Ethernet (BCM5720) 2":
                        inventory[key] = extract_NetXtreme_version2(output,netxtreme)
                    case "BOSS":
                        inventory[key] = extract_boss_version(output, boss)
                    case "IRC":
                        inventory[key] = extract_irc_version(output, irc)
                    case "ServiceTag":
                        inventory[key] = parse_ServiceTag_output(output)
                        ServiceTag = inventory[key]
                    case "HostName":
                        inventory[key] = parse_HostName_output(output)
                    case "iDRAC":
                        inventory[key] = parse_idrac_output(output, idrac)
                    case "Integrated Remote Access Controller":
                         inventory[key] = extract_irac_version(output, idrac)
                    case "BIOS":
                        inventory[key] = parse_bios_output(output, bios)
                    case "Dell OS Driver Pack":
                        inventory[key] = parse_DriverPack_output(output, driverpack)
                    case "Lifecycle Controller":
                        inventory[key] = parse_Lifecycle_output(output,lifecycle)
                    case "CPLD Version":
                        inventory[key] = parse_cpld_output(output,cpld)
                    case "License":
                        inventory[key] = parse_license_output(output)
                    case _:
                        inventory[key] = parse_inventory_output(output)

                progress_text.insert(tk.END, f"{key} data collected.\n")
                progress_text.see(tk.END)
                progress_text.update_idletasks() 
                 
            return inventory

        except Exception as e:
            print(f"ERROR : {e}\n")
            
            progress_text.insert(tk.END, f"ERROR Connecting to the Server: {e}\n")
            progress_text.see(tk.END)
            progress_text.update_idletasks() 
            return None
        finally:
            ssh.close()
            progress_text.insert(tk.END, "Disconnected from server.\n")
            progress_text.see(tk.END)
            progress_text.update_idletasks() 


# Integrated Remote Access Controller

def extract_irac_version(sw_inventory_output, irac):
    lines = sw_inventory_output.splitlines()
    irac_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("ElementName = Integrated Remote Access Controller"):
            capturing = True
        if capturing:
            if "Rollback Version" in line:
                capturing = False
            if "Current Version" in line:
                irac_info["Integrated Remote Access Controller"] = line.split(" = ")[1]
                if irac_info["Integrated Remote Access Controller"] == irac:
                    irac_info["Integrated Remote Access Controller"] = irac_info["Integrated Remote Access Controller"] + " - PASS"
                    capturing = False
                    return irac_info if irac_info else "Idrac Service Module - not Found"

    return irac_info if irac_info else "Idrac Service Module - not Found"


def parse_backplane0_output(sw_inventory_output, backplane0):
    lines = sw_inventory_output.splitlines()
    backplane0_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("ElementName = Backplane 0"):
            capturing = True
        if capturing:
            if "Rollback Version" in line:
                capturing = False
            if "Current Version" in line:
                backplane0_info["Backplane 0"] = line.split(" = ")[1]
                if backplane0_info["Backplane 0"] == backplane0:
                    backplane0_info["Backplane 0"] = backplane0_info["Backplane 0"] + " - PASS"
                    capturing = False
                    return backplane0_info if backplane0_info else "Idrac Service Module - not Found"

    return backplane0_info if backplane0_info else "Idrac Service Module - not Found"


# parse_identity_output

def parse_identity_output(sw_inventory_output, identity):
    lines = sw_inventory_output.splitlines()
    identity_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("ElementName = Identity Module(YF71J)"):
            capturing = True
        if capturing:
            if "Rollback Version" in line:
                capturing = False
            if "Current Version" in line:
                identity_info["Identity Module(YF71J)"] = line.split(" = ")[1]
                if identity_info["Identity Module(YF71J)"] == identity:
                    identity_info["Identity Module(YF71J)"] = identity_info["Identity Module(YF71J)"] + " - PASS"
                    capturing = False
                    return identity_info if identity_info else "PIdentity Module(YF71J) - not Found"

    return identity_info if identity_info else "Identity Module(YF71J) - not Found"

def parse_perc_output(sw_inventory_output, perc):
    lines = sw_inventory_output.splitlines()
    perc_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("ElementName = PERC H755 Adapter"):
            capturing = True
        if capturing:
            if "Rollback Version" in line:
                capturing = False
            if "Current Version" in line:
                perc_info["Perc H755 Adapter"] = line.split(" = ")[1]
                if perc_info["Perc H755 Adapter"] == perc:
                    perc_info["Perc H755 Adapter"] = perc_info["Perc H755 Adapter"] + " - PASS"
                    capturing = False
                    return perc_info if perc_info else "PERC H755 Adapter - not Found"

    return perc_info if perc_info else "PERC H755 Adapter - not Found"

# parse_Diagnostics_output

def parse_Diagnostics_output(sw_inventory_output, diagnostic):
    lines = sw_inventory_output.splitlines()
    diag_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("ElementName = Dell 64 Bit uEFI Diagnostics"):
            capturing = True
        if capturing:
            if "Rollback Version" in line:
                capturing = False
            if "Current Version" in line:
                diag_info["Dell 64 Bit uEFI Diagnostics"] = line.split(" = ")[1]
                if diag_info["Dell 64 Bit uEFI Diagnostics"] == diagnostic:
                    diag_info["Dell 64 Bit uEFI Diagnostics"] = diag_info["Dell 64 Bit uEFI Diagnostics"] + " - PASS"
                    capturing = False
                    return diag_info if diag_info else "Dell 64 Bit uEFI Diagnostics - not Found"

    return diag_info if diag_info else "Dell 64 Bit uEFI Diagnostics - not Found"

def parse_backplane1_output(sw_inventory_output, backplane1):
    lines = sw_inventory_output.splitlines()
    backplane1_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("ElementName = Backplane 1"):
            capturing = True
        if capturing:
            if "Rollback Version" in line:
                capturing = False
            if "Current Version" in line:
                backplane1_info["Backplane 1"] = line.split(" = ")[1]
                if backplane1_info["Backplane 1"] == backplane1:
                    backplane1_info["Backplane 1"] = backplane1_info["Backplane 1"] + " - PASS"
                    capturing = False
                    return backplane1_info if backplane1_info else "Idrac Service Module - not Found"

    return backplane1_info if backplane1_info else "Idrac Service Module - not Found"

def parse_idrac_service_output(sw_inventory_output, idrac_service):
    lines = sw_inventory_output.splitlines()
    idrac_service_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("ElementName = Dell iDRAC Service Module Embedded Package v5.3.0.0, A00"):
            capturing = True
        if capturing:
            if "Rollback Version" in line:
                capturing = False
            if "Current Version" in line:
                idrac_service_info["Dell iDRAC Service Module"] = line.split(" = ")[1]
                if idrac_service_info["Dell iDRAC Service Module"] == idrac_service:
                    idrac_service_info["Dell iDRAC Service Module"] = idrac_service_info["Dell iDRAC Service Module"] + " - PASS"
                    capturing = False
                    return idrac_service_info if idrac_service_info else "Idrac Service Module - not Found"

    return idrac_service_info if idrac_service_info else "Idrac Service Module - not Found"

def filter_inventory(inventory, keys_of_interest):
    filtered_inventory = {}

    for section, details in inventory.items():
        filtered_details = {key: value for key, value in details.items() if key in keys_of_interest}
        if filtered_details:
            filtered_inventory[section] = filtered_details

    return filtered_inventory

def parse_DriverPack_output(sw_inventory_output, driverpack):
    lines = sw_inventory_output.splitlines()
    dp_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("ElementName = Dell OS Driver Pack, 24.01.05, A00"):
            capturing = True
        if capturing:
            if "Rollback Version" in line:
                capturing = False
            if "Current Version" in line:
                dp_info["DriverPack"] = line.split(" = ")[1]
                if dp_info["DriverPack"] == driverpack:
                    dp_info["DriverPack"] = dp_info["DriverPack"] + " - PASS"
                    capturing = False
                    return dp_info if dp_info else "DriverPack - not Found"

    return dp_info if dp_info else "DriverPack - not Found"

#ElementName = TPM
#Current Version = 7.2.3.1


def extract_backplane_version(sw_inventory_output, backplane):
    lines = sw_inventory_output.splitlines()
    backplane_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("ElementName = Backplane 1"):
            capturing = True
        if capturing:
            if "Rollback Version" in line:
                capturing = False
            if "Current Version" in line:
                backplane_info["Backplane 1"] = line.split(" = ")[1]
                print(backplane_info["Backplane 1"])
                if backplane_info["Backplane 1"].strip() == backplane:
                    backplane_info["Backplane 1"] = backplane_info["Backplane 1"] + " - PASS"
                    capturing = False
                    return backplane_info if backplane_info else "Backplane 1 - Not Found"

    return backplane_info if backplane_info else "Backplane 1 - Not Found"

# DeviceDescription = Integrated NIC 1 Port 1 Partition 1
# DeviceDescription = Integrated NIC 1 Port 2 Partition 1

def extract_Broadcom10_version2(sw_inventory_output, Broadcom):
    lines = sw_inventory_output.splitlines()
    Broadcom_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("Device Description:                           Integrated NIC 1 Port 2 Partition 1"):
            capturing = True
        if capturing:
            if "Family Version" in line:
                Broadcom_info["Broadcom Adv. Dual 10GBASE-T Ethernet 2"] = line.split(":")[1]
                if Broadcom_info["Broadcom Adv. Dual 10GBASE-T Ethernet 2"].strip() == Broadcom:
                    Broadcom_info["Broadcom Adv. Dual 10GBASE-T Ethernet 2"] = Broadcom + " - PASS"
                    capturing = False
                    return Broadcom_info if Broadcom_info else "Broadcom Adv. Dual 10GBASE-T Ethernet 2 - not Found"

    return Broadcom_info if Broadcom_info else "Broadcom Adv. Dual 10GBASE-T Ethernet 2 - not Found"



def extract_Broadcom10_version1(sw_inventory_output, Broadcom):
    lines = sw_inventory_output.splitlines()
    Broadcom_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("Device Description:                           Integrated NIC 1 Port 1 Partition 1"):
            capturing = True
        if capturing:
            if "Family Version" in line:
                Broadcom_info["Broadcom Adv. Dual 10GBASE-T Ethernet 1"] = line.split(":")[1]
                if Broadcom_info["Broadcom Adv. Dual 10GBASE-T Ethernet 1"].strip() == Broadcom:
                    Broadcom_info["Broadcom Adv. Dual 10GBASE-T Ethernet 1"] = Broadcom + " - PASS"
                    capturing = False
                    return Broadcom_info if Broadcom_info else "Broadcom Adv. Dual 10GBASE-T Ethernet 1 - not Found"

    return Broadcom_info if Broadcom_info else "Broadcom Adv. Dual 10GBASE-T Ethernet 1 - not Found"


def extract_Broadcom_version1(sw_inventory_output, Broadcom):
    lines = sw_inventory_output.splitlines()
    Broadcom_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("Device Description:                           NIC in Slot 6 Port 1 Partition 1"):
            capturing = True
        if capturing:
            if "Family Version" in line:
                Broadcom_info["Broadcom Adv. Dual 25Gb Ethernet"] = line.split(":")[1]
                if Broadcom_info["Broadcom Adv. Dual 25Gb Ethernet"].strip() == Broadcom:
                    Broadcom_info["Broadcom Adv. Dual 25Gb Ethernet"] = Broadcom + " - PASS"
                    capturing = False
                    return Broadcom_info if Broadcom_info else "Broadcom Adv. Dual 25Gb Ethernet - not Found"

    return Broadcom_info if Broadcom_info else "Broadcom Adv. Dual 25Gb Ethernet - not Found"

def extract_NetXtreme_version2(sw_inventory_output, NetXtreme):
    lines = sw_inventory_output.splitlines()
    NetXtreme2_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("Device Description:                           Embedded NIC 1 Port 2 Partition 1"):
            capturing = True
        if capturing:
            if "Family Version" in line:
                NetXtreme2_info["Broadcom NetXtreme Gigabit Ethernet (BCM5720) 2"] = line.split(":")[1]
                if NetXtreme2_info["Broadcom NetXtreme Gigabit Ethernet (BCM5720) 2"].strip() == NetXtreme:
                    NetXtreme2_info["Broadcom NetXtreme Gigabit Ethernet (BCM5720) 2"] = NetXtreme + " - PASS"
                    capturing = False
                    return NetXtreme2_info if NetXtreme2_info else "Broadcom NetXtreme Gigabit Ethernet (BCM5720) 2 - not Found"

    return NetXtreme2_info if NetXtreme2_info else "Broadcom NetXtreme Gigabit Ethernet (BCM5720) 2 - not Found"

# extract_BCM57416_version1

def extract_BCM57416_version2(sw_inventory_output, netxtreme):
    lines = sw_inventory_output.splitlines()
    netxtreme2_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("Device Description:                           Integrated NIC 1 Port 2 Partition 1"):
            capturing = True
        if capturing:
            if "Family Version" in line:
                netxtreme2_info["BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 2"] = line.split(":")[1]
                if netxtreme2_info["BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 2"].strip() == netxtreme:
                    netxtreme2_info["BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 2"] = netxtreme + " - PASS"
                    capturing = False
                    return netxtreme2_info if netxtreme2_info else "BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 2 - not Found"

    return netxtreme2_info if netxtreme2_info else "BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 2 - not Found"

def extract_BCM57416_version1(sw_inventory_output, netxtreme):
    lines = sw_inventory_output.splitlines()
    netxtreme1_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("Device Description:                           Integrated NIC 1 Port 1 Partition 1"):
            capturing = True
        if capturing:
            if "Family Version" in line:
                netxtreme1_info["BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 1"] = line.split(":")[1]
                if netxtreme1_info["BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 1"].strip() == netxtreme:
                    netxtreme1_info["BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 1"] = netxtreme + " - PASS"
                    capturing = False
                    return netxtreme1_info if netxtreme1_info else "BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 1 - not Found"

    return netxtreme1_info if netxtreme1_info else "BCM57416 NetXtreme-E Dual-Media 10G RDMA Ethernet Controller 1 - not Found"

# extract_NetXtreme_version1
def extract_NetXtreme_version1(sw_inventory_output, NetXtreme):
    lines = sw_inventory_output.splitlines()
    NetXtreme1_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("Device Description:                           Embedded NIC 1 Port 1 Partition 1"):
            capturing = True
        if capturing:
            if "Family Version" in line:
                NetXtreme1_info["Broadcom NetXtreme Gigabit Ethernet (BCM5720) 1"] = line.split(":")[1]
                if NetXtreme1_info["Broadcom NetXtreme Gigabit Ethernet (BCM5720) 1"].strip() == NetXtreme:
                    NetXtreme1_info["Broadcom NetXtreme Gigabit Ethernet (BCM5720) 1"] = NetXtreme + " - PASS"
                    capturing = False
                    return NetXtreme1_info if NetXtreme1_info else "Broadcom NetXtreme Gigabit Ethernet (BCM5720) 1 - not Found"

    return NetXtreme1_info if NetXtreme1_info else "Broadcom NetXtreme Gigabit Ethernet (BCM5720) 1 - not Found"

def extract_Broadcom_version2(sw_inventory_output, Broadcom):
    lines = sw_inventory_output.splitlines()
    Broadcom2_info = {}
    capturing = False

    for line in lines:
        line = line.strip()

        if line.startswith("Device Description:                           NIC in Slot 6 Port 2 Partition 1"):
            capturing = True
        if capturing:
            if "Family Version" in line:
                Broadcom2_info["Broadcom Adv. Dual 25Gb Ethernet"] = line.split(":")[1]
                if Broadcom2_info["Broadcom Adv. Dual 25Gb Ethernet"].strip() == Broadcom:
                    Broadcom2_info["Broadcom Adv. Dual 25Gb Ethernet"] = Broadcom + " - PASS"
                    capturing = False
                    return Broadcom2_info if Broadcom2_info else "Broadcom Adv. Dual 25Gb Ethernet - not Found"

    return Broadcom2_info if Broadcom2_info else "Broadcom Adv. Dual 25Gb Ethernet - not Found"


def extract_boss_version(sw_inventory_output, boss):
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
                if boss_info["BOSS-N1 Monolithic"] == boss:
                    boss_info["BOSS-N1 Monolithic"] = boss_info["BOSS-N1 Monolithic"] + " - PASS"
                    capturing = False
                    return boss_info if boss_info else "BOSS-N1 Monolithic - not Found"

    return boss_info if boss_info else "BOSS-N1 Monolithic - not Found"

def extract_irc_version(sw_inventory_output, irc):
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
                if irc_info["Integrated Remote Access Controller Version"] == irc:
                    irc_info["Integrated Remote Access Controller Version"] = line.split(" = ")[1] + " - PASS"
                    capturing = False
                    return irc_info if irc_info else "Integrated Remote Access Controller not Found"

    return irc_info if irc_info else "Integrated Remote Access Controller not Found"

def parse_HostName_output(output):
    hostname = {}
    lines = output.split('\n')

    for line in lines:
        if 'HostName=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "HostName":
                hostname[key] = value
                if hostname[key] == "":
                    hostname[key] = "< PASS >"
                    return hostname
                
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



def parse_Lifecycle_output(output,Lifecycle):
    Lifecycle_info = {}
    lines = output.split('\n')

    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "Lifecycle Controller Version":
                Lifecycle_info[key] = value
                if Lifecycle_info["Lifecycle Controller Version"] == Lifecycle:
                    Lifecycle_info["Lifecycle Controller Version"] = Lifecycle_info["Lifecycle Controller Version"] + " - PASS"
                    return Lifecycle_info
                
    return Lifecycle_info

def parse_cpld_output(output, cpld):
    cpdl_info = {}
    lines = output.split('\n')

    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "CPLD Version":
                cpdl_info[key] = value
                if cpdl_info["CPLD Version"] == cpld:
                    cpdl_info["CPLD Version"] = cpdl_info["CPLD Version"] + " - PASS"
                    return cpdl_info
                
    return cpdl_info

def parse_idrac_output(output, idrac):
    idrac_info = {}
    lines = output.split('\n')

    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "iDRAC Version":
                idrac_info[key] = value
                if idrac_info["iDRAC Version"] == idrac:
                    idrac_info["iDRAC Version"] = idrac_info["iDRAC Version"] + " - PASS"
                    return idrac_info
                
    return idrac_info

def parse_bios_output(output, bios):
    bios_info = {}
    lines = output.split('\n')

    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()
            if key == "Bios Version":
                bios_info[key] = value
                if bios_info["Bios Version"] == bios:
                    bios_info["Bios Version"] = bios_info["Bios Version"] + " - PASS"
                    return bios_info

    return bios_info

def parse_license_output(output):
    license_info = {}
    lines = output.split('\n')

    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key, value = key.strip(), value.strip()

            match key:
                case "License Type":
                    if value == "PERPETUAL":
                        license_info[key] = value + " - PASS"
                    else:
                        license_info[key] = value + " - NOT OK"
                case "Status":
                    if value == "OK":
                        license_info[key] = value + " - Good"
                    else:
                        license_info[key] = value + " - Please CHECK"
                case "License Description":
                    if value == "iDRAC9 16G Enterprise License":
                        license_info[key] = value + " - PASS"
                    else:
                        license_info[key] = value + " - NOT OK"

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
