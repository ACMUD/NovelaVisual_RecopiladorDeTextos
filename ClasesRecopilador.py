#-------------------------------------------------------------------------------
# Name:        Clases de Recopilador de Textos
# Purpose:     Presentar las clases orientadas a almacenar extractos
#              de textos de manera propia para el proyecto de IAN
#
# Author:      PB203
#
# Created:     11/12/2021
# Copyright:   (k) Ka-Tet Co. 1999
# Licence:     <uranus>
#-------------------------------------------------------------------------------

""" Módulo: Clases de Recopilador de Textos

Presenta las clases orientadas a almacenar extractos de
textos de manera propia para el proyecto de IAN.

Recopila:
    Clase Extractor
    Clase Entregable
    Funcion encapsuladora Atajos Cambiantes
"""

from datetime import date
import string

def atjCambiantes(lmd: str) -> list(tuple((str,str))):
    """ Funcion encapsuladora: Atajos Cambiantes.

    Funcion en la cual se encapsulan diferentes funciones
    planteadas para ser implementadas con llaves especificas
    dentro del diccionario de atajos de la clase Entregable.

    El ser encapsulada probee un ahorro de memoria dinamico
    y un mantenimiento acorde a los principios SOLID.

    Listado de funciones encapsuladas (argumento de llamado):
        - Paginas Marcadas (pM)
        - Retorno Vacio ()

    Parámetros:
        lmd (str) -- argumento de llamado

    Retorno:
        una lista con tuplas, cada tupla contiene dos strings
            dependiendo del argumento de llamado
    """
    def paginaMarcada():
        """ Funcion: Paginas Marcadas

        Funcion que genera una lista de tuplas de a dos strings,
        cada tupla contiene un string construido por el usuario
        y otro string vacío. Anudado a la lista esta el remplazo
        'DOBLES SALTOS DE LÍNEA' del diccionario de atajos de la
        clase Entregable.

        Retorno:
            una lista con tuplas de a dos strings

        Excepciones:
            KeyboardInterrupt -- anulacion por el usuario o
                si no se introducen strings para construir
                el retorno
            TimeoutError -- si se ejecuta desde la interfaz
                y si se excede el tiempo predeterminado de
                respuesta del hilo de la interfaz
            EOFError -- si la construccion del retorno no
                se completa por algún error de digitacion
        """
        try:
            # pide al usuario un string en el cual puede incluir '{XX}' o no
            m = input("Introduzca las marcas de página identificadas; si la " +
                    "marca cambia según la\npágina con numeros inserte un " +
                    "'{XX}' donde deberia ir el número (Ej: el texto\ncopiado "+
                    "separa las páguinas diciendo 'Lectulandia 1' donde '1' " +
                    "es la página.\nEntonces en este cuadro de texto " +
                    "introduzco 'Lectulandia {XX}'\n-notese el espacio antes " +
                    "del '{XX}'):")
            # construccion del retorno en orden de ejecucion:
            #  si encuentra '{XX}' en m genera una lista guia
            #   para generar la lista guia pide al usuario un string
            #    con numeros separados por ';'
            #   la lista guia temdra tamaño según la cantidad de
            #    numeros dados por el usuario
            #  si no encuentra '{XX}' en m genera una lista guia vacía
            #   la lista guia vacía tendra tamaño 1 y solo el elemento ""
            #  construye el retorno agregando tuplas
            #   cada tupla agrega dos strings
            #    el primer string será m remplazando '{XX}' por los
            #     elementos en la lista guia
            #    el segundo string será ""
            #   agrega al retorno construido la lista Entregable.ATJ_RMP[
            #    "DOBLES SALTOS DE LÍNEA"]
            #   el tamaño del retorno sera el de la lista guia más dos
            return [(m.replace("{XX}",str(i)),"") for i in ([""] if m.find(
                        "{XX}") == -1 else input("Introduzca los numeros de " +
                        "páginas que hay en\nel texto separadas por punto y " +
                        "coma ';' (Ej: 2;3;4;7):").split(";"))
                        ] + Entregable.ATJ_RMP["DOBLES SALTOS DE LÍNEA"]
        except KeyboardInterrupt: return Entregable.ATJ_RMP[""]
        except TimeoutError: return Entregable.ATJ_RMP[""]
        except EOFError: return Entregable.ATJ_RMP[""]

    # condicional de funciones encapsuladas según el argumento
    if lmd == "pM": return paginaMarcada()
    return Entregable.ATJ_RMP[""] # retorno por defecto

