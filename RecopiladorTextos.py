#-------------------------------------------------------------------------------
# Name:        Recopilador de Textos
# Purpose:     Presentar una interfaz intuitiva capaz de almacenar
#              los textos de manera propia para el proyecto de IAN
#              utilizando el módulo Clases de Recopilador de Textos
#
# Version:     2.1.0
# Author:      PB203
#
# Created:     25/-2/2021
# Copyright:   (k) Ka-Tet Co. 1999
# Licence:     <uranus>
#-------------------------------------------------------------------------------

""" Módulo: Recopilador de Textos

Presenta una interfaz intuitiva capaz de almacenar los
textos de manera propia para el proyecto de IAN
utilizando el módulo Clases de Recopilador de Textos.
Si encuentra el módulo Furrcyones y sus métodos, los
llama para su ejecución.


Recopila:
    Funcion Hacer un Retroceso
    Funcion Actualizar el Retroceso
    Funcion Realizar Remplazo
    Funcion Cargar Objeto y Actualizar Pantalla
    Funcion Resetear la Interfaz de Forma Segura
    Funcion Agregar al Objeto Seguro
    Funcion Eliminar del Objeto Seguro
    Funcion Reiniciar Objeto Seguro
    Funcion Actualizar Interfaz
    Funcion Salir de la Interfaz
    Función Advertencia de Exceso
    Función Actualizar Autor
    Main Ejecucion de Interfaz
    Variable global Marco
    Variable global Objeto Entregable
    Variable global Limite de Retroceso
"""

try: # Importa tkinter, con la excepcion por version de python
    import Tkinter as tk
    from Tkinter import ttk
    from Tkinter import messagebox
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
from idlelib.tooltip import Hovertip
import copy, sys, os
from ClasesRecopilador import *

def doBckRoll():
    """ Funcion: Hacer un Retroceso

    Funcion que realiza un retroceso o back roll sobre los
    extractos de la variable local aporte. La funcion utiliza
    la variable global bckRoll, sobreescribiendola.
    """
    # para sobreescribir la variable global se debe invocar
    global bckRoll
    # al realizar el retroceso, si bckRoll es una tupla se presupone que
    #  el elemento 0 es el estado actual de extractos y el elemento 1
    #  es el estado anterior de bckRoll, en el cual se asume que si es una
    #  tupla el elemento 0 será el estado anterior de los extractos
    if type(bckRoll) == tuple: bckRoll=bckRoll[1]
    # al realizar la carga del retroceso, si bckRoll continua siendo una
    #  tupla entonces el estado a cargar se halla en el elemento 0; si
    #  bckRoll es una lista significa que la variable global nunca a sido
    #  actualizada desde su primer estado, entonces bckRoll es el estado a
    #  cargar; en cualquier otro caso significa un error
    if type(bckRoll) == tuple: aporte.setExtractos(bckRoll[0])
    elif type(bckRoll) == list: aporte.setExtractos(bckRoll)
    else: print("Error en el sistema de retro")

def chejov():
    """ Funcion: Actualizar el Retroceso

    Funcion que actualiza los estados de cambio de los
    extractos en la variable global bckRoll para realizar
    futuros retrocesos.
    """
    # para sobreescribir la variable global se debe invocar
    global bckRoll
    # se sobreescribe bckRoll como una tupla par; en el elemento 0 se hace
    #  una copia superficial de los extractos actuales y en el estado 1 se
    #  inserta el estado anterior de bckRoll
    bckRoll = ([copy.copy(i) for i in aporte.getExtractos()], bckRoll)

def gcObj():
    """ Función: Advertencia de Exceso

    Funcion que ejecuta un mensaje de advertencia que informa
    el desbordamiento del objeto.
    """
    messagebox.showwarning("Acercándose a la masa crítica",
        f'Alerta\nEl numero de extractos en el objeto ({aporte.getN()}) ' +
        'es superior al numero de extractos recomendado por semana. Este ' +
        'mensaje seguirá apareciendo hasta que guardes el entregable y ' +
        'reinicies el objeto.\nRecomendación: Has las últimas revisiones, ' +
        'guarda el entregable, sube el entregable al drive, y solo entonces' +
        'reinicia el objeto.')


def updObj(remps: [list(tuple((str,str))),callable],idx: int):
    """ Funcion: Realizar Remplazo

    Funcion que recibe una serie de remplazos para realizar
    sobre un extracto indexado.

    Parámetros:
        remps (list) -- una lista con tuplas, cada tupla
            contiene dos strings, cada primera string es un
            texto a ser remplazado y cada segunda string es
            un texto de remplazo
        remps (callable) -- un objeto llamable el cual se
            presupone devolvera una lista con tuplas papres
            de strings
        idx (int) -- un entero que indica el indice del
            extracto a editar

    Anotaciones:
        Al ser un método unicamente usado por el módulo, sin
            intervencion del usuario, se preasume que no
            será llamado con un indice que genere un
            IndexError, por eso no se toma en cuenta la
            excepcion.
    """
    # si remps es del tipo callable sobreescribe remps con el retorno del
    #  objeto callable
    if str(type(remps)) == "<class 'function'>": remps = remps()
    # por cada elemento i, que es una tupla par, en la lista remps
    #  asigna al texto del extracto idx
    #   la conversion a caracteres de
    #    el texto del extracto idx tras
    #     codificarlo con el método de clase código a char
    #     reemplazar en él el elemento 0 de i codificado por el elemento 1 de i
    #      codificado, ambos forzado
    for i in remps:
        if i[0] == "" and i[1] != "":
            messagebox.showwarning("Te faltó uno allí",'En algún punto ' +
                'intentas reemplazar el vacio, lo cuál está prohibido')
            continue
        aporte.getExtractos(idx).texto = Extracto.cod2char((Extracto.cod2char(
            aporte.getExtractos(idx).texto)).replace(Extracto.cod2char(
            Extracto.ascii2char(i[0],True)),Extracto.cod2char(
            Extracto.ascii2char(i[1],True))))
    # actualiza el nuevo estado de los textos con la funcion para ello
    chejov()

