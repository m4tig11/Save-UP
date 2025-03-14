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
###################################
def ventana(app,conn,bdd):
    app.destroy()
    ############################  Ventana ##########################
    app = Tk()
    app.geometry("1391x785")
    app.title("Save Up")
    img_bg_registro = PhotoImage(file = "Imagenes/img_Registro/bg_Registro.png")
    bg_registro = Label(image = img_bg_registro)
    bg_registro.pack()
    app.resizable(width=0, height=0)

    ############################ Entry username ##################################
    ety_username = Entry(bg="White",font=font.Font(family="Yu Gothic UI Semibold", size=15))
    ety_username.place(x=440,y=100,height = 50,width=500)
    ety_username.config(relief = FLAT)

    ############################ Entry contraseña ##################################
    ety_password = Entry(bg="White",font=font.Font(family="Yu Gothic UI Semibold", size=15))
    ety_password.place(x=490,y=205,height = 50,width=500)
    ety_password.config(relief = FLAT)

    ############################ Entry contacto ##################################
    ety_contacto = Entry(bg="White",font=font.Font(family="Yu Gothic UI Semibold", size=15))
    ety_contacto.place(x=455,y=308,height = 50,width=500)
    ety_contacto.config(relief = FLAT)

    ############################ Entry Barrio ##################################
    ety_barrio = Entry(bg="White",font=font.Font(family="Yu Gothic UI Semibold", size=15))
    ety_barrio.place(x=435,y=408,height = 50,width=550)
    ety_barrio.config(relief = FLAT)

    ############################ Checkbox es local ###################################
    global bool_local
    bool_local = 0
    ckb_esLocal = Checkbutton()
    ckb_esLocal.config(bg="light blue",overrelief=GROOVE,relief=FLAT,command=partial(b))
    ckb_esLocal.place(x=520,y=517,height=15,width=15)

    ############################ Boton aceptar ###################################
    img_btn_aceptar = PhotoImage(file = "Imagenes/img_Registro/btn_Aceptar.png")
    btn_aceptar  = Button(image = img_btn_aceptar,height =55,width =200,command=partial(validar_datos,ety_username,ety_password,ety_contacto,ety_barrio,ckb_esLocal,conn,bdd,app))
    btn_aceptar.config(overrelief=GROOVE, relief=FLAT)
    btn_aceptar.place(x=593,y=605)

    ############################ Labels Errores ##########################

    app.mainloop()

####################################################
def validar_datos(eu,ep,ec,eb,cl,conn,bdd,app):
    global bool_local
    global valido
    valido = True
    user = eu.get()
    password = ep.get()
    contacto = ec.get()
    barrio = eb.get()
    esLocal = bool_local%2
    validar_user(user)
    validar_password(password)
    validar_contacto(contacto)
    validar_barrio(barrio)
    if(valido == True):
        registrar_usuario(user,password,contacto,barrio,esLocal,conn,bdd,app)

####################################################
def validar_user(user):
    global valido
    global lbl_largo
    try: 
        lbl_largo.place_forget()
    except NameError:
        nda= ""

    if(len(user) < 8 or len(user)>15):
        valido = False
        lbl_largo = Label(text = "El nombre de usuario debe tener de 8 a 15 caracteres",bg = "light blue",fg = "Red")
        lbl_largo.place(x=335,y=70) 

#########################################################
def validar_password(password):
    global valido
    global lbl_corto
    try: 
        lbl_corto.place_forget()
    except NameError:
        nda= ""

    if(len(password) > 15 or len(password) == 0):
        valido = False
        lbl_corto = Label(text = "La contraseña debe tener como maximo 15 caracteres y minimo 1",bg = "light blue",fg = "Red")
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

###############################################################
def registrar_usuario(user,password,contacto, barrio,es_local,conn,bdd,app):
    global lbl_enuso
    try: 
        lbl_enuso.place_forget()
    except NameError:
        nda= ""

    usuario ='"'+str(user)+'"'
    contraseña ='"'+str(password)+'";'
    txt ="SELECT * FROM Usuarios WHERE username = "+str(usuario)
    datos_usuario = bdd.execute(txt)
    datos_usuario = bdd.fetchall()
    if(datos_usuario == []):
        print("a")
        texto = 'INSERT INTO Usuarios VALUES("{0}","{1}","{2}",{3},"{4}",{5});'.format(user,password,contacto,0,barrio,es_local)
        bdd.execute(texto)
        app.destroy()
        conn.commit()
        if(es_local ==0):
            v_inicio.ventana(user)
        else:
            conn.close()
            v_registrarse_local.ventana(user,contraseña)
            
    else:
        lbl_enuso = Label(text = "Ese nombre de usuario ya esta en uso",bg = "light blue",fg = "Red")
        lbl_enuso.place(x=335,y=70)
        
    return()

###############################################################
def b():
    global bool_local
    bool_local += 1
    return()
