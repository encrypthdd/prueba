import pymysql
#from win10toast_click import ToastNotifier
import webbrowser
import time
from plyer import notification
#import socket
from obtener_codigo import obtenerCodigo


def open_url(url):
    webbrowser.open(url)


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
        msg_id = str(msg_id)
        codigo_out = str(outgoing_msg_id)
        message = str(msg)
        fecha = str(fecha)
            
        sql = "SELECT usuario, nombre, profile_pic FROM USUARIOS WHERE codigo = %s " %(codigo_out)
        cursor_user.execute(sql)
        for usuario, nombre, profile_pic in cursor_user.fetchall() :
            usuario = str(usuario)
            titulo = str(nombre)
            profile = str(profile_pic)
            print(titulo)

            # Título de la notificación
            title = titulo
            # Mensaje de la notificación
            message = message
            # Ruta de la imagen de la persona
            app_icon = 'P:/Carlos Flores/logo.ico'
            
            #app_icon = 'C:/Users/cflores/Pictures/images.ico'
            # URL que se abrirá al pulsar la notificación
            url = 'http://192.1.1.16/AppWeb/rori/chats/chat.php?user_id='+codigo_out
            
            notification.notify(
                title=title,
                message=message,
                app_name='RORI Chats',
                app_icon=app_icon,
            )

            # Crear un objeto ToastNotifier
            #toast = ToastNotifier()

            # Mostrar la notificación
            #toast.show_toast(title, message, icon_path=app_icon, duration=60, threaded=True, callback_on_click=lambda: open_url(url))
            #toast.show_toast(title, message, icon_path=app_icon, callback_on_click=lambda: open_url(url))
            
            sql_notification = "UPDATE messages SET desktop_notification = 'SI' WHERE msg_id = %s " % msg_id
            cursor_notification.execute(sql_notification)
            db.commit()  
            
    cursor.close()   
    db.close()


while True:
    codigo_empleado = obtenerCodigo()
    if (codigo_empleado != ""):
        buscarMensaje(codigo_empleado)
    time.sleep(30)