def loadObj(idx: int = None):
    """ Funcion: Cargar Objeto y Actualizar Pantalla

    Funcion que carga el objeto entregable acudiendo a su
    método cargar objeto y actualiza la interfaz con el
    indice que recibe.

    Parámetros:
        idx (int) -- un entero que será el indice con el
        que se actualice la interfaz (p.d. None)
    """
    aporte.load()
    loadGUI(marco,idx)

def resetGUI(idx: int = None):
    """ Funcion: Resetear la Interfaz de Forma Segura

    Funcion que actualiza la interfaz, guardando y
    recargando el objeto entregable. Acude a la funcion
    cargar objeto y actualizar pantalla para funcionar.

    Parámetros:
        idx (int) -- un entero que será el indice con el
        que se actualice la interfaz (p.d. None)
    """
    aporte.save()
    loadObj(idx)

def addObj(txt: str,end: bool,gen: str,cls: str,idx: int):
    """ Funcion: Agregar al Objeto Seguro

    Funcion que presenta confirmaciones antes de agregar un
    nuevo extracto al objeto entregable.

    Parámetros:
        txt (str) -- un texto
        end (bool) -- un booleano que representa la posible
            finalización de txt
        gen (str) -- un género narrativo al cual pertenece
            el txt; debe estar en la lista GNS de la clase
            Entregable
        cls (str) -- una clasificacion literaria que
            conforma txt; debe estar en la lista CLS de la
            clase Entregable
        idx (int) -- un indice al cual se asignara el
            extracto a agregar y con el cual se actualiza
            la interfaz; si idx es None se agregara al
            final el extracto

    Excepciones:
        AssertionError: multiples errores de assert, ver
            excepciones contempladas en el método dunder
            constructor extracto de la clase extracto del
            módulo clases de recopilador de textos
        AssertionError: multiples errores de assert, ver
            excepciones contempladas en el método agregar
            a extractos de la clase entregable del módulo
            clases de recopilador de textos
    """
    try:
        # si el texto del extracto a agregar, calculado con el método de clase
        #  calcular longitud de texto, cumple con el limite minimo de palabras
        #  de clase la clase entregable
        if Entregable.LIM_WORDS[0] <= Extracto.calcLngTxt(txt):
            # crea el extracto como una variable temporal
            t= Extracto(txt,True if end == "true" else (False if end == "false"
                else None),gen,cls)
            # si para cada extracto e en
            #  enumerate(aporte.getExtractos()) exceptuando cuando i es idx
            #  es cierto que e no es identico a t
            if all(e!=t for i,e in enumerate(aporte.getExtractos()) if i!=idx):
                # si el texto del extracto a agregar, calculado con el método de
                #  clase calcular longitud de texto, excede por mucho los limites
                #  de palabras de la clase entregable
                if Extracto.calcLngTxt(txt) > (Entregable.LIM_WORDS[1] *
                    Entregable.LIM_WORDS[0]):
                        messagebox.showinfo("Then you'll begin to make it better " +
                            "better better better better better",'¿¡Que carajos' +
                            f'!? Nuevo lider: {aporte.autor}')
                # si el texto del extracto a agregar, calculado con el método de
                #  clase calcular longitud de texto, excede los limites de palabras
                #  de la clase entregable
                elif Extracto.calcLngTxt(txt) > (Entregable.LIM_WORDS[1] +
                    Entregable.LIM_WORDS[0]):
                        messagebox.showinfo("Hey Jude! refrain, don't carry " +
                            "the world upon your shoulders", 'El texto que has ' +
                            'pasado es bastante amplio... \\U0001f97a Gracias... ' +
                            f'¡{Extracto.calcLngTxt(txt)} palabras! Toma awa de ' +
                            'uwu y ponle un break a tu código.')
                # usa el método agregar a extractos y el constructor de extractos
                #  dinámicamente
                aporte.addExtractos(obj=t,idx=idx)
                # llama a la función advertencia de exceso si existe un exceso
                if aporte.isTLDR(): gcObj()
                # actualiza el retroceso y actualiza la interfaz de forma segura
                chejov()
                resetGUI(idx=idx)
            else:
                messagebox.showwarning("So let it out and let it in (?)",
                'El extracto que has pasado es identico a otro existente en ' +
                'el objeto, lo cuál no cumple con los estandares ' +
                'preacordados para los entregables. Puedes pasar el mismo ' +
                'texto varias veces, pero solo si identificas que sus ' +
                'criterios son diferentes.')
        else:
            messagebox.showwarning("Hey Jude! don't make it bad",
                'El texto que has pasado es demasiado corto según los ' +
                'estandares preacordados para los entregables. El texto que ' +
                f'pasaste tiene {Extracto.calcLngTxt(txt)} palabras, y el ' +
                f'mínimo  son {Entregable.LIM_WORDS[0]} palabras.')
    except AssertionError:
        messagebox.showerror("Datos erróneos", "Alguno de los datos " +
            "ha sido mal seleccionado. El error puede ser en los campos de" +
            "género, clasifikación o finalidad. Rectifique y reintente.")

def delGUIObj(idx: int):
    """ Funcion: Eliminar del Objeto Seguro

    Funcion que presenta confirmaciones antes de eliminar un
    extracto existente del objeto entregable.

    Parámetros:
        idx (int) -- un entero que será el indice a eliminar

    Excepciones:
        IndexError -- si no existe un indice idx
        AttributeError -- si al hacer la confirmacion de
            usuario sucede un error de indice entonces esta
            funcion no puede procesarlo y devulve un
            AttributeError
    """
    try:
        # confirmación del usuario
        if messagebox.askokcancel("Realizar (d)eliminacinación del extracto",
            f'¿Desea eliminar el extracto {idx} ' +
            f'({aporte.getExtractos(idx).texto[:25]}...)?'):
            # usa el método eliminar de extractos y actualiza el retroceso
            aporte.delExtracto(idx)
            chejov()
    except IndexError: messagebox.showinfo("Alerta de ¿Huh... indice perdido?",
        'Vale, este es un error muy especifico y como el usuario final quizá ' +
        'no lo vea nunca lo usaré como easter egg. (Rápido, subelo a reddit!)' +
        '\nSi quieres saber que pasó y porque nunca se desplegará este ' +
        'mensaje, vamo\' allá:\nCuando este metodo recibe un indice indebido ' +
        'o un None como argumento (usualmente porque no habia un extracto ' +
        'cargado en memoria) el mensaje de confirmacion devuelve toda la ' +
        'lista de extractos en lugar de solo un extracto. Cuando trata de ' +
        'cargar el texto del extracto encuentra que la lista no tiene un ' +
        'atributo llamado texto. Entonces, siempre que un índice no exista ' +
        'dará un AttributeError, nunca un IndexError... Este es el easter '
        'egg más aburrido que verás. Ahora averigua sobre uno mejor, como La ' +
        'Quinta Llave o la apariencia de mujer de Juan en La Última Cena...')
    except AttributeError: messagebox.showwarning("Alerta de extracto perdido"+
        "del espacio exterior", 'Un error desconocido ha ocurrido al intentar '
        f'eliminar el extracto {idx}.\nPerdone, pero se reiniciará la ' +
        'interfaz (tratando de no guardar el extracto actual) para correguir '+
        'el error')
    # actualiza la interfaz de forma segura sin importar la confirmacion
    finally: resetGUI()

