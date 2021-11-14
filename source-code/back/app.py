from flask import Flask, render_template, request,redirect, session, flash
from flask.helpers import url_for
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
        (None, nombre, apellidos, fechaNacimiento, gender,  telefono, correo, contraseña)
        )
        mysql.commit()
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

@app.route("/formularioEmpresa.html")
def formularioEmpresa():
    return render_template('formularioEmpresa.html')

@app.route("/formularioAspirantes.html")
def formularioAspirantes():
    return render_template('formularioAspirantes.html')

@app.route("/homepage")
<<<<<<< HEAD

@app.route("/homepage/<int:id>")
def index(id = 1):
=======
@app.route("/homepage/<int:page>")
@app.route("/homepage/<int:page>/<int:id_trabajo>")
def index(page = 1, id_trabajo = None):
>>>>>>> 62520681548b22350ccf9e99988cff1ef33366db
    #data usu
    cur = mysql.connection.cursor()
    cur.execute("SELECT Nombre, Apellidos FROM aspirantes WHERE id ={0}".format(session["usuario"]))
    data_usu = cur.fetchall()
    #data empleos
    sql = "SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil, job.ID  FROM empleos job, empresa c WHERE job.idEmpresa = c.ID LIMIT {0}, 10".format( str(10*(page-1)))
    cur.execute(sql)
    data = cur.fetchall()
<<<<<<< HEAD

    return render_template('homepage.html', info_usu = data_usu[0], empleos = data )
=======
    #mensaje si no hay resultados
    if len(data) == 0:
        flash("No hay resultados")
    #path
    path = "homepage/"+str(page)+"/"
    #Empleo seleccionado
    if id_trabajo:
        sql = "SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil,job.Descripcion  FROM empleos job, empresa c WHERE job.idEmpresa = c.ID AND job.ID = {0}".format(id_trabajo)
        print(sql)
        cur.execute(sql)
        data_trabajo = cur.fetchall()
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,path = path, page = page, empleo_seleccionado= data_trabajo[0] )
    else:
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,path = path,page = page)
>>>>>>> 62520681548b22350ccf9e99988cff1ef33366db

@app.route("/homepage/guardados/")
@app.route("/homepage/guardados/<int:page>")
@app.route("/homepage/guardados/<int:page>/<int:id_trabajo>")
def guardados(page = 1,id_trabajo = None):
    #data usu
    cur = mysql.connection.cursor()
    cur.execute("SELECT Nombre, Apellidos FROM aspirantes WHERE id ={0}".format(session["usuario"]))
    data_usu = cur.fetchall()
    #data empleos guardados
    sql = """
<<<<<<< HEAD
    SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil
=======
    SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil, job.ID 
>>>>>>> 62520681548b22350ccf9e99988cff1ef33366db
    FROM empleos job, empresa c, aspirantes_empleos ae, aspirantes a
    WHERE job.idEmpresa = c.ID
    AND job.ID = ae.idEmpleos
    AND a.ID = ae.idAspirante
    AND ae.Estado = 1
    LIMIT {0}, 10""".format( str(10*(page-1)))
    #print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    if len(data) == 0:
        flash("No hay resultados")
    
    #path
    path = "homepage/guardados/"+str(page)+"/"

    #Empleo seleccionado
    if id_trabajo:
        sql = "SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil,job.Descripcion  FROM empleos job, empresa c WHERE job.idEmpresa = c.ID AND job.ID = {0}".format(id_trabajo)
        print(sql)
        cur.execute(sql)
        data_trabajo = cur.fetchall()
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,path = path, page = page, empleo_seleccionado= data_trabajo[0] )
    else:
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,path = path,page = page)