class Extracto:
    """ Clase: Extracto

    Objeto en el que se agrupa un texto, una longitud, un
    género, una clasificación y un supuesto de finalización.

    Agrupa métodos estáticos utiles para el tratamiento de
    textos.
    """
    def __init__(self,txt: str,nd: bool,gn: str,cls: str):
        """ Método dunder: Constructor Extracto

        Recibe parametros necesarios para generar un objeto de
        la clase Extracto.

        Parámetros:
            txt (str) -- un texto
            nd (bool) -- un booleano que representa la posible
                finalización de txt
            gn (str) -- un género narrativo al cual pertenece
                el txt; debe estar en la lista de GNS de la
                clase Entregable
            cls (str) -- una clasificacion literaria que
                conforma txt; debe estar en la lista de CLS de
                la clase Entregable

        Excepciones:
            AssertionError (Booleano de finalización pasado
                erróneo) -- Si el argumento nd no es del tipo
                bool
            AssertionError (Género pasado erróneo) -- Si el
                argumento gn no esta en GNS
            AssertionError (Clasificación pasado erróneo) --
                Si el argumento cls no esta en CLS
        """
        # este metodo contiene un assert que verifica que txt sea de tipo str
        self.longitud = self.calcLngTxt(txt)
        self.texto = txt
        assert type(nd) == bool, "Booleano de finalización pasado erróneo"
        self.fin = nd
        assert gn in Entregable.GNS, "Género pasado erróneo"
        self.genero = gn
        assert cls in Entregable.CLS, "Clasificación pasado erróneo"
        self.clase = cls

    def __str__(self, paExc: bool = False,legible: bool = False, soloTxt:
            bool = False) -> str:
        """ Método dunder: String Extracto

        Método integrado que invoca python para convertir
        los objetos al tipo str. El método esta adaptado
        para diferentes versiones necesarias en ejecucion
        de la conversión a str.

        Parámetros:
            paExc (bool) -- booleano que afecta la
                conversión, adaptandolo para excel. Si paEx
                es True el retorno incluye self.longitud y
                hace que el separador entre datos sea '\t'.
                Si paEx es False hace que el separador
                entre datos sea '\n' (p.d. False)
            legible (bool) -- booleano que afecta la
                conversión, haciendo legible self.texto. Si
                legible es True hace que self.texto tenga
                carácteres especiales. Si legible es False
                hace que self.texto no tenga caracteres
                especiales (p.d. False)
            soloTxt (bool) -- booleano que afecta la
                conversión, haciendo que solo se devuelva
                self.texto. Si soloTxt es True solo
                devuelve self.texto. Si soloTxt es False
                devuelve otros datos aparte de self.texto
                (p.d. False)

        Retorno:
            una cadena de texto con datos del objeto
        """
        # construccion del retorno en orden de ejecucion:
        #  si no legible o si legible pero self.texto esta sin
        #   carácteres especiales agrega al retorno self.texto sin
        #    carácteres especiales
        #  si legible esta con carácteres especiales agrega al retorno
        #   self.texto
        #  si soloTxt no agrega más al retorno
        #  si no soloTxt continua revizando los condicionales
        #   si paExc agrega al retorno '\t', self.longitud y '\t'
        #   si no paExc agrega al retorno '\n'
        #   agrega al retorno self.fin en minúsculas
        #   si paExc agrega al retorno '\t'
        #   si no paExc agrega al retorno '\n'
        #   agrega al retorno self.genero
        #   si paExc agrega al retorno '\t'
        #   si no paExc agrega al retorno '\n'
        #   agrega al retorno self.clase
        return (ascii(self.texto)[1:-1] if not legible or (legible and self.
            is_ascii(self.texto)) else self.texto) + str("" if soloTxt else str(
                (str('\t' + str(self.longitud) + '\t') if paExc else '\n') +
                    str(self.fin).lower() + ('\t' if paExc else '\n') +
                        self.genero + ('\t' if paExc else '\n') + self.clase))

    def __eq__(self,comp: None) -> bool:
        """ Método dunder: Equivalencia Extracto

        Metodo integrado que invoca python para considerar
        si otro objeto iguala al objeto self.

        Parámetros:
            comp (Extracto) -- extracto a comparar con
                self

        Retorno:
            un booleano que determina si comp equivale a
                self
        """
        return type(comp) == Extracto and [comp.texto,comp.longitud,comp.fin,comp.genero,
            comp.clase] == [self.texto,self.longitud,self.fin,
            self.genero,self.clase]

    # Método dunder: Iterador del Extracto
    def __iter__(self): yield from self.__dict__.items()

    # Método dunder: Subscriptor del Extracto
    def __getitem__(self, s: str = "texto"):
        try: return dict(self)[s]
        except KeyError: return self

    @staticmethod
    def calcLngTxt(txt: str) -> int:
        """ Método de clase: Calcular Longitud de Texto

        Calcula el numero de palabras en txt, teniendo en
        cuenta separadores discretos de palabras como
        ligaduras y contracciones.

        Parámetros:
            txt (str) -- un texto

        Retorno:
            numero de palabras del texto

        Excepciones:
            AssertionError (Texto pasado erróneo) -- si el
            argumento txt no es del tipo str
        """
        assert type(txt) == str, "Texto pasado erróneo"
        #s.maketrans({i: " " for i in string.punctuation}) #Nada importante
        # construccion del retorno en orden de ejecucion:
        #  genera una cadena
        #  genera un diccionario en el que cada llave es un carácter en
        #   string.puntation y cada elemento es " "
        #  si encuentra c en el diccionario agrega el elmento en c a la cadena
        #  si no encuentra c en el diccionario agrega c a la cadena
        #  separa la cadena en una lista
        #  calcula y retorna la longitud de la lista
        return len(str("".join([{i: " " for i in string.punctuation}.get(
            c,c) for c in txt])).split())

    @staticmethod
    def is_ascii(txt: str) -> bool:
        """ Método de clase: Es Ascii

        Define si txt contiene caracteres especiales o no.

        Parámetros:
            txt (str) -- un texto

        Retorno:
            un booleano
        """
        # comprueba que cada c en txt cumpla que al convertirse en ordinal
        #  esté antes del ordinal 128
        return all(ord(c) < 128 for c in str(txt))

    @staticmethod
    def ascii2char(txt: str, forced: bool = False) -> str:
        """ Método de clase: Ascii a Char

        Devuelve txt sin carácteres especiales si los
        tiene, o con carácteres especiales si no los
        tiene o si forced es verdadero.

        Parámetros:
            txt (str) -- un texto
            forced (bool) -- un booleano que condiciona
            el retorno (p.d. False)

        Retorno:
            un texto
        """
        # si no self.is_ascii(txt) y no forced retorna ascii(txt)
        # si self.is_ascii(txt) o forced retorna txt tras codificarlo a unicode,
        #  reemplazar los carácteres '\\' a '\' y decodificarlo a unicode
        return ascii(txt)[1:-1] if not Extracto.is_ascii(txt) and not forced else (
            txt.encode('unicode-escape').replace(b'\\\\', b'\\').decode(
            'unicode-escape'))

    @staticmethod
    def cod2char(txt: str) -> str:
        """ Método de clase: Código a Char

        Devuelve txt en carácteres si está codificado,
        o codificado si no los está.

        Parámetros:
            txt (str) -- un texto

        Retorno:
            un texto
        """
        # conteo de \ en txt, asignado en a para ahorrar ciclos en la siguiente linea
        a = txt.count("\\")
        # si txt contiene la misma cantidad de / y \ que no es 0 retorna
        #  txt tras
        #   dividirlo por / y convertir cada código a carácter
        # si txt no contiene / ni \ o si no coincide el conteo de / y \ retorna
        #  txt tras codificarlo al convertir cada carácter a ordinal
        return ''.join(chr(int(c[:-1])) for c in txt.split("/")[1:]
            ) if a != 0 and a == txt.count("/") else ''.join(f"/{ord(c)}\\"
                for c in txt)

