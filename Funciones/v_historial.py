import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from functools import partial
import sqlite3 
import os
import tkinter as tk 
from Funciones import v_inicio
from Funciones import v_tienda
from Funciones import v_gastos 
from datetime import datetime
from tkinter import font
def ventana(user,app):
    app.destroy()
    app = Tk()
    app.attributes('-fullscreen',False)
    app.geometry("1366x765")
    app.title("Save Up")
    img_bg_historial = PhotoImage(file = "Imagenes/img_historial/bg_historial.png")
    bg_historial = Label(image = img_bg_historial)
    bg_historial.pack()
    dias = []
    for i in range(1,31):
        dias.append(str(agregarcero(i)))
    gastosxdia = []
    for i in range(1,31):
        gastosxdia.append(int(gastos_dia(user,dias[i-1])))

    fig, ax = plt.subplots(figsize=(11.8,6.7))
    ax.set_ylabel('Gastos')
    ax.set_title('Gastos por dia')
    plt.bar(dias, gastosxdia)
    plt.savefig('barras_simple.png')
    barras_hist = PhotoImage(file = 'barras_simple.png')
    grafico = Label(image = barras_hist)
    grafico.place(x= 160,y = 82)


    ############################# Label user ###############################
    lbl_user = Label(text = user ,bg = "light grey",fg = "Black", font=font.Font(family="Segoe UI Semibold"))
    lbl_user.place(x=1193,y=43)
    
    ############################ boton INICIO #######################
    img_btn_inicio = PhotoImage(file = "Imagenes/img_gastos/btn_inicio.png")
    btn_inicio  = Button(image = img_btn_inicio,height =71,width =73,command=partial(inicio,user,app))
    btn_inicio.config(overrelief=GROOVE, relief=FLAT)
    btn_inicio.place(x=13.5,y=182.5)

    ############################ boton Gastos #######################
    img_btn_gastos = PhotoImage(file = "Imagenes/img_Inicio/btn_gastos.png")
    btn_gastos  = Button(image = img_btn_gastos,height =70,width =70,command=partial(v_gastos.ventana,user,app))
    btn_gastos.config(overrelief=GROOVE, relief=FLAT)
    btn_gastos.place(x=15,y=388)
    
    
    ############################ boton Tienda #######################
    img_btn_tienda = PhotoImage(file = "Imagenes/img_Inicio/btn_tienda.png")
    btn_tienda  = Button(image = img_btn_tienda,height =75,width =77,command=partial(tienda,user,app))
    btn_tienda.config(overrelief=GROOVE, relief=FLAT)
    btn_tienda.place(x=11,y=283)


    ############################ boton Cerrar sesion #######################
    img_btn_out = PhotoImage(file = "Imagenes/img_Inicio/btn_cerrarSesion.png")
    btn_out  = Button(image = img_btn_out,height =48,width =44,command = partial(cerrarSesion,app))
    btn_out.config(overrelief=GROOVE, relief=FLAT)
    btn_out.place(x=30,y=610)
    app.mainloop()




def agregarcero(valor):
    return f"{valor:02d}"


def cerrarSesion(app):
    os.remove('user.txt')
    app.destroy()
    return()

def inicio(user,app):
    app.destroy()
    v_inicio.ventana(user)

def tienda(user,app):
    app.destroy()
    v_tienda.ventana(user)

def gastos_dia(user,dia):
    conn = sqlite3.connect("Base de datos/BDD_Save_up.db")
    bdd = conn.cursor()
    us ='"'+str(user)+'"'
    fecha = "2022-11"
    fecha +="-"+str(dia)
    txt ="SELECT SUM(precio) FROM Gastos WHERE username = "+str(us)+"and (fecha LIKE '"+str(fecha)+"%')"
    bdd.execute(txt)
    total = bdd.fetchall()
    total = str(total)
    total = total[:-3]
    total  = total[2:]
    conn.close()
    if(total == "None"):
        return(0)
    else :
        return(total)
    
