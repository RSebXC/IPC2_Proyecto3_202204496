from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import xml.etree.ElementTree as ET
from Objetos.mensaje import mensaje
from Objetos.usuario import usuario
from Objetos.hashtag import hashtag
from Objetos.sentimiento import sentimientos
import re


class app_dao:
    def __init__(self):
        self.mensajes = []
        self.usuarios = []
        self.hashtags = []
        self.sentimientos_positivos = []
        self.sentimientos_negativos = []
        self.sentimientos_manage = sentimientos()
    
    def leer_mensaje(self,xml):
        root = ET.fromstring(xml)
        for msj in root.findall('MENSAJE'):
            fecha = msj.find('FECHA').text
            texto = msj.find('TEXTO').text
            self.mensajes.append(mensaje(fecha,texto))

    def leer_configuracion(self,xml):
        root = ET.fromstring(xml)
        self.sentimientos_positivos = [elem.text for elem in root.find('sentimientos_positivos').findall('palabra')]
        print('Sentimientos Positivos:', self.sentimientos_positivos)
        self.sentimientos_negativos = [elem.text for elem in root.find('sentimientos_negativos').findall('palabra')]
        print('Sentimientos Negativos:', self.sentimientos_negativos)

    def analizar_mensaje(self, fecha_inicio, fecha_fin):
        self.sentimientos_manage.reset()
        # Convertir las fechas de cadena a datetime
        fecha_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")

        for texto in self.mensajes:
            cadena = texto.texto.lower()
            fecha_mensaje = datetime.strptime(texto.fecha, "%d/%m/%Y")

            # Comprobar si la fecha de mensaje está dentro del rango de fechas
            if fecha_inicio <= fecha_mensaje <= fecha_fin:
                print("Cadena:",cadena)
                usuarios_leidos = re.findall(r'(@\w+)', texto.texto.lower())
                hashtags_leidos = re.findall(r'#(.*?)#', texto.texto.lower())

                for user in usuarios_leidos:
                    print("Estamos con el usuario",user,"------------")
                    cadena = cadena.replace(user, '')
                    
                    usuario_encontrado = False            
                    for elemento in self.usuarios:
                        print("Entro al cilo for",elemento.nombre)
                        if elemento.nombre == user:
                            print("Incrementando cantidad...")
                            elemento.plus_menciones()
                            usuario_encontrado = True
                            break            
                    if not usuario_encontrado:
                        print("Creando nuevo usuario",user)
                        self.usuarios.append(usuario(user))
                                        
                for hs in hashtags_leidos:
                    cadena= cadena.replace('#' + hs + '#', '')
                    encontrado = False            
                    for elemento in self.hashtags:
                        print("Entro al cilo for")
                        if elemento.nombre == hs:
                            print("Incrementando cantidad...")
                            elemento.plus_menciones()
                            encontrado = True
                            break            
                    if not encontrado:
                        print("Creando nuevo usuario",hs)
                        self.hashtags.append(hashtag(hs))
                
                self.buscar_sentimiento(cadena)

        print("\nEntro conteo usuarios")
        for user in self.usuarios:
            print(user.nombre, user.menciones)
        print("\nEntro conteo hastag")
        for hs in self.hashtags:
            print(hs.nombre, hs.menciones)        

        print("\nSentimientos Positivos:",self.sentimientos_manage.positivo)
        print("\nSentimientos Negativos:",self.sentimientos_manage.negativo) 
        print("\nSentimientos Neutros:",self.sentimientos_manage.neutro)

    def consultar_hashtags(self, fecha_inicio, fecha_fin):
        response = ""
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

        for texto in self.mensajes:
            hashtags = []
            fecha_mensaje = datetime.strptime(texto.fecha, "%d/%m/%Y")

            # Comprobar si la fecha de mensaje está dentro del rango de fechas
            if fecha_inicio <= fecha_mensaje <= fecha_fin:
                hashtags_leidos = re.findall(r'#(.*?)#', texto.texto.lower())
                                        
                for hs in hashtags_leidos:
                    encontrado = False            
                    for elemento in hashtags:
                        if elemento.nombre == hs:
                            elemento.plus_menciones()
                            encontrado = True
                            break            
                    if not encontrado:
                        print("Creando nuevo usuario",hs)
                        hashtags.append(hashtag(hs))
                response += texto.fecha+"\n"
                contador = 0
                for hs in hashtags:
                    contador += 1
                    cadena = f"{contador}.  #{hs.nombre}# : {hs.menciones} mensajes \n"
                    response += cadena
        print(response)                
        return response

    def consultar_menciones(self, fecha_inicio, fecha_fin):
        response = ""
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

        for texto in self.mensajes:
            usuarios = []
            fecha_mensaje = datetime.strptime(texto.fecha, "%d/%m/%Y")

            if fecha_inicio <= fecha_mensaje <= fecha_fin:
                usuarios_leidos = re.findall(r'(@\w+)', texto.texto.lower())

                for user in usuarios_leidos:
                    print("Estamos con el usuario",user,"------------")                    
                    usuario_encontrado = False            
                    for elemento in usuarios:
                        print("Entro al ciclo for",elemento.nombre)
                        if elemento.nombre == user:
                            print("Incrementando cantidad...")
                            elemento.plus_menciones()
                            usuario_encontrado = True
                            break            
                    if not usuario_encontrado:
                        print("Creando nuevo usuario",user)
                        usuarios.append(usuario(user))
                response += texto.fecha+"\n"
                contador = 0
                for user in usuarios:
                    contador += 1
                    cadena = f"{contador}.  {user.nombre} : {user.menciones} mensajes \n"
                    response += cadena
        print(response)
        return response
    
    def consultar_sentimientos(self, fecha_inicio, fecha_fin):
        response = ""       
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

        for texto in self.mensajes:
            self.sentimientos_manage.reset()
            cadena = texto.texto.lower()
            fecha_mensaje = datetime.strptime(texto.fecha, "%d/%m/%Y")

            # Comprobar si la fecha de mensaje está dentro del rango de fechas
            if fecha_inicio <= fecha_mensaje <= fecha_fin:
                usuarios_leidos = re.findall(r'(@\w+)', texto.texto.lower())
                hashtags_leidos = re.findall(r'#(.*?)#', texto.texto.lower())

                for user in usuarios_leidos:
                    cadena = cadena.replace(user, '')
                                        
                for hs in hashtags_leidos:
                    cadena= cadena.replace('#' + hs + '#', '')

                response += texto.fecha+"\n"             
                self.buscar_sentimiento(cadena)
                response += "Sentimientos Positivos: "+str(self.sentimientos_manage.positivo)+"\n"
                response += "Sentimientos Negativos: "+str(self.sentimientos_manage.negativo)+"\n"
                response += "Sentimientos Neutros: "+str(self.sentimientos_manage.neutro)+"\n"
        return response       

    def buscar_sentimiento(self,cadena):
        positivo = 0
        negativo = 0
        palabras = cadena.lower().split()
        
        for palabra in palabras:
            if palabra in self.sentimientos_positivos:
                positivo += 1
            elif palabra in self.sentimientos_negativos:
                negativo += 1
        
        if positivo > negativo:
            self.sentimientos_manage.plus_positivo()
        elif positivo < negativo:
            self.sentimientos_manage.plus_negativo()
        elif positivo == negativo:
            self.sentimientos_manage.plus_neutro()                            


    def mostrar_mensaje(self):
        for mensaje in self.mensajes:
            print(mensaje.texto)

    def clear_datos(self):
        print("Se procedera a limpiar los datos...")
        self.mensajes = []
        self.usuarios = []
        self.hashtags = []
        self.msj_positivos = []
        self.msj_negativos = []    

    def generar_xml(self):
        generador_xml = GeneradorXML(self.mensajes)
        return generador_xml.generar_xml()



class GeneradorXML:
    def __init__(self, mensajes):
        self.mensajes = mensajes

    def generar_xml(self):
        root = Element("MENSAJES_RECIBIDOS")

        for mensaje in self.mensajes:
            tiempo_element = SubElement(root, "TIEMPO")
            fecha_element = SubElement(tiempo_element, "FECHA")
            fecha_element.text = mensaje.fecha

            msj_recibidos_element = SubElement(tiempo_element, "MSJ_RECIBIDOS")
            msj_recibidos_element.text = mensaje.texto

            usr_mencionados_element = SubElement(tiempo_element, "USR_MENCIONADOS")
            usr_mencionados_element.text = " ".join(mensaje.usuarios_mencionados)

            hash_incluidos_element = SubElement(tiempo_element, "HASH_INCLUIDOS")
            hash_incluidos_element.text = " ".join(mensaje.hashtags_incluidos)

        return self.formatear_xml(root)

    def formatear_xml(self, elem):
        rough_string = tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")