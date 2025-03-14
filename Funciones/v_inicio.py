######IMPORT#######################
from tkinter import *                                     ##
from tkinter import ttk                                  ##
import tkinter as tk                                        ##          ##
from functools import partial                      ##
import sqlite3                                                ##                 ##
from tkinter import font
import os
from Funciones import v_gastos
from Funciones import v_tienda
from Funciones import v_historial
from datetime import datetime
###################################

def ventana(user):
    ############################  Ventana ##########################
    app = Tk()
    app.attributes('-fullscreen',False)
    app.geometry("1390x775")
    app.title("Save Up")
    img_bg_inicio = PhotoImage(file = "Imagenes/img_Inicio/bg_inicio.png")
    bg_inicio = Label(image = img_bg_inicio)
    bg_inicio.pack()
    

    ############################ Entry saldo ##################################
    ety_saldo = Entry(bg="SkyBlue4",font=font.Font(family="Yu Gothic UI Semibold", size=15))
    ety_saldo.place(x=298,y=433,height = 36,width=220)
    ety_saldo.config(relief = FLAT)
    
    ############################ boton aceptar #######################
    img_btn_aceptar = PhotoImage(file = "Imagenes/img_Inicio/btn_aceptar.png")
    btn_aceptar  = Button(image = img_btn_aceptar,height =25,width =100,command=partial(cargar_saldo,ety_saldo,user))
    btn_aceptar.config(overrelief=GROOVE, relief=FLAT)
    btn_aceptar.place(x=356,y=509)

    ############################ boton Tienda #######################
    img_btn_tienda = PhotoImage(file = "Imagenes/img_Inicio/btn_tienda.png")
    btn_tienda  = Button(image = img_btn_tienda,height =75,width =77,command =partial(tienda,user,app))
    btn_tienda.config(overrelief=GROOVE, relief=FLAT)
    btn_tienda.place(x=11,y=283)
    
    ############################ boton Gastos #######################
    img_btn_gastos = PhotoImage(file = "Imagenes/img_Inicio/btn_gastos.png")
    btn_gastos  = Button(image = img_btn_gastos,height =70,width =70,command=partial(v_gastos.ventana,user,app))
    btn_gastos.config(overrelief=GROOVE, relief=FLAT)
    btn_gastos.place(x=15,y=388)

    ############################ boton Historial #######################
    img_btn_historial = PhotoImage(file = "Imagenes/img_Inicio/btn_historial.png")
    btn_historial  = Button(image = img_btn_historial,height =70,width =70,command=partial(v_historial.ventana,user,app))
    btn_historial.config(overrelief=GROOVE, relief=FLAT)
    btn_historial.place(x=16.5,y=493)

    ############################ boton Cerrar sesion #######################
    img_btn_out = PhotoImage(file = "Imagenes/img_Inicio/btn_cerrarSesion.png")
    btn_out  = Button(image = img_btn_out,height =48,width =44,command = partial(cerrarSesion,app))
    btn_out.config(overrelief=GROOVE, relief=FLAT)
    btn_out.place(x=22,y=614)

    ############################# Label user ###############################
    lbl_user = Label(text = user ,bg = "light grey",fg = "Black", font=font.Font(family="Segoe UI Semibold"))
    lbl_user.place(x=1195,y=41)

    ############################# Label saldo ###############################
    lbl_saldo = Label(text ="$"+consultarSaldo(user) ,bg = "LightBlue",fg = "Black", font=font.Font(family="Segoe UI Semibold"))
    lbl_saldo.place(x=268,y=220)
    ##Consultar gastos
    consultarGastos(user)
    lbl_supermercado = Label(text ="$"+gastos(user,"Supermercado") ,bg = "White",fg = "Green", font=font.Font(family="Segoe UI Semibold"))
    lbl_supermercado.place(x=916,y=262)
    lbl_servicios = Label(text ="$"+gastos(user,"Servicios") ,bg = "White",fg = "LightBlue", font=font.Font(family="Segoe UI Semibold"))
    lbl_servicios.place(x=873,y=330)
    lbl_transporte = Label(text ="$"+gastos(user,"Transporte") ,bg = "White",fg = "Red", font=font.Font(family="Segoe UI Semibold"))
    lbl_transporte.place(x=879,y=401.5)
    lbl_ahorros = Label(text ="$"+gastos(user,"Ahorros") ,bg = "White",fg = "LightGreen", font=font.Font(family="Segoe UI Semibold"))
    lbl_ahorros.place(x=868,y=468)
    lbl_shopping = Label(text ="$"+gastos(user,"Shopping") ,bg = "White",fg = "Purple", font=font.Font(family="Segoe UI Semibold"))
    lbl_shopping.place(x=873,y=538.5)
    lbl_otro = Label(text ="$"+gastos(user,"Otro") ,bg = "White",fg = "Gray", font=font.Font(family="Segoe UI Semibold"))
    lbl_otro.place(x=863,y=608.7)
    
    app.mainloop()
    return()

