from flask import Flask, render_template, request,redirect, session, flash
from flask.helpers import url_for
from flask_mysqldb import MySQL
#regular expression 
import re
#recommender system
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
        cursor.execute("SELECT ID from aspirantes WHERE Telefono="+telefono)
        id=cursor.fetchall()
        url_id="/asp2/"+str(id[0][0])
        mysql.connection.commit()
        #aqui debe ir a la siguiente pantalla del registro
    else:
        #<<<<<<<Hay que retornar una alerta de que las contraseñas no coinciden
        flash("Error en la contraseña")
        return redirect("/registroAspirantes.html")
#
@app.route("/asp2/<id>", methods=['GET'])
def registroasp2(id):
    print(id)
    print("Hola..............")
    return render_template("/formularioAspirantes.html")

@app.route("/registroEmpresa.html")
def registroEmpresa():
    return render_template('registroEmpresa.html')
@app.route("/formulario_empresa")
def formulario_empresa():
    nombre = request.form["nombre"]
    correo = request.form["correo"]
    contraseña = request.form["contraseña"]
    confirmarContraseña = request.form["confirmarContraseña"]
    if contraseña==confirmarContraseña and contraseña:
        cursor=mysql.connection.cursor()
        cursor.execute("""INSERT into empresa (ID, Nombre, correoElectronico, Contraseña)
        values (%s,%s,%s,%s,%s,%s,%s,%s);
        """,
        (None, nombre, correo, contraseña)
        )
    return render_template("formularioEmpresa.html")
@app.route("/homepage")
@app.route("/homepage/<int:page>")
@app.route("/homepage/<int:page>/<int:id_trabajo>")
def index(page = 1, id_trabajo = None):
    #data usu
    cur = mysql.connection.cursor()
    cur.execute("SELECT Nombre, Apellidos FROM aspirantes WHERE id ={0}".format(session["usuario"]))
    data_usu = cur.fetchall()
    #data empleos
    sql = """SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil, job.ID  
    FROM empleos job, empresa c 
    WHERE job.idEmpresa = c.ID 
    LIMIT {0}, 10""".format( str(10*(page-1)))
    cur.execute(sql)
    data = cur.fetchall()
    #mensaje si no hay resultados
    if len(data) == 0:
        flash("No hay resultados")
    #path
    path = "homepage/"+str(page)+"/"
    #Empleo seleccionado
    if id_trabajo:
        sql = """
        SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil,job.Descripcion, job.ID
        FROM empleos job, empresa c 
        WHERE job.idEmpresa = c.ID 
        AND job.ID = {0}""".format(id_trabajo)
        print(sql)
        cur.execute(sql)
        data_trabajo = cur.fetchall()
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,path = path, page = page, empleo_seleccionado= data_trabajo[0] )
    else:
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,path = path,page = page)

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
    SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil, job.ID
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
        sql = """
        SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil,job.Descripcion, job.ID
        FROM empleos job, empresa c 
        WHERE job.idEmpresa = c.ID 
        AND job.ID = {0}""".format(id_trabajo)
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
    SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil, job.ID
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
        sql = """
        SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil,job.Descripcion, job.ID
        FROM empleos job, empresa c 
        WHERE job.idEmpresa = c.ID 
        AND job.ID = {0}""".format(id_trabajo)
        
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

    #empleo seleccionado
    if(id):
        print(id)
        sql = """
        SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil,job.Descripcion, job.ID
        FROM empleos job, empresa c 
        WHERE job.idEmpresa = c.ID 
        AND job.ID = {0}""".format(id)
        print(sql)
        cur.execute(sql)
        data_trabajo = cur.fetchall()
        data_trabajo = data_trabajo[0]
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,page = page, termino =  search, path = path, empleo_seleccionado = data_trabajo)
    else:
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,page = page, termino =  search, path = path)


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
            session["recomendaciones"] = generar_recomendaciones(session["usuario"])
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

"""
Estado en aspirantes_empleos
1 - Guardados
2 - Postulados
3 - No me interesa
"""

