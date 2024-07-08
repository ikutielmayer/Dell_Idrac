import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
from inventory import inventory, load_config
import threading
import os
import sys

def show_loading_window():
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading...")
    loading_label = tk.Label(loading_window, text="Loading Inventory...",  font=(
        "Arial", 16, "bold"), padx=20, pady=20)
    loading_label.pack()

    # Barra de progreso
    progress_bar = ttk.Progressbar(
        loading_window, mode='indeterminate', length=300)
    progress_bar.pack(pady=10)
    progress_bar.start()

    # Caja de texto para mostrar el progreso
    progress_text = tk.Text(loading_window, wrap=tk.WORD, height=10, width=50)
    progress_text.pack(pady=10)
    progress_text.insert(tk.END, "Starting inventory collection...\n")
    
    # Centrar la ventana de carga sobre la ventana principal
    window_width = 500
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    loading_window.geometry(
        f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Mostrar la ventana de carga de forma modal (esperar hasta que se cierre)
    loading_window.transient(root)
    loading_window.grab_set()

    return loading_window, progress_text


def run_inventory():
    pn = option_combobox.get()
    config = load_config(pn)
    
    if not config:
        return
        
    ip = ip_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    loading_window, progress_text = show_loading_window()

    # Crear y arrancar el hilo para ejecutar la tarea en segundo plano
    inventory_thread = threading.Thread(target=load_inventory, args=(loading_window, progress_text, ip, username, password, config, pn))
    inventory_thread.start()


def load_inventory(loading_window, progress_text, ip, username, password, config, pn):
    # Llamar a la función get_inventory
    inventory_data = inventory.get_inventory(ip, username, password, config, pn, progress_text)

    loading_window.destroy()  # Cerrar la ventana de carga

    if inventory_data:
        pn = option_combobox.get()
        show_inventory_html(inventory_data, pn)
    else:
        messagebox.showerror(
            "Error", "Verify Connection to the Lan or IP Address.")


def show_inventory_html(inventory_data, report_title):
    # Generar HTML y abrirlo en el navegador
    html_content = f"""
    <html lang="en">
    <head><title>Inventory Report</title></head>
    <body>
    <h1 style="text-align:center; font-weight:bold;">DC for {report_title}</h1>
    <table class="table" border="1" cellspacing="0" cellpadding="5" style="margin:auto;">
        <thead>
            <tr>
                <th>Details</th>
                <th>Version</th>
            </tr>
        </thead>
         <tbody>
    """

    for section, data in inventory_data.items():
        for key, value in data.items():
            html_content += f"<tr><td>{key}</td><td>{value}</td></tr>"

    html_content += """
        </tbody>
        </table>
    
        <br><br>
            <table class="table" border="0" cellspacing="0" cellpadding="5" style="margin:auto;">
        <tr>
            <td style="text-align:center; font-weight:bold;">Worker:</td>
            <td style="text-align:center; font-weight:bold;">D.C.:</td>
        </tr>
        <tr>
            <td style="text-align:center;"><br><br>______________________<br>Firme</td>
            <td style="text-align:center;"><br><br>______________________<br>Firme</td>
        </tr>

    </body>
    </html>

    """

    with open("inventory_report.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    # Abrir el archivo HTML en el navegador web
    webbrowser.open("inventory_report.html")


# Crear la interfaz gráfica
root = tk.Tk()
root.title("App Inventory")

# Obtener las dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular la posición para centrar la ventana
window_width = 600
window_height = 350
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Establecer la geometría de la ventana
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Etiquetas y campos de entrada para usuario, clave y IP usando grid
username_label = tk.Label(root, text="IPMI User:", font=("Arial", 12, "bold"))
username_label.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
username_entry = tk.Entry(root, font=("Arial", 12, "bold"))
username_entry.grid(row=0, column=1, padx=5, pady=5)
username_entry.insert(0, "root")

password_label = tk.Label(root, text="Password:", font=("Arial", 12, "bold"))
password_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
password_entry = tk.Entry(root, show="*", font=("Arial", 12, "bold"))
password_entry.grid(row=1, column=1, padx=5, pady=5)
password_entry.insert(0, "P@ssw0rd")

ip_label = tk.Label(root, text="IP Address:", font=("Arial", 12, "bold"))
ip_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
ip_entry = tk.Entry(root, font=("Arial", 12, "bold"))
ip_entry.grid(row=2, column=1, padx=5, pady=5)
ip_entry.insert(0, "192.168.0.")

# Separador
tk.Frame(height=2, bd=1, relief=tk.SUNKEN).grid(
    row=3, columnspan=2, sticky="we", padx=5, pady=5)

# Resto del formulario como antes
title_label = tk.Label(root, text="Dell Servers", font=("Arial", 16, "bold"))
title_label.grid(row=4, columnspan=2, pady=10)

choice_label = tk.Label(root, text="Choose P/N:", font=("Arial", 12, "bold"))
choice_label.grid(row=5, column=0, sticky=tk.E, padx=5, pady=5)

option_var = tk.StringVar()
option_combobox = ttk.Combobox(root, textvariable=option_var, values=[
                               "APP-R760XL-PR10st","APP-R760XL-RMS"])
option_combobox.grid(row=5, column=1, padx=5, pady=5)

# Botón RUN más ancho
run_button = tk.Button(root, text="RUN", width=20,
                       height=2, command=run_inventory)
run_button.grid(row=7, column=1, columnspan=2, pady=10)

# Ejecutar la aplicación
root.mainloop()
