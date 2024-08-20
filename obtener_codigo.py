import socket

#Funcion que obtiene el codigo empleado de la persona loggeada en la intranet
def obtenerCodigo():

    ip_local = obtener_ip_local()
    ruta = '//SRV-CCS-APP01/notifications/'+ip_local+'.txt' #lo guardamos en una variable

    with open(ruta) as archivo:
        codigo_empleado = archivo.read()
        return codigo_empleado
    
    
#Función que devuelve la IP local de un dispositivogmai


def obtener_ip_local():
    ip_local = socket.gethostbyname(socket.gethostname())
    return ip_local
