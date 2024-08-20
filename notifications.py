import pymysql
from win10toast_click import ToastNotifier
import webbrowser
import time
#import socket
from obtener_codigo import obtenerCodigo


def open_url(url):
    webbrowser.open(url)


def muestraNotificacion(titulo, message, icono, url):
    
    # Título de la notificación
    title = titulo
    # Mensaje de la notificación
    message = message
    # Ruta de la imagen de la persona
    app_icon = icono
    # URL que se abrirá al pulsar la notificación
    url = url
    # Crear un objeto ToastNotifier
    toast = ToastNotifier()
    # Mostrar la notificación
    toast.show_toast(title, message, icon_path=app_icon, callback_on_click=lambda: open_url(url))
    

def buscarTicket(codigo_empleado):

    # Open database connection
    db = pymysql.connect(
        host="192.1.1.16",
        user="python",
        passwd="rori2019",
        db="intranet"
    )
    
    # Cursor
    cursor_usuario = db.cursor()
    cursor_dirigido = db.cursor()
    cursor_ticket = db.cursor()
    cursor_notification = db.cursor()
    
    sql = "SELECT usuario FROM usuarios WHERE codigo = %s " %(codigo_empleado)
    cursor_usuario.execute(sql)
    for usuario in cursor_usuario.fetchall() :
        usuario=str(usuario[0])
        
    sql = "SELECT id_dirigido FROM dirigido WHERE user = '%s' " %(usuario)
    cursor_dirigido.execute(sql)
    for id_dirigido in cursor_dirigido.fetchall() :
        id_dirigido=str(id_dirigido[0])
        
    sql = "SELECT A.estatus AS estatus, A.id_ticket AS ticket, A.id_usuario AS remitente, A.id_asunto AS id_asunto, A.porcentaje AS porcentaje, B.name AS nombre_estatus, C.asunto AS asunto FROM ticket_rori A, status B, asuntos C WHERE A.estatus = B.id AND A.id_asunto = C.id_asunto AND (atendido = '%s' OR dirigido = '%s') AND desktop_notification <> 'SI' " %(usuario, id_dirigido)
    cursor_ticket.execute(sql)
    for estatus, ticket, remitente, id_asunto, porcentaje, nombre_estatus, asunto in cursor_ticket.fetchall() :
        estatus=str(estatus)
        ticket=str(ticket)
        remitente=str(remitente)
        id_asunto=str(id_asunto)
        nombre_estatus=str(nombre_estatus)
        asunto=str(asunto)
        porcentaje=str(porcentaje)
        print(asunto)
        
        if (estatus=='1'):
            titulo = 'Generación Ticket # '+ ticket + ' - Estatus: ' + nombre_estatus + ' ' + porcentaje + '%'
        else:
            titulo = 'Actualización Ticket # '+ ticket + ' - Estatus: ' + nombre_estatus + ' ' + porcentaje + '%'
            
        message = asunto
        icono = 'P:/Carlos Flores/Ticket2.ico'
        url = 'http://192.1.1.16/AppWeb/rori/Tickets/tickets.php'
        
        muestraNotificacion(titulo, message, icono, url)
        
        sql_notification = "UPDATE ticket_rori SET desktop_notification = 'SI' WHERE id_ticket = %s " % ticket
        cursor_notification.execute(sql_notification)
        db.commit() 
        
        
        
def buscarMensaje(codigo_empleado):

    # Open database connection
    db = pymysql.connect(
        host="192.1.1.16",
        user="python",
        passwd="rori2019",
        db="intranet"
    )
    
    # Cursor
    cursor = db.cursor()
    cursor_user = db.cursor()
    cursor_notification = db.cursor()

    sql = "SELECT msg_id, outgoing_msg_id, msg, fecha FROM messages WHERE incoming_msg_id = %s and estatus = '3' AND desktop_notification = '' ORDER BY outgoing_msg_id, fecha asc" %(codigo_empleado)

    #Ejecuta SQL
    cursor.execute(sql)

    for msg_id, outgoing_msg_id, msg, fecha in cursor.fetchall() :
        msg_id=str(msg_id)
        codigo_out=str(outgoing_msg_id)
        message=str(msg)
        fecha=str(fecha)
            
        sql = "SELECT usuario, nombre, profile_pic FROM USUARIOS WHERE codigo = %s " %(codigo_out)
        cursor_user.execute(sql)
        for usuario, nombre, profile_pic in cursor_user.fetchall() :
            usuario = str(usuario)
            titulo=str(nombre)
            profile=str(profile_pic)
            print(titulo)
            
            icono = 'P:/Carlos Flores/logo.ico'
            url = 'http://192.1.1.16/AppWeb/rori/chats/chat.php?user_id='+codigo_out
            
            muestraNotificacion(titulo, message, icono, url)
            
            sql_notification = "UPDATE messages SET desktop_notification = 'SI' WHERE msg_id = %s " % msg_id
            cursor_notification.execute(sql_notification)
            db.commit()  
            
    cursor.close()   
    db.close()
    
    buscarTicket(codigo_empleado)


while True:
    codigo_empleado = obtenerCodigo()
    if (codigo_empleado != ""):
        buscarMensaje(codigo_empleado)
    time.sleep(30)