class Entregable:
    """ Clase: Entregable

    Clase en la que se agrupan los generos narrativos, las
    clasificaciones literarias, el nombre por defecto del
    archivo entregable, los limites cerrados de palabras
    por texto, los limites cerrados de extractos por
    entregable y el diccionario de atajos.

    Objeto en el que se agrupan extractos, un autor y la
    fecha de inicio.

    Agrupa métodos estáticos utiles para guardar y cargar
    el archivo entregable.
    """
    GNS = ['AVENTURA','COMEDIA','FANTASIA','TERROR','ACCIÓN','THRILLER',
        'ROMANCE','CIENCIA FICCIÓN','DRAMA','MISTERIO']
    CLS = ['DIALOGO','PUENTE','NARRATIVA']
    OBJ = "objEntregable.txt"
    LIM_WORDS = (300,2000)
    LIM_EXTRA = (7,48)
    # ATJ_RMP es un diccionario de atajos de remplazo
    #  cada llave es un nombre de auto-exhibición sobre el atajo
    #  cada elemento es una lista con tuplas, cada tupla es un par
    #   cada par contiene un string para ser remplazado y un string de remplazo
    ATJ_RMP = {"":[],#('','')],
               "DOBLES SALTOS DE LÍNEA": [("\\\\n\\n","\\n"),
                    ("\n\n","\n")],
               "SALTOS DE LÍNEA FALSOS": [(".\\\\n","saltodelinearealconpunto"),
                    ("\\\\n"," "),
                    ("saltodelinearealconpunto",".\\n"),
                    (".\n","saltodelinearealconpunto"),
                    ("\n"," "),
                    ("saltodelinearealconpunto",".\n")],
               "SALTOS DE PÁGINA CON MARCAS": lambda: atjCambiantes("pM")}

    def __init__(self,auth: str = None,etrs: list = [],obj: [None,bool] = None):
        """ Método dunder: Constructor Entregable

        Recibe parametros necesarios u oportunos para generar
        un objeto de la clase Entregable.

        Parámetros:
            auth (str) -- un nombre (p.d. None)
            etrs (list) -- una lista de extractos (p.d. [])
            obj (Entregable,bool) -- un comodín que altera la
                construcción del objeto; si obj es del tipo
                Entregable construye el objeto basado en los
                atributos de obj; si obj es True construye el
                objeto basado en los atributos del objeto
                plano entregable; si obj es None lo ignora
                (p.d. None)
        """
        if type(obj) == Entregable:
            self.__init__(obj.autor,obj.getExtractos())
            # inicializa la fecha de inicio de self según la de obj
            self.__primer = obj.__primer
        # pide nuevamente la construcción de self, pasando como obj
        #  Entregable.loadObj()
        elif obj == True: self.__init__(obj = Entregable.loadObj())
        else:
            self.autor = str(auth)
            # si etrs es del tipo list lo asigna a self. extractos sino
            #  asigna []
            if type(etrs) == list: self.setExtractos(etrs)
            else: self.reset()
            # asigna a self.__primer la fecha actual
            self.__primer = date.today()

    def __str__(self, conAut: bool = False) -> str:
        """ Método dunder: String Entregable

        Método integrado que invoca python para convertir
        los objetos al tipo str. El método esta adaptado
        para una alternancia necesaria en ejecucion de la
        conversión a str.

        Parámetros:
            conAut (bool) -- booleano que afecta la
                conversión, agregando self.autor al retorno
                solo si conAut es True (p.d. False)

        Retorno:
            una cadena de texto con los extractos
        """
        # si conAut agrega self.autor al inicio del retorno
        # concatena los extractos, apelando al método dunder str de cada uno
        return str(f'{self.autor}:\n' if conAut else '') + ''.join([
            f'{i.__str__()}\n' for i in self.__extractos])

    @staticmethod
    def loadObj() -> None:
        """ Método de clase: Cargar Entregable

        Devuelve el objeto almacenado en el archivo plano.

        Retorno:
            un Entregable
        """
        import pickle
        # intenta realizar el proceso hasta que cargue el objeto plano
        while True:
            # asigna a stt el objeto plano y rompe el ciclo
            try:stt = open(Entregable.OBJ,"rb"); break
            # al no encontrar el archivo usa el método de clase para crearlo
            except FileNotFoundError: Entregable.saveObj()
            except pickle.UnpicklingError: Entregable.saveObj()
        obj = pickle.load(stt)
        stt.close()
        return obj

    @staticmethod
    def saveObj(obj: None = None):
        """ Método de clase: Guardar Entregable

        Guarda el argumento obj en el archivo plano.

        Parámetros:
            obj (Entregable) -- un Entregable o ningún
                objeto
        """
        # si obj no es del tipo Entregable entonces le asigna un Entregable
        #  generico con los argumentos por defectos del constructor
        obj = Entregable() if type(obj) != Entregable else obj
        import pickle
        # guarda obj en el archivo plano
        stt = open(Entregable.OBJ,"wb")
        pickle.dump(obj,stt)
        stt.close()

    # Método: Setter Autor
    def setAutor(self,newA: str): self.autor = newA

    def getExtractos(self,idx: int = None) -> (list, Extracto):
        """ Método: Getter Extractos

        Parámetros:
            idx (int) -- indice del extracto a devolver; si
                idx es None devuelve self.__extractos
                (p.d. None)

        Retornos:
            si halla idx en self.__extractos retorna el
                elemento del indice
            si no halla idx o idx es incongruente retorna
                self.__extractos
        """
        try: return self.__extractos[idx] if idx != None else self.__extractos
        except IndexError: print("Error de índice"); return self.__extractos
        except TypeError: print("Error de índice"); return self.__extractos

    # Método: Setter Extractos
    #  por defecto el argumento de setteo es []
    def setExtractos(self,newEx: list = []): self.__extractos = newEx

    # Método: Reiniciar Extractos
    #  utiliza el método setter extractos por defecto
    def reset(self): self.setExtractos()

    # Método: Guardar Objeto
    #  utiliza el método de clase guardar entregable con el argumento self
    def save(self): Entregable.saveObj(self)

    # Método: Cargar Objeto
    #  utiliza el constructor pasando el argumento obj según el argumento new
    #   si new es None pasa True de argumento obj
    #   si new no es None pasa new de argumento obj
    def load(self,new: None = None): self.__init__(obj = True if new == None
        else new)

    # Método: Get N
    # retorna la longitud de self.__extractos
    def getN(self) -> int: return len(self.__extractos)

    def addExtractos(self,obj: (list,Extracto,None,dict) = [],txt: str =
        None,end: bool = False,gen: str = None,cls: str = None,idx: int = None):
        """ Método: Agregar a Extractos

        Agrega a los extractos nuevos datos según el
        indice idx; si el indice no existe añade un nuevo
        extracto con los datos.

        Parámetros:
            obj (list,Extracto,Entregable,dict) -- un
                comodín que altera el extracto a agregar;
                si obj es del tipo lista se agragan todos
                los elementos del tipo Extracto que
                contenga obj; si obj es del tipo Extracto
                se agrega; si obj es de tipo dict se
                genera un Extracto con el contenido de
                obj y se agrega (p.d. [])
            txt (str) -- un texto (p.d. None)
            end (bool) -- un booleano que representa la
                posible finalización de txt (p.d. False)
            gen (str) -- un género narrativo al cual
                pertenece el txt; debe estar en la lista
                GNS de la clase Entregable (p.d. None)
            cls (str) -- una clasificacion literaria que
                conforma txt; debe estar en la lista CLS
                de la clase Entregable (p.d. None)
            idx (int) -- un indice al cual se asignara
                el extracto a agregar; si idx es None se
                agregara al final el extracto (p.d.
                None)

        Excepciones:
            AssertionError (Argumentos pasados erróneos)
                -- si al crear el extracto los
                parámetros no cumplen con los
                requisitos del constructor extractos
            AssertionError (Contenidos de diccionario
                pasados erróneos) -- si los contenidos
                del diccionario obj no cumplen con los
                requisitos del constructor extractos
            KeyError -- si las llaves del diccionario
                obj no son las correctas
        """
        try:
            if [txt,end,gen,cls] != [None,False,None,None]:
                if idx==None:self.__extractos.append(Extracto(txt,end,gen,cls))
                else:self.__extractos[idx] = Extracto(txt,end,gen,cls)
        except AssertionError as A:print("Argumentos pasados erróneos\n"+str(A))
        finally:
            if type(obj) == Entregable:
                self.__extractos += [i for i in obj.getExtractos() if type(i)
                    == Extracto]
            elif type(obj) == Extracto:
                if idx == None: self.__extractos.append(obj)
                else: self.__extractos[idx] = obj
            elif type(obj) == dict:
                try:
                    if idx == None: self.__extractos.append(Extracto(obj["txt"],
                        obj["end"],obj["gen"],obj["cls"]))
                    else:self.__extractos[idx] = Extracto(obj["txt"],obj["end"],
                            obj["gen"],obj["cls"])
                except AssertionError as A: print(
                    "Contenidos de diccionario pasados erróneos\n" + str(A))
                except KeyError: print("Llaves de diccionario pasadas erróneas")
            elif type(obj) == list:
                self.__extractos += [i for i in obj if type(i) == Extracto]

    # Método: Eliminar de Extractos
    #  elimina el elemento del indice idx de self.__extractos
    def delExtracto(self,idx: int): self.__extractos.pop(idx)

    def saveFl(self):
        """ Método: Guardar Archivo

        Genera el archivo plano entregable de manera
        legible. Le asigna de nombre al archivo
        self.autor, remplazando los signos de puntuacion
        por espacios y agregando un numero según las
        semanas desde la creacion del entregable.
        """
        # para crear el nombre del archivo
        #  genera una cadena en la cual va agregando cada carácter dentro de
        #   self.autor
        #   si el carácter esta en string.puntuation agrega " " sino agrega el
        #    carácter
        #  agrega a la cadena 'm' y el resultado de la diferencia en dias entre
        #   self.__primer y el día actual sin el 'm' del comienzo
        #  remplaza 'm0.txt' por 'm.txt'; por si es la primera semana de entrega
        fl = open(
            str("".join(("" if c in string.punctuation + " " else c) for c in
                self.autor)) + str(f'm{(self.__primer - date.today()).days//7}'+
                '.txt').replace("m0.txt","m.txt")[1:], 'w')
        # utiliza el método dunder str y lo escribe en el archivo
        fl.write(self.__str__()[:-1])
        fl.close()

    # Método: Extractos Excedidos
    #  compara el retorno del método Get N con el Limite superior de extractos
    #   por entregable
    def isTLDR(self) -> bool: return self.getN() > Entregable.LIM_EXTRA[1]

