from flask import Flask, render_template, request
from flask_mysqldb import MySQL

#Se crea una aplicacion flask
app= Flask(__name__)

#Se especifica en donde estara la base de datos, por ejemplo localhost
app.config['MYSQL_HOST']='bfrbtunhryqfh3eywkgx-mysql.services.clever-cloud.com'
app.config['MYSQL_USER']='ub8frnffaufhoqum'
app.config['MYSQL_PASSWORD']='4QWMy9S2vwBaQgYGI3zu'
app.config['MYSQL_DB']='bfrbtunhryqfh3eywkgx'

mysql=MySQL(app)


#@app.route("") se definen rutas o enlaces en la pagina web es decir interfaces.
@app.route("/")
def Index():
    return render_template('index.html')
@app.route("/login.html")
def login():
    return render_template('login.html')
@app.route("/loginbtn", methods=['POST'])
def loginbtn():
    if request.method == "POST":
        correo=request.form["correo"]
        psw=request.form["contraseña"]
        print(correo,"\n",psw)
    return "recibido"
@app.route("/prueba_db")
def prueba_db():
    cur=mysql.connection.cursor()
    cur.execute("select * from aspirantes")
    print(cur)
    consulta = cur.fetchone()
    print(consulta)
    cur.execute("show tables")
    return "\n\nProbando db"
@app.route("/registro_aspirantes/registro")
def registro_aspirantes():
    return 'registro_aspirantes'
@app.route("/registro_empresa/registro")
def registro_empresa():
    return 'Registro empresa'
@app.route("/aspirante_home/empleos_postulados")
def empleos_postulados():
    return 'Hello World'
@app.route("/aspirante_home/buscar_empleo")
def buscar_empleo():
    return 'Hello World'
@app.route("/aspirante_home/ver_empleos_guardados")
def ver_empleos_guardados():
    return 'Hello World'
@app.route("/empleos/ver_empleo")
def ver_empleo():
    return 'Hello World'
@app.route("/empleos/postular")
def postular():
    return 'Hello World'
@app.route("/empleos/dejar_recomendar")
def dejar_recomendar():
    return 'Hello World'
@app.route("/empleos/guardar_empleo")
def guardar_empleo():
    return 'Hello World'
@app.route("/perfil_empresa/calificar_empresa")
def calificar_empresa():
    return 'Hello World'
@app.route("/configuracion/cambiar_password")
def cambiar_password():
    return 'Hello World'
@app.route("/configuracion/cambiar_email")
def cambiar_email():
    return 'Hello World'
@app.route("/perfil/editar")
def editar():
    return 'Hello World'
@app.route("/perfil/cambiar_foto")
def cambiar_foto():
    return 'Hello World'
@app.route("/empresa_home/publicar_vacante")
def publicar_vacante():
    return 'Hello World'
if __name__=='__main__':
    app.run(port=3000, debug=True)