def resetGUIObj():
    """ Funcion: Reiniciar Objeto Seguro

    Funcion que presenta confirmaciones antes de reiniciar
    el objeto entregable.
    """
    # mensaje de advertencia que informa el proceso
    messagebox.showwarning("Alerta de reinicio de archivo",
        f'ALERTA\nAl resetear el objeto se eliminan los ({aporte.getN()}) ' +
        'extractos que se hallan en memoria y se guarda automaticamente el ' +
        'objeto sin extractos para evitar posibles errores. El archivo de ' +
        'texto entregable NO se guarda automaticamente.\nPor el bien de su ' +
        'sanidad mental, antes de aceptar el reseteo del objeto asegurese ' +
        'de que el entregable guardado (.txt) ya no sea necesario, pues ' +
        'puede que lo sobreescriba en breve.')
    # confirmacion de usuario directa de reinicio
    if messagebox.askokcancel("Realizar reseteo objeto",
        "¿Desea realizar el reseteo del objeto?"):
        # usa el método reiniciar extractos, actualiza el retroceso y actualiza
        #  la interfaz de forma segura
        aporte.reset()
        chejov()
        resetGUI()
    else:
        # confirmacion de usuario para guardar archivo plano y despues reiniciar
        if messagebox.askquestion("Para ahorrar tiempo",
        'Si en realidad sí quieres resetear el objeto, y solo te falta ' +
        'guardar el entregable para poder resetearlo con tranquilidad da ' +
        'clic en "Sí"; en caso contrario da clic en "No"') == "yes":
            # guardar el archivo plano, usa el método reiniciar extractos,
            #  actualiza el retroceso y actualiza la interfaz de forma segura
            aporte.saveFl()
            aporte.reset()
            chejov()
            resetGUI()