def cargar_saldo(e_s,user):
    
    global lbl_numerico
    try: 
        lbl_numerico.place_forget()
    except NameError:
        nda= ""
    if (e_s.get().isnumeric()== False):
        lbl_numerico = Label(text = "Solo se pueden insertar numeros" ,bg = "SkyBlue4",fg = "red3", font=font.Font(family="Segoe UI Semibold"))
        lbl_numerico.place(x=290,y=460)
    else:
        conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
        bdd = conn.cursor()
        us ='"'+str(user)+'";'
        txt ="SELECT saldo FROM Usuarios WHERE username = "+str(us)
        bdd.execute(txt)
        saldo = bdd.fetchall()
        if(saldo != []):
            saldo = str(saldo)
            saldo=saldo[:-3]
            saldo = saldo[2:]
            saldo = int(saldo)+int(e_s.get())
            txt = "UPDATE Usuarios SET saldo ="+str(saldo)+"  WHERE username ='"+str(user)+"';"
            bdd.execute(txt)
            lbl_saldo = Label(text = "$"+str(saldo) ,bg = "LightBlue",fg = "Black", font=font.Font(family="Segoe UI Semibold"))
            lbl_saldo.place(x=268,y=220)
            conn.commit()
            conn.close()
            
        else:
            conn.close()
    return()

def consultarSaldo(user):
    conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
    bdd = conn.cursor()
    us ='"'+str(user)+'";'
    txt ="SELECT saldo FROM Usuarios WHERE username = "+str(us)
    bdd.execute(txt)
    saldo = bdd.fetchall()
    saldo = str(saldo)
    saldo = saldo[:-3]
    saldo = saldo[2:]
    conn.close()

    return(saldo)

def consultarGastos(user):
    conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
    bdd = conn.cursor()
    us ='"'+str(user)+'"'
    #month = str(datetime.today().year)
    #month +="-"+str(datetime.today().month)
    month = "2022-11"
    txt ="SELECT SUM(precio) FROM Gastos WHERE username = "+str(us)+"and (fecha LIKE '"+str(month)+"%')"
    bdd.execute(txt)
    total = bdd.fetchall()
    total = str(total)
    total = total[:-3]
    total  = total[2:]
    conn.close()
    if(total == "None"):
        total = int(0)
    lbl_gastos = Label(text = "$"+str(total) ,bg = "Light Blue",fg = "Black", font=font.Font(family="Segoe UI Semibold"))
    lbl_gastos.place(x=289,y=292)
    return()

def gastos(user,categoria):
    conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
    bdd = conn.cursor()
    us ='"'+str(user)+'"'
    categoria ='"'+str(categoria)+'"'
    #month = str(datetime.today().year)
    #month +="-"+str(datetime.today().month)
    month = "2022-11"
    
    txt ="SELECT SUM(precio) FROM Gastos WHERE username = "+str(us)+"and categoria ="+categoria+"and (fecha LIKE '"+str(month)+"%')"
    bdd.execute(txt)
    total = bdd.fetchall()
    total = str(total)
    total = total[:-3]
    total  = total[2:]
    conn.close()
    if(total == "None"):
        return("0")
    else :
        return(total)

def cerrarSesion(app):
    os.remove('user.txt')
    app.destroy()
    
def tienda(user,app):
    app.destroy()
    v_tienda.ventana(user)
    
