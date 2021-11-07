from flask import Flask
from flask_mysqldb import MySQL

#Se crea una aplicacion flask
app= Flask(__name__)

#Se especifica en donde estara la base de datos, por ejemplo localhost
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='1234'
app.config['MYSQL_DB']=''

mysql=MySQL(app)


#@app.route("") se definen rutas o enlaces en la pagina web es decir interfaces.
@app.route("/")
def Index():
    return 'Hello World'
@app.route("/prueba_db")
def prueba_db():
    #cur=mysql.connection.cursor()
    #cur.execute("select * from table Aspirantes")
    return "Probando db"


if __name__=='__main__':
    app.run(port=3000, debug=True)