def loadGUI(root: tk.Tk, idx: int = None):
    """ Funcion: Actualizar Interfaz

    Funcion que actualiza la interfaz dependiendo del proceso
    para el que halla sido llamada.

    Parámetros:
        root (tk.Tk) -- un objeto tk con el atributo
            grid_slaves, de preferencia del tipo tk.Tk
        idx (int) -- un indice con el cual varia como se
            actualiza la interfaz; sirve como comodín,
            permitiendo ver el archivo entregable (p.d. None)

    Anotaciones:
        Esta funcion puede segregarse en funciones atomicas
            o estructurarse como funcion encapsuladora; para
            la documentación línea a línea se referencia esta
            posible segregación al nombrar los segmentos.
        Algunas posibles excepciones discretas llaman a la
            misma funcion por defecto con el argumento root.
        Se generan reiteradamente variables bajo el mismo
            nombre, aprovechando la asignacion de padres de
            varios elementos de tkinter por memoria en lugar
            de por nombres.
    """
    # destruye todos los elementos de root
    for l in root.grid_slaves(): l.destroy()

    # Segmento: Zona de Texto
    # se genera un label anonimo, decorado y ubicado
    #  se adapta el texto segun idx
    #   si el texto pertenece a un extracto se informa el idx
    #   si el texto no pertenece a un extracto se informa genericamente
    tk.Label(root,text=(("Inserte el texto" if idx == None else "Edite el " +
        f"texto del extracto {idx}") + " aqui debajo:" if idx != -1 else
            "Así se ve el archivo completo entregable"),bg="#202020",fg="white",
                font="Times").grid(row=0,column=0,sticky="NEWS")
    # se genera txEx, un text
    txEx = tk.Text(root,width=80, height=30)
    # si idx no es un indice no inserta nada en txEx
    # si idx es el comodín -1 inserta el entregable completo en txEx
    # si existe el indice idx en los extractos inserta el texto del indice idx
    #  en txEx
    try:txEx.insert('1.0',(aporte.getExtractos(idx).texto if idx != -1 else str(
        aporte)) if idx != None else "")
    except IndexError:loadGUI(root)
    txEx.grid(row=1,column=0,rowspan=22,sticky="NSWE")
    # se genera una hovertip anonima sobre txEx
    #  se adapta el texto segun idx
    #   si el texto pertenece a un extracto se aclara el idx
    #   si el texto no pertenece a un extracto se aclara genericamente
    Hovertip(txEx,"Zona de texto\n" + (("inserte un texto; el texto no se " +
        "guardará hasta que de clic en guardar nuevo extracto, solo si se " +
        "llenaron los campos complementarios" if idx == None else
        "edita el texto; el texto no se guardará hasta que de clic en guardar "+
        f"{idx}º extracto") if idx != -1 else "ningún cambio que hagas en " +
        "esta vista se guardará"),hover_delay=500)
    # código basura descartado para tener la longitud en palabras del texto
    #  en cada tiempo t, ocupaba espacio en memoria y era ineficiente
    # txEx.bind("<Key>",lambda x:print(Extracto.calcLngTxt(txEx.get('1.0',
    #     tk.END))))

    # Segmento: Advertencia
    # si existe al menos un extracto se ejecuta el segmento
    if aporte.getN() > 0:
        # se genera lb, un label
        #  se adapta el texto con el autor y el número de extractos
        lb = tk.Label(root,text='ADVERTENCIA, el archivo en el que estas ' +
            f'trabajando, de autor\n{aporte.autor}, tiene en este momento ' +
            f'{aporte.getN()} extracto{"s" if aporte.getN() > 1 else ""}. Si ' +
            'quieres empezar de\ncero da clic:',bg="#f06060",fg="white",font=
            "Times",justify=tk.LEFT)
        lb.grid(row=0,column=1,rowspan=2,columnspan=3,sticky="NEWS")
        Hovertip(lb,"Advertencia\neste mensaje solo aparece si el archivo " +
            "actual tiene al menos 1 extracto",hover_delay=500)
        lb = tk.Label(root,bg="#f06060")
        lb.grid(row=2,column=1,columnspan=3,sticky="NEWS")
        Hovertip(lb,"Advertencia\neste mensaje solo aparece si el archivo " +
            "actual tiene al menos 1 extracto",hover_delay=500)
        bt = tk.Button(root, text="Resetear objeto", command=resetGUIObj)
        bt.grid(row=2, column=2,columnspan=2,sticky="NEW")
        Hovertip(bt,"Botón de reinicio\nelimina todos los extractos dentro de "+
            "un aporte",hover_delay=500)

    # Segmento: Zona de Extractos
    # si idx no es el comodín -1 se ejecuta el segmento
    if idx != -1:
        lb = tk.Label(root,bg="#7090c0")
        lb.grid(row=3,column=1,rowspan=10,columnspan=3,sticky="NEWS")
        Hovertip(lb,"Zona de extractos\ntodas las funciones agrupadas en este "+
            "espacio sirven para introducir los datos complementarios, " +
            "guardar, eliminar o cerrar un extracto",hover_delay=500)
        tk.Label(root,text="ZONA DE TRABAJO PARA UN EXTRACTO DE TEXTO",bg=
            "#7090c0",font="Times").grid(row=3,column=1,columnspan=3,sticky=
            "NEWS")
        #tk.Label(root,bg="#7090c0").grid(row=4,column=1) # código basura
        tk.Label(root,text="Seleccione un género:",bg="#7090c0",font="Times"
            ).grid(row=5,column=1,columnspan=2,sticky="NWS")
        # se genera cbGn, una combobox bloqueada
        cbGn = ttk.Combobox(root, state="readonly", width="2")
        # usa los generos narrativos de la clase entregable
        cbGn["values"] = Entregable.GNS
        # si idx no es un indice inserta "" en cbGn
        # si existe el indice idx en los extractos inserta el género del indice
        #  idx en cbGn
        # si no existe el indice idx en los extractos llama a la funcion
        #  actualizar interfaz por defecto con el argumento root
        try: cbGn.set(aporte.getExtractos(idx).genero if idx != None else "")
        except IndexError: loadGUI(root)
        cbGn.grid(row=5, column=3,sticky="EW")
        Hovertip(cbGn,"Campo de género\nopciones para asignar un género al " +
            "extracto",hover_delay=500)
        tk.Label(root,text="Seleccione una clasificación:",bg="#7090c0",font=
            "Times").grid(row=6,column=1,columnspan=2,sticky="NWS")
        # se genera cbCl, una combobox bloqueada
        cbCl = ttk.Combobox(root, state="readonly", width="2")
        # usa las clasificaciones literarias de la clase entregable
        cbCl["values"] = Entregable.CLS
        # si idx no es un indice inserta "" en cbCl
        # si existe el indice idx en los extractos inserta la clasificación
        #  del indice idx en cbCl
        # si no existe el indice idx en los extractos llama a la funcion
        #  actualizar interfaz por defecto con el argumento root
        try: cbCl.set(aporte.getExtractos(idx).clase if idx != None else "")
        except IndexError: loadGUI(root)
        cbCl.grid(row=6, column=3,sticky="EW")
        Hovertip(cbCl,"Campo de clasificación\nopciones para asignar una " +
            "clase al extracto",hover_delay=500)
        tk.Label(root,text="Clasifique si el texto es finalizado:",bg="#7090c0",
            font="Times").grid(row=7,column=1,columnspan=2,sticky="NWS")
        # se genera cbNd, una combobox bloqueada
        cbNd = ttk.Combobox(root,state="readonly",width="2")
        cbNd["values"] = ["true","false"]
        # si idx no es un indice inserta "" en cbCl
        # si existe el indice idx en los extractos inserta la finalización
        #  del indice idx en cbNd
        # si no existe el indice idx en los extractos llama a la funcion
        #  actualizar interfaz por defecto con el argumento root
        try: cbNd.set(str(aporte.getExtractos(idx).fin).lower() if idx != None
            else "")
        except IndexError: loadGUI(root)
        cbNd.grid(row=7, column=3,sticky="EW")
        Hovertip(cbNd,"Campo de finalización\nopciones para especular sobre " +
            "el final del extracto",hover_delay=500)
        # se genera vrLn, una stringvar
        vrLn = tk.StringVar()
        # se genera txLn, una entry bloqueada
        #  se asigna vrLn como variable de texto para txLn
        txLn = tk.Entry(root,textvariable=vrLn,state="readonly")
        txLn.grid(row=8,column=3,sticky="E")
        # si idx no es un indice inserta "" en vrLn
        # si existe el indice idx en los extractos inserta la longitud del
        #  indice idx en vrLn
        # si no existe el indice idx en los extractos llama a la funcion
        #  actualizar interfaz por defecto con el argumento root
        try: vrLn.set(str(aporte.getExtractos(idx).longitud) if idx != None
            else "")
        except IndexError: loadGUI(root)
        # se genera una hovertip anonima sobre txLn
        #  se adapta el texto segun idx
        #   si la longitud pertenece a un extracto se aclara el idx
        #   si la longitud no pertenece a un extracto se aclara genericamente
        Hovertip(txLn,"Campo de conteo\nmuestra el conteo " + ("inicializado " +
            "con el botón de conteo" if idx == None else "registrado en el " +
            f"texto del extracto {idx}"),hover_delay=500)
        # se genera bt, un button
        #  se asigna un comando con parámetros a través de una funcion lambda
        #   lambda llamará el setter de vrLn
        #    usa el método de clase calcular longitud de texto sobre el
        #     retorno del getter de txEx
        bt = tk.Button(root,text="Revelar conteo de palabras del texto",command=
            lambda:vrLn.set(Extracto.calcLngTxt(txEx.get('1.0',tk.END))))
        bt.grid(row=8,column=1,columnspan=2)
        Hovertip(bt,"Botón de conteo\ncuenta las palabras del texto que este " +
            "en la zona de textos, mostrando el conteo en el campo de conteo",
            hover_delay=500)
        #tk.Label(root,bg="#7090c0").grid(row=9,column=1) # código basura
        # se genera bt, un button
        #  se adapta el texto
        #   si idx no es un indice informa genericamente
        #   si existe el indice idx en los extractos informa idx
        #  se asigna un comando con parámetros a través de una funcion lambda
        #   lambda llamará la funcion agregar al objeto seguro con los
        #    argumentos txEx, cbNd, cbGn, cbCl e idx
        bt = tk.Button(root,text="Guardar {} extracto ".format('nuevo' if idx
            == None else str(idx) + 'º') + "en el archivo actual (sin guardar "+
            "el entregable)",command=lambda:addObj(txEx.get('1.0',tk.END)[:-1],
            cbNd.get(),cbGn.get(),cbCl.get(),idx))
        bt.grid(row=10,column=1,columnspan=3,sticky="NEWS")
        # se genera una hovertip anonima sobre bt
        #  se adapta el texto segun idx
        #   si idx no es un indice aclara genericamente
        #   si existe el indice idx en los extractos aclara idx
        Hovertip(bt,"Guardar "+("nuevo" if idx == None else f"{idx}º")+
            " extracto\nguarda y cierra el extracto si cumple con los campos " +
            "complementarios",hover_delay=500)
        # si idx no es un indice se agregan los siguientes elementos
        if idx != None:
            bt = tk.Button(root,text="Cerrar el extracto sin guardar",command=
                lambda:loadGUI(root))
            bt.grid(row=11,column=1,columnspan=3,sticky="NEWS")
            Hovertip(bt,"Cerrar extracto\ncierra el extracto",hover_delay=500)
            bt = tk.Button(root,text="Eliminar este extracto, guardar y cerrar",
                command=lambda:delGUIObj(idx))
            bt.grid(row=12,column=1,columnspan=3,sticky="NEWS")
            Hovertip(bt,"Eliminar extracto\nelimina el extracto",
                hover_delay=500)

    # Segmento: Zona de Objeto
    tk.Label(root,bg="#80f080").grid(row=13,column=1,rowspan=4,columnspan=3,
        sticky="NEWS")
    tk.Label(root,text="ZONA DE TRABAJO PARA EL OBJETO",bg="#80f080",
        font="Times").grid(row=13,column=1,columnspan=3,sticky="NEWS")
    # se genera bt, un button
    #  se asigna un comando de varios llamados con parámetros a través de
    #   una funcion lambda
    #   se genera una confirmacion de usuario
    #    se adapta el texto de la confirmacion con el numero de extractos del
    #     objeto entregable y el numero de extractos del archivo entregable
    #    si confirmación de usuario lambda llamará el método cargar de aporte
    #    si no confirmación de usuario lambda llamará la funcion actualizar
    #     interfaz
    bt = tk.Button(root,text="Cargar objeto",command=lambda:[aporte.load() if
        messagebox.askokcancel("Realizar cargue del objeto", "El archivo que " +
        f"desea cargar tiene {Entregable.loadObj().getN()} extractos y el" +
        f" actual tiene {aporte.getN()} ¿Desea cargar del objeto?") else None,
        loadGUI(root), gcObj() if aporte.isTLDR() else None])
    bt.grid(row=14,column=1,sticky="NEWS")
    Hovertip(bt,"Cargar objeto\ncarga el objeto basandose en el archivo " +
        "llamado objEntregable.txt",hover_delay=500)
    # se genera bt, un button
    #  se asigna un comando de varios llamados a través de una funcion lambda
    #   lambda llamará el método guardar de aporte y el método cargar de aporte
    bt = tk.Button(root,text="Guardar objeto",command=lambda:[aporte.save(),
        aporte.load()])
    bt.grid(row=14,column=2,sticky="NEWS")
    Hovertip(bt,"Guardar objeto\nguarda el objeto actualmente abierto en el " +
        "archivo llamado objEntregable.txt",hover_delay=500)
    # se genera bt, un button
    #  se asigna un comando de varios llamados con parámetros a través de
    #   una funcion lambda
    #   lambda llamará el método guardar archivo de aporte y la funcion
    #    resetear la interfaz de forma segura con el argumento idx
    bt = tk.Button(root,text="Guardar objeto y entregable",command=lambda:[
        aporte.saveFl(),resetGUI(idx=idx)])
    bt.grid(row=14,column=3,sticky="NEWS")
    # se genera una hovertip anonima sobre bt
    #  se adapta el texto con aporte.autor
    Hovertip(bt,"Guardar todo\nguarda el objeto actualmente abierto en el " +
        "archivo llamado objEntregable.txt\ny estructura y almacena el " +
        "entregable en el archivo " + f"{aporte.autor}.txt",hover_delay=500)
    tk.Label(root,text="Seleccione un extracto:",bg="#80f080",font="Times"
        ).grid(row=15,column=1,sticky="NWS")
    # se genera cbEx, una combobox bloqueada
    cbEx = ttk.Combobox(root,state="readonly",width="2")
    # asigna a 'values' de cbEx una lista de un único elemento "Nueva"
    #  agregando una lista por comprension
    #   la lista por comprension se formará "i: j" por cada indice i y
    #    elemento j retornado por el metodo getter extractos por
    #    defecto
    #    cada elemento j sera el retorno del método dunder string extracto
    #     con el argumento soloTxt como True
    cbEx["values"] = ["Nueva"] + ['{}: {}'.format(i,j.__str__(soloTxt = True
        )[:10]) for i,j in enumerate(aporte.getExtractos())]
    cbEx.set("Nueva")
    cbEx.grid(row=15, column=2,sticky="EW")
    Hovertip(cbEx,"Listado de extractos\nopciones de selección de extractos " +
        "almacenados en el objeto actual",hover_delay=500)
    # se genera bt, un button
    #  se asigna un comando de varios llamados con parámetros a través de
    #   una funcion lambda
    #   lambda llamará la funcion actualizar interfaz con argumentos root y
    #    None si el retorno de cbEx.get() coincide con el elemento 0 de cbEx
    #    o el indice seleccionado de cbEx si cbEx.get() no coincide con el
    #    elemento 0
    bt = tk.Button(root,text="Cargar extracto",command=lambda:[loadGUI(root,
        None if cbEx["values"].index(cbEx.get()) == 0 else cbEx["values"].index(
            cbEx.get()) - 1)])
    bt.grid(row=15,column=3,sticky="NEWS")
    Hovertip(bt,"Cargar extracto\ncarga el extracto seleccionado en el " +
        "listado de extractos para su trabajo",hover_delay=500)
    # se genera bt, un button
    #  se asigna un comando con parámetros a través de una funcion lambda
    #   lambda llamará la funcion actualizar interfaz con argumentos root y -1
    bt = tk.Button(root,text="Renombrar objeto",command=lambda:[updAut("Dime " +
        "tu nuevo nombre (y espero no me vuelvas a pedir cambiarlo)"),
        marco.title(f'{aporte.autor}: Recopilador de Textos -JEAN (Proyecto ' +
        'IAN)')])
    bt.grid(row=16,column=1,sticky="NEWS")
    Hovertip(bt,"Renombrar autor del objeto\ncarga el dialogo para asignar un "+
        "autor al objeto actual",hover_delay=500)
    # se genera bt, un button
    #  se asigna un comando con parámetros a través de una funcion lambda
    #   lambda llamará la funcion actualizar interfaz con argumentos root y -1
    bt = tk.Button(root,text="Cargar extractos completos",command=lambda:
        loadGUI(root,idx=-1))
    bt.grid(row=16,column=2,columnspan=2,sticky="NEWS")
    Hovertip(bt,"Cargar extractos completos\ncarga el entregable completo en " +
        "la zona de textos",hover_delay=500)

    # Segmento: Zona de Edición de Texto
    #   si existe el indice idx en los extractos ejecuta el segmento
    if idx not in [-1,None]:
        tk.Label(root,bg="#f0f080").grid(row=17,column=1,rowspan=6,columnspan=3,
            sticky="NEWS")
        tk.Label(root,text="ZONA DE EDICION PARA EL TEXTO",bg="#f0f080",
            font="Times").grid(row=17,column=1,columnspan=3,sticky="NEWS")
        #tk.Label(root,bg="#f0f080").grid(row=18,column=1,columnspan=3
        # ) # código basura
        tk.Label(root,text="Escriba el texto a remplazar:",bg="#f0f080",font=
            "Times").grid(row=19,column=1,columnspan=2,sticky="NWS")
        # se genera vrRt, una stringvar
        vrRt = tk.StringVar()
        # se genera txRt, una entry bloqueada
        #  se asigna vrRt como variable de texto para txRt
        txRt = tk.Entry(root,textvariable=vrRt)
        txRt.grid(row=19,column=3,sticky="E")
        #vrRt.set("") # código basura
        Hovertip(txRt,"Cadena de reemplazados\nintroduzca el, los o las " +
            "segmentos del texto que\nconsidere que desea reeplazar en el " +
            "texto; se\nrecomienda ver la documentación o las video-guias\n" +
            "para estructurar bien la cadena de reemplazados",hover_delay=500)
        tk.Label(root,text="Escriba el texto de remplazo:",bg="#f0f080",font=
            "Times").grid(row=20,column=1,columnspan=2,sticky="NWS")
        # se genera vrRg, una stringvar
        vrRg = tk.StringVar()
        # se genera txRg, una entry bloqueada
        #  se asigna vrRg como variable de texto para txRg
        txRg = tk.Entry(root,textvariable=vrRg)
        txRg.grid(row=20,column=3,sticky="E")
        #vrRg.set("") # código basura
        Hovertip(txRg,"Cadena de reemplazos\nintroduzca la, las o los cadenas "+
            "del texto que\nconsidere que reeplazará en el texto a la cadena\n"+
            "de reemplazados; se recomienda ver la documentación\no las " +
            "video-guias para estructurar bien la cadena\nde reemplazos",
            hover_delay=500)
        tk.Label(root,text="Atajos de remplazo:",bg="#f0f080",font="Times"
            ).grid(row=21,column=1,sticky="NWS")
        # se genera cbAt, una combobox bloqueada
        cbAt = ttk.Combobox(root, state="readonly", width="2")
        # asigna a 'values' de cbAt una lista heredada del diccionario de
        #  atajos de la clase entregable
        cbAt["values"] = list(Entregable.ATJ_RMP.keys())
        cbAt.set("")
        cbAt.grid(row=21, column=2,columnspan=2,sticky="EW")
        # se asigna un evento comboboxselected de varios llamados con varios
        #  parámetros a través de una funcion lambda con un parametro
        #  inservible
        #  lambda llamará a sobreescribir state de txRt con el argumento
        #   'readonly' si el retorno de cbAt.get() no es "", sino con el
        #   argumento'normal', a sobreescribir state de txRg con el argumento
        #   'readonly' si el retorno de cbAt.get() no es "", sino con el
        #   argumento 'normal', al setter de vrRt con el argumento vrRt.get()
        #   si el retorno de cbAt.get() es "", sino con el argumento "" y al
        #   setter de vrRg con el argumento vrRg.get() si el retorno de
        #   cbAt.get() es "", sino con el argumento ""
        cbAt.bind("<<ComboboxSelected>>",lambda dummy:[txRt.configure(state=
            "readonly" if cbAt.get() != "" else "normal"),txRg.configure(state=
            "readonly" if cbAt.get() != "" else "normal"),vrRt.set(vrRt.get()
            if cbAt.get() == "" else ""),vrRg.set(vrRg.get() if cbAt.get() ==
            "" else "")])
        Hovertip(cbAt,"Atajos de reemplazo\nopciones de reemplazos " +
            "identificados como frecuentes; se recomienda\nver la " +
            "documentación o las video-guias para identificar las acciones " +
            "de\nlos atajos",hover_delay=500)
        # se genera bt, un button
        #  se asigna un comando de varios llamados con parámetros a través de
        #   una funcion lambda
        #   lambda llamará las siguientes funciones
        #    la funcion realizar remplazo con argumentos una lista heredada e
        #     idx
        #     si la longitud de la lista generada al separar el retorno del
        #      getter de txRt con el separador "**" es igual a la longitud de
        #      la lista generada al separar el retorno del getter de txRg con
        #      el separador "**" la lista heredada será una lista por
        #      comprension formada por la tupla par (i,j) por cada elemento i y
        #      elemento j en el rango de la longitud de la lista generada al
        #      separar el retorno del getter de txRt con el separador
        #      "**"
        #       cada elemento i sera el retorno del indice i de la lista
        #        generada al separar el retorno del getter de txRt con el
        #        separador "**"
        #       cada elemento j sera el retorno del indice j de la lista
        #        generada al separar el retorno del getter de txRg con el
        #        separador "**"
        #     si la longitud de la lista generada al separar el retorno del
        #      getter de txRt con el separador "**" no es igual a la longitud
        #      de la lista generada al separar el retorno del getter de txRg
        #      con el separador "**" la lista heredada será []
        #    la funcion realizar remplazo con argumentos el retorno del
        #     elemento del diccionario de atajos de la clase entregable al
        #     invocar la llave que retorne el getter de cbAt e idx
        #    la funcion resetear la interfaz de forma segura con argumento idx
        bt = tk.Button(root,text="Reemplazar y guardar texto",command=lambda:
            [updObj(list([(txRt.get().split("**")[i],txRg.get().split("**")[i])
            for i in range(len(txRt.get().split("**")))] if len(txRt.get(
            ).split("**")) == len(txRg.get().split("**")) else []),idx),updObj(
            Entregable.ATJ_RMP[cbAt.get()],idx),resetGUI(idx)])
        bt.grid(row=22,column=2,columnspan=2,sticky="NEWS")
        Hovertip(bt,"Reemplazar\nrealiza los reemplazos; guarda el texto con " +
            "reeplazos en el extracto",hover_delay=500)

    # Segmento: Zona Retroceso
    #   si bckRoll es del tipo tupla ejecuta el segmento
    #   bckRoll solo puede no ser del tipo tupla si es del tipo lista, osea si
    #   es el limite de retroceso
    if type(bckRoll) == tuple:
        # se genera bt, un button
        #  se asigna un comando de varios llamados con parámetros a través de
        #   una funcion lambda
        #   lambda llamará la funcion hacer un retroceso y la funcion resetear
        #    la interfaz de forma segura con argumento idx si idx es un indice
        #    y si idx es menor al retorno del getter n del objeto emtregable;
        #    sino con argumento None
        bt = tk.Button(root,text="Control-Z",command=lambda:[doBckRoll(),
            resetGUI(idx if idx != None and aporte.getN() > idx else None)])
        bt.grid(row=22,column=1,sticky="NEWS")
        Hovertip(bt,"Deshacer\nretrocede el estado de los extractos una vez\n" +
            "Se recomienda usar este botón por encima del atajo de teclado " +
            "Ctrl-Z",hover_delay=500)

    if idx == -1:
        lb = tk.Label(root,text= "¡Y este es tu aporte (con cariño) al " +
            "proyecto JEAN, " + (aporte.autor if aporte.autor != str(None) else
            f"pero ya ponte un nombre o te lo seguiré pidiendo, {aporte.autor}")
            +"! (k) Ka-Tet Co. 1999/Software libre",bg="#202020",fg="#303030",
            font="Consolas 9 italic")
    else:
        lb = tk.Label(root,text= "Producido con cariño en un ataque de ira " +
            "durante el paro de 2021 para el proyecto JEAN: (k) Ka-Tet Co. " +
            "1999/Software libre",bg="#202020",fg="#303030",font=
            "Consolas 9 italic")
    lb.grid(row=23,column=0,columnspan=4,sticky="NEWS")
    Hovertip(lb,"Una suerte de firma, anunciando el proyecto y referenciando " +
        "un copyright ficticio de uso libre\n¡Hile! Todas las cosas sirven " +
        "al Haz",hover_delay=5000)
    # trata de forzar el enfoque en la interfaz
    txEx.focus_force()
    root.focus_force()