@app.route("/<path:path>/Guardar/<int:numero>")
def guardar(path, numero):
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT * FROM aspirantes_empleos 
    WHERE idAspirante ={0}
    AND idEmpleos = {1}""".format(session["usuario"], numero))
    row_empleo = cur.fetchall()   
    #Si no hay ningun registro, hago un insert  
    if len(row_empleo) == 0:
        cur.execute("""
        insert into aspirantes_empleos (idAspirante, idEmpleos, Estado )
        values (%s,%s,%s)
        """,
        ( session["usuario"],numero, 1))
        mysql.connection.commit()
        print("Se ha insertado un registro")
    else:
        #Si ya habia un registro, entonces se hace un update
        cur.execute("""
        UPDATE aspirantes_empleos 
        SET Estado = 1
        WHERE idAspirante ={0}
        AND idEmpleos = {1}""".format(session["usuario"], numero)),
        mysql.connection.commit()
        print("Se ha actualizado un registro")       
    #obtengo el path, y lo redirecciono al path sin el /Guardar/<numero>
    path = request.path
    path = re.sub("\\/Guardar\\/\d\d?\d?\d?","",path)
    print(path)
    return redirect(path)

@app.route("/<path:path>/Postular/<int:numero>")
def Postular(path, numero):
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT * FROM aspirantes_empleos 
    WHERE idAspirante ={0}
    AND idEmpleos = {1}""".format(session["usuario"], numero))
    row_empleo = cur.fetchall()   
    #Si no hay ningun registro, hago un insert  
    if len(row_empleo) == 0:
        cur.execute("""
        insert into aspirantes_empleos (idAspirante, idEmpleos, Estado )
        values (%s,%s,%s)
        """,
        ( session["usuario"],numero, 2))
        mysql.connection.commit()
        print("Se ha insertado un registro")
    else:
        #Si ya habia un registro, entonces se hace un update
        cur.execute("""
        UPDATE aspirantes_empleos 
        SET Estado = 2
        WHERE idAspirante ={0}
        AND idEmpleos = {1}""".format(session["usuario"], numero)),
        mysql.connection.commit()
        print("Se ha actualizado un registro")       
    #obtengo el path, y lo redirecciono al path sin el /Guardar/<numero>
    path = request.path
    path = re.sub("\\/Postular\\/\d\d?\d?\d?","",path)
    print(path)
    return redirect(path)

