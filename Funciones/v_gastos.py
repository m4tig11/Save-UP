#####IMPORT#######################
from tkinter import *                                     ##
from tkinter import ttk                                  ##
import tkinter as tk                                        ##          
from functools import partial                         ##
import sqlite3                                                ##                 
from tkinter import font
import os
from Funciones import v_inicio
from Funciones import v_tienda
from Funciones import v_historial
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
#####################################
def ventana(user,app):
    app.destroy()
    app = Tk()
    app.attributes('-fullscreen',False)
    app.geometry("1366x765")
    app.title("Save Up")
    img_bg_gastos = PhotoImage(file = "Imagenes/img_gastos/bg_gastos.png")
    bg_gastos = Label(image = img_bg_gastos)
    bg_gastos.pack()

    colores = ["Green","Turquoise","Blue","Orange","Yellow","gold","lightgreen","Brown","Red","darkred","LightBlue","magenta","Purple","Pink","Gray"]
    categorias = ["Supermercado","Kiosco","Inversion","Comida","Viajes","Regalos","Ahorros","Mascotas","Transporte","Hijos","Servicios","Shopping","Salud","Alquiler","Otro"] 
    valores = []
    categorias_filtradas = []
    global r
    r = 0
    
    for i in range(15):
        valor = gastos(user, categorias[i])
        if valor > 0:  # Filtrar valores 0
            valores.append(valor)
            categorias_filtradas.append(categorias[i])
    
    if valores:
        fig1, ax1 = plt.subplots(figsize=(6,7.2))
        ax1.pie(valores, labels=categorias_filtradas, startangle=90, colors=colores[:len(valores)], autopct="%0.1f %%")
        ax1.axis('equal')
        plt.title("Gastos del mes")
        plt.legend(labels=valores, loc="lower center", bbox_to_anchor=(-0.1,-0.2))
        plt.savefig('grafica_pastel.png')
        grafico = PhotoImage(file='grafica_pastel.png')
        lbl_gra = Label(image=grafico)
        lbl_gra.place(x=138,y=20,width=590,height=720)
    
    app.mainloop()

def gastos(user,categoria):
    global r 
    conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
    bdd = conn.cursor()
    us = '"'+str(user)+'"'
    categoria = '"'+str(categoria)+'"'
    month = "2022-11"
    txt = "SELECT SUM(precio) FROM Gastos WHERE username = "+str(us)+" and categoria ="+categoria+" and (fecha LIKE '"+str(month)+"%')"
    bdd.execute(txt)
    cat = bdd.fetchone()[0]
    conn.close()
    
    return int(cat) if cat else 0

def cerrarSesion(app):
    os.remove('user.txt')
    app.destroy()
    return()

def inicio(user,app):
    app.destroy()
    v_inicio.ventana(user)

def agregarGastos(ety,categoria,user):
    monto = ety.get()
    if not monto.isnumeric():
        lbl_numerico = Label(text="Solo se pueden insertar numeros", bg="SkyBlue4", fg="red3", font=font.Font(family="Segoe UI Semibold"))
        lbl_numerico.place(x=886,y=100)
        return()
    
    monto = int(monto)
    fecha = datetime.now()
    conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
    bdd = conn.cursor()
    txt = "INSERT INTO Gastos(precio,categoria,fecha,username) values({0},'{1}','{2}','{3}')".format(monto,categoria,fecha,user)
    bdd.execute(txt)
    
    txt = "SELECT saldo FROM Usuarios WHERE username = '"+user+"'"
    bdd.execute(txt)
    saldo = bdd.fetchone()
    if saldo:
        saldo = saldo[0] - monto
        txt = "UPDATE Usuarios SET saldo ="+str(saldo)+" WHERE username ='"+user+"'"
        bdd.execute(txt)
    
    conn.commit()
    conn.close()
    return()

def tienda(user,app):
    app.destroy()
    v_tienda.ventana(user)
