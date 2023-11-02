from flask import Flask,jsonify
from flask_cors import CORS
from flask.globals import request
from App_DAO import app_dao

app_manage = app_dao()

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "<h1> Hola MUNDO </h1>"   

@app.route("/grabarMensajes",methods =['POST'])
def upload_msj():
    if 'file' not in request.files:
        return jsonify({
            'mensaje' : "No se ha enviado ningun archivo, intenta cargar uno"
        })
    file = request.files['file']
    if file.filename=="":
        return jsonify({
            'mensaje' : "Error en el archivo, intenta cargar otro"
        })        
    mensajes_xml = file.read().decode('utf-8')
    print(mensajes_xml)
    app_manage.leer_mensaje(mensajes_xml)    
    return jsonify({
        'mensaje' : "El archivo fue cargado exitosamente!"
    }) 

@app.route("/grabarConfiguracion",methods =['POST'])
def upload_confi():
    if 'file' not in request.files:
        return jsonify({
            'mensaje' : "No se ha enviado ningun archivo, intenta cargar uno"
        })
    file = request.files['file']
    if file.filename=="":
        return jsonify({
            'mensaje' : "Error en el archivo, intenta cargar otro"
        })        
    configuracion_xml = file.read().decode('utf-8')
    app_manage.leer_configuracion(configuracion_xml)
    return jsonify({
        'mensaje' : "El archivo fue cargado exitosamente!"
    })

@app.route("/devolverDatos/<opcion>", methods=['GET'])
def get_Datos(opcion):
    fecha_inicio = request.args.get('inicio')
    fecha_fin = request.args.get('fin')
    if opcion == "Menciones":
        response = app_manage.consultar_menciones(fecha_inicio, fecha_fin)
    elif opcion == "Hashtags":
        response = app_manage.consultar_hashtags(fecha_inicio,fecha_fin)
    elif opcion == "Sentimientos":
        response = app_manage.consultar_sentimientos(fecha_inicio,fecha_fin)
    response_data = {"mensaje": response}
    return jsonify(response_data)

@app.route("/limpiarDatos",methods=['POST'])
def limpiarDatos():
    app_manage.clear_datos()
    return jsonify({
        'mensaje' : "Datos eliminados!"
    }) 

@app.route("/ayuda/datos_estudiante",methods=['GET'])
def mostrar_datos():
    return jsonify({
        'nombre' : "Rodrigo Sebastian Castro Aguilar",
        'carnet' : 202204496,
        'curso' : "Laboratorio de IPC2"
    })        

if __name__ == "__main__":
    app.run(threaded=True,port=5000,debug=True)