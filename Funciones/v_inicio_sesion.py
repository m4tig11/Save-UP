######IMPORT#######################
from tkinter import *                                     ##
from tkinter import ttk                                  ##
import tkinter as tk                                        ##
from Funciones import v_registrarse           ##
from functools import partial                      ##
import sqlite3                                                ##
from Funciones import v_inicio                   ##
import os
from os import remove                                ##
###################################
def iniciarSesion(e_u,e_p,app):
    global lbl_inc
    try:
        lbl_inc.place_forget()
    except NameError:
        nda= ""
        
    try:
        user = e_u.get()
        password = e_p.get()
    except AttributeError:
        user = e_u
        password = e_p
        
        
    us ='"'+str(user)+'"'
    pas ='"'+str(password)+'";'
    txt ="SELECT * FROM Usuarios WHERE username = "+str(us)+"and contraseña ="+str(pas)
    datos_usuario = bdd.execute(txt)
    datos_usuario = bdd.fetchall()
    if(datos_usuario == []):
        if(os.path.exists("user.txt") == True):
            remove("user.txt")
        lbl_inc = Label(text = "usuario o contraseña incorrecta",bg = "light blue",fg = "Red")
        lbl_inc.place(x=885,y=300)
    else:
        if(os.path.exists("user.txt") == False):
            a = open("user.txt","w")
            a.write(user)
            a.write("\n")
            a.write(password)
            a.close()
            app.destroy()
            conn.close()
            v_inicio.ventana(user)
        else:
            conn.close
            app.destroy()
            v_inicio.ventana(user)
        

############################ Base de datos ######################
conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
bdd = conn.cursor()
############################ inicio automatico ##################
if(os.path.exists("user.txt") == True):
        a = open("user.txt","r")
        c = int(0)
        v = [""]*2
        for i in a.readlines():
            v[c] = i
            c+=1
        username =v[0]
        username = username[:-1]
        password = v[1]
        a.close()
        app = Tk()
        iniciarSesion(username,password,app)
        exit()
############################  Ventana ##########################
app = Tk()
app.geometry("1391x785")
app.title("Save Up")
img_bg_inicio_sesion = PhotoImage(file = "Imagenes/img_InicioSesion/bg_InicioSesion.png")
bg_inicioSesion = Label(image = img_bg_inicio_sesion)
bg_inicioSesion.pack()

############################ Entry username ##################################
ety_username = Entry(bg="White")##ety = Entry
ety_username.place(x=880,y=325,height = 50,width=300)
ety_username.config(relief = FLAT)

############################ Entry contraseña ##################################
ety_contraseña = Entry(bg="White")##ety = Entry
ety_contraseña.place(x=880,y=442,height = 50,width=300)
ety_contraseña.config(relief = FLAT)

############################ Boton Entrar  ####################################
img_btn_entrar = PhotoImage(file = "Imagenes/img_InicioSesion/btn_entrar.png")
btn_entrar  = Button(image = img_btn_entrar,height =33,width =135,command=partial(iniciarSesion,ety_username,ety_contraseña,app))
btn_entrar.config(overrelief=GROOVE, relief=FLAT)
btn_entrar.place(x=960,y=540)

############################ Boton registrarse ###################################
img_btn_registrarse = PhotoImage(file = "Imagenes/img_InicioSesion/btn_registrarse.png")
btn_registrarse  = Button(image = img_btn_registrarse,height =15,width =77,command=partial(v_registrarse.ventana,app,conn,bdd))
btn_registrarse.config(overrelief=GROOVE, relief=FLAT)
btn_registrarse.place(x=986,y=612)




app.mainloop()