@app.route("/<path:path>/NoMeInteresa/<int:numero>")
def NoMeInteresa(path, numero):
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT * FROM aspirantes_empleos 
    WHERE idAspirante ={0}
    AND idEmpleos = {1}""".format(session["usuario"], numero))
    row_empleo = cur.fetchall()   
    #Si no hay ningun registro, hago un insert  
    if len(row_empleo) == 0:
        cur.execute("""
        insert into aspirantes_empleos (idAspirante, idEmpleos, Estado )
        values (%s,%s,%s)
        """,
        ( session["usuario"],numero, 3))
        mysql.connection.commit()
        print("Se ha insertado un registro")
    else:
        #Si ya habia un registro, entonces se hace un update
        cur.execute("""
        UPDATE aspirantes_empleos 
        SET Estado = 3
        WHERE idAspirante ={0}
        AND idEmpleos = {1}""".format(session["usuario"], numero)),
        mysql.connection.commit()
        print("Se ha actualizado un registro")       
    #obtengo el path, y lo redirecciono al path sin el /Guardar/<numero>
    path = request.path
    path = re.sub("\\/NoMeInteresa\\/\d\d?\d?\d?","",path)
    print(path)
    return redirect(path)


def clean_data(x):
  if isinstance(x, str):
      return str.lower(x.replace(" ", "").replace(",", " "))
  else:
      return ''

def create_soup(df):
  return "".join(df[2]) + ' ' + "".join(df[3]) + ' ' + "".join(df[4])

def generar_recomendaciones(id):
    cursor = mysql.connection.cursor()
    #Dataframe de todos los empleos
    cursor.execute("SELECT ID, Titulo, hardSkills,Idiomas,Escolaridad   FROM empleos")
    data_empleos = pd.DataFrame(cursor.fetchall())
    #metadata de los empleos
    for i in range (2,4+1):
        data_empleos[i] = data_empleos[i].apply(clean_data)
    data_empleos["soup"] = data_empleos.apply(create_soup, axis=1)

    #Datos del usuario aspirante
    cursor.execute("SELECT ID, Nombre, hardSkills,Idiomas,Escolaridad FROM aspirantes WHERE id ={0}".format(id))#session["usuario"]
    data_usuario = pd.DataFrame(cursor.fetchall())
    data_usuario[1] = "skill_usuario_objetivo"
    print(data_usuario)
    #escolaridad, estandarizar a terminos que tienen los empleos
    escolaridad = data_usuario.loc[0][4]
    if(escolaridad == "Licenciatura terminada" or escolaridad == "Maestría trunca o en curso"):
        data_usuario[4] = "Licenciatura, Bachelor"
    elif(escolaridad == "Maestría terminada" or escolaridad == "Doctorado trunco o en curso"):
        data_usuario[4] = "Maestria, Master"
    elif(escolaridad == "Doctorado terminado"):
        data_usuario[4] = "Doctorado, PhD"
    else:
        data_usuario[4]  = ""
    #metadata del aspirante
    for i in range (2,4+1):
        data_usuario[i] = data_usuario[i].apply(clean_data)
    data_usuario["soup"] = data_usuario.apply(create_soup, axis=1)
    print("metadata del usu", data_usuario["soup"])
    #df para hacer calculos
    df_rs = pd.concat([data_empleos, data_usuario], axis=0)
    #print(df_rs)
    indices = pd.Series(df_rs.index, index=df_rs[1])
    #print(indices)
    idx = indices["skill_usuario_objetivo"]
    count = CountVectorizer(stop_words=('english', "spanish"))
    count_matrix = count.fit_transform(df_rs['soup'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    #Ordenar resultados 
    sim_scores = list(enumerate(cosine_sim2[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #50 empleos a recomendar
    sim_scores = sim_scores[1:51]
    #ID de los empleos a recomendar
    jobs_indices = tuple([i[0] for i in sim_scores])

    return jobs_indices

@app.route("/homepage/recomendaciones/")
@app.route("/homepage/recomendaciones/<int:page>")
@app.route("/homepage/recomendaciones/<int:page>/<int:id_trabajo>")
def recomendaciones(page = 1, id_trabajo = None):
    #data usu
    cur = mysql.connection.cursor()
    cur.execute("SELECT Nombre, Apellidos FROM aspirantes WHERE id ={0}".format(session["usuario"]))
    data_usu = cur.fetchall()
    #recomendaciones
    print(session["recomendaciones"])
    cursor = mysql.connection.cursor()
    sql = """
        SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil, job.ID  
        FROM empleos job, empresa c 
        WHERE job.idEmpresa = c.ID  AND 
        job.ID IN {1}  LIMIT {0}, 10""".format( str(10*(page-1)), str(session["recomendaciones"]))
    print("consulta", sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    #print(data)  
    if len(data) == 0:
            flash("No hay resultados")

    #path
    path = "homepage/recomendaciones/"+str(page)+"/"
    
    #Empleo seleccionado
    if id_trabajo:
        sql = """
        SELECT job.Titulo, job.Ubicacion,c.Nombre, c.fotoPerfil,job.Descripcion, job.ID
        FROM empleos job, empresa c 
        WHERE job.idEmpresa = c.ID 
        AND job.ID = {0}""".format(id_trabajo)
        
        cur.execute(sql)
        data_trabajo = cur.fetchall()
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,path = path, page = page, empleo_seleccionado= data_trabajo[0] )
    else:
        return render_template('homepage.html', info_usu = data_usu[0], empleos = data,path = path,page = page)


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

if __name__=='__main__':
    app.run(port=3000, debug=True)
