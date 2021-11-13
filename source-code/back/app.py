from flask import Flask, render_template, request,redirect, session, flash
from flask_mysqldb import MySQL

#Se crea una aplicacion flask
app= Flask(__name__)

#Se especifica en donde estara la base de datos, por ejemplo localhost
app.config['MYSQL_HOST']='bfrbtunhryqfh3eywkgx-mysql.services.clever-cloud.com'
app.config['MYSQL_USER']='ub8frnffaufhoqum'
app.config['MYSQL_PASSWORD']='4QWMy9S2vwBaQgYGI3zu'
app.config['MYSQL_DB']='bfrbtunhryqfh3eywkgx'

mysql=MySQL(app)

#Es para especificar como va ir protegida nuestra sesion
app.secret_key = b'w\xbdE[p+\xf5\xf8-\xc9\xbc~\x9f\xd1y\x14'

#@app.route("") se definen rutas o enlaces en la pagina web es decir interfaces.
@app.route("/")
def Index():
    return render_template('login.html')
@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/registroAspirantes.html")
def registroAspirantes():
    return render_template('registroAspirantes.html')
@app.route("/asp1", methods=["POST"])
def registroasp1():
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    fechaNacimiento = request.form["fechaNacimiento"]
    gender = request.form["gender"]
    correo = request.form["correo"]
    telefono = request.form["telefono"]
    contraseña = request.form["contraseña"]
    confirmarContraseña = request.form["confirmarContraseña"]
    if contraseña==confirmarContraseña and contraseña:
        cursor=mysql.connection.cursor()
        cursor.execute("""INSERT into aspirantes (ID, Nombre, Apellidos, fechaNacimiento, Genero, Telefono, correoElectronico, Contraseña)
        values (%s,%s,%s,%s,%s,%s,%s,%s);
        """,
        (None, nombre, apellidos, fechaNacimiento, gender, correo, )
        )
        print(sql_registroA)
        cursor.execute(sql_registroA)
        results=cursor.fetchall()
        print(results)
        #aqui debe ir a la siguiente pantalla del registro
        return redirect("/homepage")
    else:
        #<<<<<<<Hay que retornar una alerta de que las contraseñas no coinciden
        flash("Error en la contraseña")
        return redirect("/registroAspirantes.html")

@app.route("/registroEmpresa.html")
def registroEmpresa():
    return render_template('registroEmpresa.html')

@app.route("/registroUsuarios.html")
def registroUsuario():
    return render_template('registroUsuarios.html')

@app.route("/homepage")
def index():
    return render_template('homepage.html')

@app.route("/hacer_login", methods=["POST"])
def hacer_login():
    correo = request.form["correo"]
    contra = request.form["contraseña"]
    #print(correo)
    #print(contra)
    cursor=mysql.connection.cursor()

    sql_empresas = "SELECT * FROM empresa where correoElectronico= '"+correo+"' and Contraseña='"+contra+"'"
    sql_aspirantes= "SELECT * FROM aspirantes where correoElectronico= '"+correo+"' and Contraseña='"+contra+"'"

    try:
        cursor.execute(sql_aspirantes)
        results = cursor.fetchall()
        print(results)
        if len(results)==1:
            session["usuario"] = correo
            #home de aspirante
            return redirect("/homepage")
        else:
            cursor.execute(sql_empresas)
            results = cursor.fetchall()
            print(results)
            if len(results)==1:
                session["usuario"] = correo
                #home de empresa
                return redirect("/homepage")
            else:
                # Si NO coincide, lo regresamos
                print("Esta llegando al else")
                flash("Correo o contraseña incorrectos")
                return redirect("/login.html")
    except:
        print("Esta llegando al except")
        return redirect("/login.html")


# Un "middleware" que se ejecuta antes de responder a cualquier ruta. Aquí verificamos si el usuario ha iniciado sesión
@app.before_request
def antes_de_cada_peticion():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    #if not 'usuario' in session and ruta != "/login.html" and ruta != "/hacer_login" and ruta != "/logout" and not ruta.startswith("/static"):
    #    flash("Inicia sesión para continuar")
    #    return redirect("/login.html")
    # Si ya ha iniciado, no hacemos nada, es decir lo dejamos pasar

# Cerrar sesión
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")



@app.route("/prueba_db")
def prueba_db():
    cur=mysql.connection.cursor()
    cur.execute("select * from aspirantes")
    print(cur)
    consulta = cur.fetchone()
    print(consulta)
    cur.execute("show tables")
    return "\n\nProbando db"

if __name__=='__main__':
    app.run(port=3000, debug=True)
