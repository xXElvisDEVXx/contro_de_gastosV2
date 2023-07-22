import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import calendar
from datetime import datetime
import locale
import pandas as pd
import os

# Configurar el idioma y la moneda a pesos chilenos (CLP)
locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')

def calcular_saldo():
    ingresos = float(entrada_ingresos.get())

    # Calcular gasto total del mes
    gasto_total_mes = sum(sum(gastos['monto'] for gastos in gastos_por_dia[fecha]) for fecha in gastos_por_dia)

    saldo = ingresos - gasto_total_mes
    label_saldo.config(text=f"Saldo restante: {saldo:n} CLP")

def seleccionar_fecha(event):
    fecha_seleccionada = cal.selection_get()
    label_fecha.config(text=f"Fecha seleccionada: {fecha_seleccionada.strftime('%Y-%m-%d')}")
    mostrar_gastos_por_dia(fecha_seleccionada)

def agregar_gasto_diario():
    try:
        fecha = cal.selection_get()
        gasto_dia = float(entrada_gasto_diario.get())
        descripcion_gasto = entrada_descripcion_gasto.get()

        if fecha in gastos_por_dia:
            gastos_por_dia[fecha].append({"descripcion": descripcion_gasto, "monto": gasto_dia})
        else:
            gastos_por_dia[fecha] = [{"descripcion": descripcion_gasto, "monto": gasto_dia}]

        label_gasto_total_mes.config(text=f"Gasto total del mes: {sum(sum(gastos['monto'] for gastos in gastos_por_dia[fecha]) for fecha in gastos_por_dia):n} CLP")

        # Calcular y mostrar el saldo restante de los ingresos mensuales
        ingresos = float(entrada_ingresos.get())
        saldo = ingresos - sum(sum(gastos['monto'] for gastos in gastos_por_dia[fecha]) for fecha in gastos_por_dia)
        label_saldo.config(text=f"Saldo restante: {saldo:n} CLP")

        messagebox.showinfo("Gasto diario agregado", f"Se ha agregado un gasto de {gasto_dia:n} CLP para el día {fecha.strftime('%Y-%m-%d')}.")
        mostrar_gastos_por_dia(fecha)
    except ValueError:
        messagebox.showerror("Error", "Ingresa un valor numérico válido.")

def mostrar_gastos_por_dia(fecha):
    tabla.delete(*tabla.get_children())
    if fecha in gastos_por_dia:
        for gasto in gastos_por_dia[fecha]:
            tabla.insert("", "end", values=(gasto["descripcion"], fecha.strftime('%Y-%m-%d'), f"{gasto['monto']:n} CLP"))

def guardar_datos_excel():
    datos = []
    for fecha, gastos in gastos_por_dia.items():
        for gasto in gastos:
            datos.append([fecha.strftime('%Y-%m-%d'), gasto['descripcion'], gasto['monto']])
    
    df = pd.DataFrame(datos, columns=['Fecha', 'Descripción', 'Monto'])
    df.to_excel('gastos_diarios.xlsx', index=False, engine='openpyxl')
    messagebox.showinfo("Guardado exitoso", "Los datos se han guardado correctamente en el archivo 'gastos_diarios.xlsx'.")

def cargar_datos_excel():
    if os.path.exists('gastos_diarios.xlsx'):
        df = pd.read_excel('gastos_diarios.xlsx', engine='openpyxl')
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')
        for index, row in df.iterrows():
            fecha = row['Fecha'].date()
            descripcion = row['Descripción']
            monto = row['Monto']
            if fecha in gastos_por_dia:
                gastos_por_dia[fecha].append({"descripcion": descripcion, "monto": monto})
            else:
                gastos_por_dia[fecha] = [{"descripcion": descripcion, "monto": monto}]

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Control de Gastos Mensuales")

# Variables para almacenar los gastos por día
gastos_por_dia = {}

# Cargar datos del archivo Excel al inicio
cargar_datos_excel()

# Crear etiqueta y entrada para ingresos mensuales
etiqueta_ingresos = tk.Label(ventana, text="Ingresos mensuales:")
etiqueta_ingresos.grid(row=0, column=0, padx=10, pady=5)
entrada_ingresos = tk.Entry(ventana)
entrada_ingresos.grid(row=0, column=1, padx=10, pady=5)

# Calendario en español
cal = Calendar(ventana, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, locale='es_ES')
cal.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Etiqueta para mostrar fecha seleccionada
label_fecha = tk.Label(ventana, text="Fecha seleccionada: ")
label_fecha.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Etiqueta y entrada para agregar gasto diario
etiqueta_gasto_diario = tk.Label(ventana, text="Agregar gasto diario:")
etiqueta_gasto_diario.grid(row=3, column=0, padx=10, pady=5)
entrada_gasto_diario = tk.Entry(ventana)
entrada_gasto_diario.grid(row=3, column=1, padx=10, pady=5)

etiqueta_descripcion_gasto = tk.Label(ventana, text="Descripción del gasto:")
etiqueta_descripcion_gasto.grid(row=4, column=0, padx=10, pady=5)
entrada_descripcion_gasto = tk.Entry(ventana)
entrada_descripcion_gasto.grid(row=4, column=1, padx=10, pady=5)

# Botón para agregar gasto diario
boton_agregar_gasto = tk.Button(ventana, text="Agregar Gasto Diario", command=agregar_gasto_diario)
boton_agregar_gasto.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Etiqueta para mostrar el gasto total del mes en pesos chilenos
label_gasto_total_mes = tk.Label(ventana, text="Gasto total del mes: ")
label_gasto_total_mes.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Etiqueta para mostrar el saldo restante de los ingresos mensuales en pesos chilenos
label_saldo = tk.Label(ventana, text="Saldo restante: ")
label_saldo.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

# Crear tabla de gastos por día
tabla = ttk.Treeview(ventana, columns=("Descripción", "Fecha", "Monto"))
tabla.heading("#1", text="Descripción")
tabla.heading("#2", text="Fecha")
tabla.heading("#3", text="Monto")
tabla.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Botón para guardar los datos en un archivo Excel
boton_guardar_excel = tk.Button(ventana, text="Guardar en Excel", command=guardar_datos_excel)
boton_guardar_excel.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

ventana.mainloop()
