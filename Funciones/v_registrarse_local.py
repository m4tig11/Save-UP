######IMPORT#######################
from tabnanny import check
from tkinter import *                                     ##
from tkinter import ttk                                  ##
import tkinter as tk                                        ##
from functools import partial
from tkinter.tix import TEXT                      ##
from tkinter import font
import sqlite3
from Funciones import v_inicio
from Funciones import v_registrarse_local


def ventana(usr,pasw):
    global app
    global us
    global pas
    us = usr
    pas = pasw
    app = Tk()
    app.geometry("1391x785")
    app.title("Save Up")
    img_bg_registro = PhotoImage(file = "Imagenes/img_Registro/bg_Registro_local.png")
    bg_registro = Label(image = img_bg_registro)
    bg_registro.pack()
    app.resizable(width=0, height=0)
    ############################ Entry username ##################################
    ety_nombre = Entry(bg="White",font=font.Font(family="Yu Gothic UI Semibold", size=15))
    ety_nombre.place(x=570,y=100,height = 50,width=250)
    ety_nombre.config(relief = FLAT)

    ############################ Entry contraseña ##################################
    ety_direc = Entry(bg="White",font=font.Font(family="Yu Gothic UI Semibold", size=15))
    ety_direc.place(x=490,y=205,height = 50,width=500)
    ety_direc.config(relief = FLAT)

    ############################ Entry contacto ##################################
    ety_contacto = Entry(bg="White",font=font.Font(family="Yu Gothic UI Semibold", size=15))
    ety_contacto.place(x=455,y=308,height = 50,width=500)
    ety_contacto.config(relief = FLAT)

    ############################ Entry Barrio ##################################
    ety_barrio = Entry(bg="White",font=font.Font(family="Yu Gothic UI Semibold", size=15))
    ety_barrio.place(x=435,y=408,height = 50,width=550)
    ety_barrio.config(relief = FLAT)

    img_btn_aceptar = PhotoImage(file = "Imagenes/img_Registro/btn_Aceptar.png")
    btn_aceptar  = Button(image = img_btn_aceptar,height =55,width =200,command=partial(validar_datos,ety_nombre,ety_direc,ety_contacto,ety_barrio))
    btn_aceptar.config(overrelief=GROOVE, relief=FLAT)
    btn_aceptar.place(x=593,y=605)
    app.mainloop()





def registrar_local(nombre,direc,contacto,barrio,app):
    global us
    global pas
    ############################ Base de datos ######################
    conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
    bdd = conn.cursor()
    pas = pas[:-1]
    texto = 'INSERT INTO Locales(contraseña,nombre_Local,direccion,contacto,barrio,username) values('+pas+',"'+nombre+'","'+direc+'","'+contacto+'","'+barrio+'","'+us+'")'
    print(texto)
    bdd.execute(texto)
    conn.commit()
    conn.close()
    app.destroy()
    v_inicio.ventana(us)
    



def validar_datos(nombre,direc,contacto,barrio):
    global valido
    valido = True
    validar_nombre(nombre.get())
    validar_direc(direc.get())
    validar_contacto(contacto.get())
    validar_barrio(barrio.get())
    if(valido == True):
        global app
        registrar_local(nombre.get(),direc.get(),contacto.get(),barrio.get(),app)


    
def validar_nombre(nombre):
    global valido
    global lbl_largo
    try: 
        lbl_largo.place_forget()
    except NameError:
        nda= ""

    if( len(nombre)>15):
        valido = False
        lbl_largo = Label(text = "El nombre de usuario debe tener maximo 15 caracteres",bg = "light blue",fg = "Red")
        lbl_largo.place(x=335,y=70) 

#########################################################
def validar_direc(direc):
    global valido
    global lbl_corto
    try: 
        lbl_corto.place_forget()
    except NameError:
        nda= ""

    if(len(direc) > 15 or len(direc) == 0):
        valido = False
        lbl_corto = Label(text = "La direccion debe tener como maximo 15 caracteres y minimo 1",bg = "light blue",fg = "Red")
        lbl_corto.place(x=335,y=170) 

###########################################################
def validar_contacto(contacto):
    global valido
    global lbl_len
    try: 
        lbl_len.place_forget()
    except NameError:
        nda= ""

    if(len(contacto) > 30):
        valido = False
        lbl_len = Label(text = "El contacto debe tener como maximo 30 caracteres",bg = "light blue",fg = "Red")
        lbl_len.place(x=335,y=270) 

##############################################################
def validar_barrio(barrio):
    global valido 
    global lbl_lenb
    try: 
        lbl_lenb.place_forget()
    except NameError:
        nda= ""

    if(len(barrio) > 30 or len(barrio) == 0):
        valido = False
        lbl_lenb = Label(text = "El barrio debe tener como maximo 30 caracteresy minimo 1",bg = "light blue",fg = "Red")
        lbl_lenb.place(x=335,y=375)
    


    