@app.route("/homepage/postulados/")
@app.route("/homepage/postulados/<int:page>")
@app.route("/homepage/postulados/<int:page>/<int:id_trabajo>")
def postulados(page = 1, id_trabajo = None):
    #data usu
    cur = mysql.connection.cursor()
    cur.execute("SELECT Nombre, Apellidos FROM aspirantes WHERE id ={0}".format(session["usuario"]))
    data_usu = cur.fetchall()
    #data empleos guardados
    sql = """
<<<<<<< HEAD
    SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil
=======
    SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil, job.ID
>>>>>>> 62520681548b22350ccf9e99988cff1ef33366db
    FROM empleos job, empresa c, aspirantes_empleos ae, aspirantes a
    WHERE job.idEmpresa = c.ID
    AND job.ID = ae.idEmpleos
    AND a.ID = ae.idAspirante
    AND ae.Estado = 2
    LIMIT {0}, 10""".format( str(10*(page-1)))
    #print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    if len(data) == 0:
        flash("No hay resultados")

    #path
    path = "homepage/postulados/"+str(page)+"/"
    
    #Empleo seleccionado
    if id_trabajo:
        sql = "SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil,job.Descripcion  FROM empleos job, empresa c WHERE job.idEmpresa = c.ID AND job.ID = {0}".format(id_trabajo)
        print(sql)
        cur.execute(sql)
        data_trabajo = cur.fetchall()
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,path = path, page = page, empleo_seleccionado= data_trabajo[0] )
    else:
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,path = path,page = page)

@app.route("/homepage/search", methods=['GET', 'POST'])
def busqueda():
    #data usu
    cur = mysql.connection.cursor()
    cur.execute("SELECT Nombre, Apellidos FROM aspirantes WHERE id ={0}".format(session["usuario"]))
<<<<<<< HEAD
    data_usu = cur.fetchall()
    #

    return render_template('homepage.html', info_usu = data_usu[0])
=======
    data_usu = cur.fetchall()   
    #Tomar el valor del cuadro de busqueda
    search = request.values.get("busqueda")
    try:
        page = request.values.get("page")
        page = int(page)
    except:
        page = 1    
    id = request.values.get("id")
    #print(search)
    #print("page",page)
    #print("id", id)
    #buqueda
    sql = """
    SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil, job.ID 
    FROM empleos job, empresa c
    WHERE job.idEmpresa = c.ID
    AND job.Titulo like '%""" +search+"""%'
    LIMIT {0}, 10""".format( str(10*(page-1)))
    cur.execute(sql)
    data = cur.fetchall()
    if len(data) == 0:
        flash("No hay resultados")
    
    #path
    path = "homepage/search?busqueda="+search+"&page="+str(page)+"&id="
>>>>>>> 62520681548b22350ccf9e99988cff1ef33366db

    #empleo seleccionado
    if(id):
        print(id)
        sql = "SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil,job.Descripcion  FROM empleos job, empresa c WHERE job.idEmpresa = c.ID AND job.ID = {0}".format(id)
        print(sql)
        cur.execute(sql)
        data_trabajo = cur.fetchall()
        data_trabajo = data_trabajo[0]
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,page = id, termino =  search, path = path, empleo_seleccionado = data_trabajo)
    else:
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,page = id, termino =  search, path = path)


@app.route("/hacer_login", methods=["POST"])
def hacer_login():
    correo = request.form["correo"]
    contra = request.form["contraseña"]
    #print(correo)
    #print(contra)
    cursor=mysql.connection.cursor()

    sql_empresas = "SELECT ID FROM empresa where correoElectronico= '"+correo+"' and Contraseña='"+contra+"'"
    sql_aspirantes= "SELECT ID FROM aspirantes where correoElectronico= '"+correo+"' and Contraseña='"+contra+"'"

    try:
        cursor.execute(sql_aspirantes)
        results = cursor.fetchall()
        #print(results)
        if len(results)==1:
            session["usuario"] = results[0][0]
            #home de aspirante
            return redirect("/homepage")
        else:
            cursor.execute(sql_empresas)
            results = cursor.fetchall()
            #print(results)
            if len(results)==1:
                session["usuario"] = results[0][0]
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
    print("pan")
    return redirect("/login.html")


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
