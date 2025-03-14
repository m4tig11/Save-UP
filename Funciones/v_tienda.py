######IMPORT#######################
from tkinter import *                                     ##
from tkinter import ttk                                  ##
import tkinter as tk                                        ##
from Funciones import v_registrarse           ##
from functools import partial                      ##
import sqlite3                                                ##
from Funciones import v_inicio
from Funciones import v_gastos
from Funciones import v_historial
from tkinter import font  
import os
from os import remove                         ##
###################################


def ventana(user):
    global usuario
    usuario = user
    ############################  Ventana ##########################
    app = Tk()
    app.attributes('-fullscreen',False)
    app.geometry("1390x775")
    app.title("Save Up")
    img_bg_tienda = PhotoImage(file = "Imagenes/img_tienda/bg_tienda.png")
    bg_tienda = Label(image = img_bg_tienda)
    bg_tienda.pack()
    

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

    ############################ boton Historial #######################
    img_btn_historial = PhotoImage(file = "Imagenes/img_Inicio/btn_historial.png")
    btn_historial  = Button(image = img_btn_historial,height =70,width =70,command=partial(v_historial.ventana,user,app))
    btn_historial.config(overrelief=GROOVE, relief=FLAT)
    btn_historial.place(x=16.5,y=493)

    ############################ boton Cerrar sesion #######################
    img_btn_out = PhotoImage(file = "Imagenes/img_Inicio/btn_cerrarSesion.png")
    btn_out  = Button(image = img_btn_out,height =48,width =44,command = partial(cerrarSesion,app))
    btn_out.config(overrelief=GROOVE, relief=FLAT)
    btn_out.place(x=30,y=613.5)

    ############################# Label user ###############################
    lbl_user = Label(text = user ,bg = "light grey",fg = "Black", font=font.Font(family="Segoe UI Semibold"))
    lbl_user.place(x=1193,y=42)



    ######################### comb resultados #######################
    global combo
    combo = ttk.Combobox()
    combo.place(x=168,y=198,height = 81,width=632)
    app.bind('<Key>',resultados)
    combo.bind("<<ComboboxSelected>>", buscar)
    
    ####################### Treeview #########################
    global trv_res
    trv_res = ttk.Treeview(columns =("Nombre local","Producto","Precio","Direccion"))
    trv_res.heading("Nombre local",text="Nombre local")
    trv_res.heading("Producto",text="Producto")
    trv_res.heading("Precio",text="Precio")
    trv_res.heading("Direccion",text="Direccion")
    trv_res.place(x=152,y=420,height = 295,width =1118)
    conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
    bdd = conn.cursor()
    t = combo.get()
    txt ="SELECT es_local from Usuarios where username =='"+user+"';"

    bdd.execute(txt)
    local=bdd.fetchall()
    if(local == [(1,)]):
        img_btn_produ = PhotoImage(file = "Imagenes/img_tienda/btn_producto.png")
        global btn_produ
        btn_produ  = Button(image = img_btn_produ,height =55,width =55,command=partial(new_prod,app,user))
        btn_produ.config(overrelief=GROOVE, relief=FLAT)
        btn_produ.place(x=1280,y=113.5)



    
    app.mainloop()



def buscar(event):
    global trv_res
    trv_res.delete(*trv_res.get_children())
    conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
    bdd = conn.cursor()
    t = combo.get()
    txt ="SELECT id_local,nombre,precio from Productos where nombre == '"+t+"'Order By Precio ASC LIMIT 3;"
    bdd.execute(txt)
    a=bdd.fetchall()

    
    direcciones =[]
    nombres =[]
    cant = len(a)

    for i in range(cant):
        txt ="SELECT direccion,nombre_Local from Locales where id_local == '"+str(a[i][0])+"';"
        bdd.execute(txt)
        d_local = (bdd.fetchall())
        direcciones.append(d_local[0][0])
        nombres.append(d_local[0][1])
    tg = "Mejor precio"
    for i in range(cant):
        trv_res.insert("",tk.END,text=tg ,values=(nombres[i],a[i][1],a[i][2],direcciones[i]))
        tg ="Alternativas"
    conn.close()
    
def new_prod(app,user):
    global btn_produ
    btn_produ['state'] = tk.DISABLED
    app.update()
    np = Tk()
    np.geometry("600x600")
    np.resizable(width =0,height=0)
    np.title("Save Up")
    np.config(bg="light blue")
    lbl_nom = Label(np,text = "Nombre del producto:" ,fg = "Black")
    lbl_nom.place(x=50,y=50)
    ety_nombre = Entry(np,bg="White")
    ety_nombre.place(x=230,y=50,height = 50,width=150)
    ety_nombre.config(relief = FLAT)
    lbl_precio = Label(np,text = "Precio del producto:" ,fg = "Black")
    lbl_precio.place(x=50,y=150)
    ety_precio = Entry(np,bg="White")
    ety_precio.place(x=230,y=150,height = 50,width=150)
    ety_precio.config(relief = FLAT)
    btn_acept  = Button(np,text ="Aceptar",height =5,width =50,command = partial(validar,ety_nombre,ety_precio,user,np))
    btn_acept.config(overrelief=GROOVE, relief=FLAT)
    btn_acept.place(x=30,y=250.5)
    
    np.mainloop()
    
def validar(nom,precio,user,np):
    if(len(nom.get())>30):
        lbl  = Label(np,text="No puede contener mas de 30 caracteres")
        lbl.place(x=230,y=20)
        return()
    else:
        nombre = (nom.get().replace(" ","_")).lower()

    if(precio.get().isnumeric()==False):
        lblp  = Label(np,text="Solo se aceptan valores enteros")
        lblp.place(x=230,y=130)
        return()

    conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
    bdd = conn.cursor()
    txt ="SELECT id_local FROM Locales WHERE username = '"+str(user)+"'"
    bdd.execute(txt)
    id_local = bdd.fetchall()
    id_local = str(id_local)
    id_local = id_local[:-3]
    id_local  = id_local[2:]
    txt ="SELECT barrio FROM Locales WHERE id_local ="+id_local
    bdd.execute(txt)
    barrio = bdd.fetchall()
    
    barrio = str(barrio)
    barrio = barrio[:-3]
    barrio  = barrio[2:]
    txt ="INSERT INTO Productos(nombre,precio,id_local,barrio) values('{0}',{1},{2},{3})".format(nombre,precio.get(),id_local,barrio)
    print(txt)
    btn_produ['state'] = tk.NORMAL
    bdd.execute(txt)
    conn.commit()
    conn.close()
    np.destroy()
        
    return()
def cerrarSesion(app):
    os.remove('user.txt')
    app.destroy()
    return()

def inicio(user,app):
    app.destroy()
    v_inicio.ventana(user)
def resultados(event):
    global usuario
    usuario=str(usuario)
    global combo
    conn =sqlite3.connect("Base de datos/BDD_Save_up.db")
    bdd = conn.cursor()
    t = combo.get()
    txt ="SELECT barrio from Usuarios where username = '"+usuario+"';"
    bdd.execute(txt)
    barrio_user=bdd.fetchall()
    barrio_user = str(barrio_user)
    barrio_user = barrio_user[:-4]
    barrio_user = barrio_user[3:]
    txt ="SELECT DISTINCT nombre from Productos where nombre LIKE '"+t+"%""'and barrio = '"+barrio_user+"';"
    bdd.execute(txt)
    a=bdd.fetchall()
    combo['values'] = a
    conn.close()