def main():
    """ Main: Registro Pruebas Unitarias

    Así probé que todo sirviera, y aun así tiene errores.
    """
    #d = Entregable(obj = Entregable.loadObj())
    #d = Entregable(obj = True)
    #d = Entregable("Pedro")
    '''
    d.addExtractos(obj = Extracto('TOM!\nNo ánswer.\n"TOM!"\nNo answer.',False,
        "AVENTURA","NARRATIVA"))
    d.addExtractos(obj = [Extracto('TOM!\nNo ánswer.\n"TOM!"\nNo answer.',False,
        "AVENTURA","NARRATIVA"),Extracto('TOM!\nNo ánswer.\n"TOM!"\nNo answer.',
            False,"AVENTURA","NARRATIVA")])
    d.addExtractos(obj = {"txt": 'TOM!\nNo ánswer.\n"TOM!"\nNo answer.',
        "end": False,"gen": "AVENTURA","cls": "NARRATIVA"})
    d.addExtractos(txt='TOM!\nNo ánswer.\n"TOM!"\nNo answer.',end=False,
        gen="AVENTURA",cls="NARRATIVA")
    '''
    #print(d.ascii2char(d.ascii2char(d.texto)))
    #d.save()
    #d.saveFl()
    #print(d.getExtractos(0).__str__(True,True))
    #print(d)

if __name__ == '__main__': main()