def updAut(s: str = "Simplemente lo pediré ¿Tu nombre es?"):
    """ Función: Actualizar Autor

    Funcion que genera una peticion segura al objeto para usar
    su método setter autor.

    Parámetros:
        s (str) -- El mensaje con el que se desplegará el
        diálogo para la peticion (p.d. "Simplemente lo pediré
        ¿Tu nombre es?"
    """
    # pide al usuario un autor para settear al objeto entregable
    try: aporte.setAutor(input(s))
    except KeyboardInterrupt: pass #   ＼(-o- )
    # usa la funcion resetear la interfaz de forma segura sin importar el
    #  getter autor del objeto entregable
    finally: resetGUI()

def outGUI():
    """ Funcion: Salir de la Interfaz

    Funcion para salir de la interfaz de forma segura.
    """
    # confirmación de salida
    if messagebox.askokcancel("¡Oye Judas! no me dejes",
            'Antes de salir recomiendo que guardes el objeto y el entregable' +
            '\nDa clic en aceptar para cerrar todo:'):
        # destruye el marco
        marco.destroy()
        # finaliza la ejecucion
        sys.exit()

# generamos marco como una variable global del módulo sin inicializarla para
#  que al importar el módulo no se genere una interfaz vacía por defecto
marco = None
# generamos el objeto entregable como una variable global del módulo
#  usa el método constructor con su comodín obj == True para que automaticamente
#   el objeto se cree con el archivo objeto entregable
aporte = Entregable(obj = True)
# generamos el limite de retroceso como una variable global del módulo
#  usa el método getter extractos por defecto para obtener todos los extractos
#  así el objeto se convierte en una lista, sirviendo de límite si se usa la
#   funcion hacer un retroceso
bckRoll = aporte.getExtractos()

def main():
    """ Main: Ejecucion de Interfaz

    Ejecuta la interfaz.
    """
    # para sobreescribir la variable global se debe invocar
    global marco
    marco = tk.Tk()
    # si el getter autor del objeto entregable retorna None usa la función
    #  renombrar
    # si el getter autor del objeto entregable retorna diferente de None usa
    #  la función resetear la interfáz de forma segura
    if aporte.autor == str(None): updAut("No haz marcado tu archivo aún, no " +
        "te lo pedire de nuevo:")
    else: resetGUI()

    # se asigna un evento Control-z de varios llamados con varios a través
    #  de una funcion lambda con un parametro inservible
    #  lambda llamara a la funcion hacer un retroceso tras la confirmación del
    #   usuario y resetear la interfaz de forma segura sin confirmación
    marco.bind('<Control-z>', lambda dummy:[doBckRoll(), resetGUI()] if messagebox.
        askokcancel('Alto ahí, rufian', 'Activaste el atajo de teclado ' +
            '<Ctrl+Z> que afecta al objeto ¿Desea retroceder un paso sobre' +
            'el objeto?') else [])
    # se asigna un evento Escape de parámetro perdido a través de una funcion
    #  lambda con un parametro inservible
    #  lambda llamara a la funcion salir de la interfaz
    marco.bind('<Escape>', lambda dummy:outGUI())
    # se asigna un evento Control-u de parámetro perdido a través de una funcion
    #  lambda con un parametro inservible
    #  lambda llamara al sistema operativo para que ejecute el comando explorer
    #   explorer llamara al path absoluto para abrir el manual de usuario final
    marco.bind('<Control-u>', lambda dummy:os.system("explorer " +
        os.path.dirname(os.path.abspath(__file__)) +
        "\\Manuales Temporales\\Manual de usuario final.pdf"))
    # se asigna un evento Control-g de parámetro perdido a través de una funcion
    #  lambda con un parametro inservible
    #  lambda llamara al sistema operativo para que ejecute el comando start
    #   start redirigira a la carpeta de video-guias
    marco.bind('<Control-g>', lambda dummy:os.system("start " +
        "https://drive.google.com/drive/folders/1ZuXA-" +
        "FNLElBZdFk2MgIxdEgW65oZMyuv?usp=sharing"))
    # se asigna un evento Control-e de parámetro perdido a través de una funcion
    #  lambda con un parametro inservible
    #  lambda llamara al sistema operativo para que ejecute el comando start
    #   start redirigira a la nube de entrega
    marco.bind('<Control-e>', lambda dummy:os.system("start " +
        "https://drive.google.com/drive/folders/1ylcTjKPp2N0bpP4-" +
        "epVAtzv0vy_vvE2F?usp=sharing"))

    mn = tk.Menu(marco)
    # se genera flMn, un menu
    flMn =tk.Menu(mn, tearoff=0)
    # importa el módulo funciones avanzadas de recopilador de textos con
    #  un alias
    # si halla el módulo usa la funcion barra avanzada archivo con los
    #  argumentos flMn, aporte, un objeto callable lambda de varios llamados
    #  con parámetros y marco
    #  lambda llamará las funciones loadObj, chejov, resetGUI y
    #   loadGUI(marco,-1)]
    # si no halla el módulo ignora el importe
    try:
        import Furrcyones as FJ
        FJ.flBar(flMn,aporte,lambda:[loadObj(),chejov(),resetGUI(),loadGUI(
            marco,-1)],marco)
    except ModuleNotFoundError: pass

    # agrega las funciones aflMn
    flMn.add_command(label="Atrás <Ctrl+Z>",command=lambda:[doBckRoll(),
        resetGUI()])
    flMn.add_separator()
    flMn.add_command(label="Salir <Esc>",command=lambda:outGUI())
    # se genera hlMn, un menu
    hlMn =tk.Menu(mn, tearoff=0)
    # agrega las funciones aflMn
    hlMn.add_command(label="Manual de usuario final",command=lambda:os.system(
        "explorer " + os.path.dirname(os.path.abspath(__file__)) +
        "\\Manuales Temporales\\Manual de usuario final.pdf"))
    hlMn.add_command(label="Manual del programador",command=lambda:os.system(
        "start https://docs.google.com/document/d/1rr5pqEPb6-" +
        "_vN4Fz2edDKf73rSZuU6FBGCbITYqAsGg/edit?usp=sharing"))
    hlMn.add_command(label="Carpeta de video-guías",command=lambda:os.system(
        "start https://drive.google.com/drive/folders/1ZuXA-" +
        "FNLElBZdFk2MgIxdEgW65oZMyuv?usp=sharing"))
    hlMn.add_command(label="Consulta al líder JEAN",command=lambda:os.system(
        "start https://discord.com/channels/507661892450517000/" +
        "762888726971154442"))
        #"start https://www.facebook.com/messages/t/1406299817"))
    hlMn.add_command(label="Consulta al líder IAN",command=lambda:os.system(
        "start https://www.facebook.com/messages/t/100005951105444"))
    hlMn.add_command(label="Ir a la nube de entrega",command=lambda:os.system(
        "start https://drive.google.com/drive/folders/1ylcTjKPp2N0bpP4-" +
        "epVAtzv0vy_vvE2F?usp=sharing"))

    # importa el módulo funciones avanzadas de recopilador de textos con
    #  un alias
    # si halla el módulo usa la funcion barra avanzada ayuda con argumento hlMn
    # si no halla el módulo ignora el importe
    try: import Furrcyones as FJ; FJ.hlBar(hlMn)
    except: pass
    mn.add_cascade(label="Archivo",menu=flMn)
    mn.add_cascade(label="Ayuda",menu=hlMn)

    # configura la geometria, el rotulo, el fondo de color, el protocolo de
    #  cierre, el icono, la barra de menú, el control de tamaño y el
    #  poscisionamiento en pantalla de marco
    marco.geometry("+%d+%d" % (25, 25))
    marco.title(f'{aporte.autor}: Recopilador de Textos -JEAN (Proyecto IAN)')
    marco.configure(background='#202020')
    marco.protocol("WM_DELETE_WINDOW",lambda:outGUI())
    try: marco.iconbitmap('Icono.ico')
    except: pass
    marco.config(menu=mn)
    marco.resizable(0,0)
    marco.eval('tk::PlaceWindow . center')

    # maneja la excepcion KeyboardInterrupt, destruyendo el marco
    try: marco.mainloop()
    except KeyboardInterrupt:
        # destruye el marco
        marco.destroy()
        # finaliza la ejecucion
        sys.exit()
    finally:
        # *Se despide y va a su esquinita*
        print("Adiós, contare las semanas hasta tu regreso,", aporte.autor)

if __name__ == '__main__': main()
