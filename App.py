from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
from flask import send_from_directory



# initializations
app = Flask(__name__)




# Mysql Connection
app.config['MYSQL_HOST'] = 'sql199.main-hosting.eu' 
app.config['MYSQL_USER'] = 'u112798984_ipea239'
app.config['MYSQL_PASSWORD'] = 'Lasken1973!'
app.config['MYSQL_DB'] = 'u112798984_ipea239'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes

@app.route('/alumnos')
def trae_alumnos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos')
    data = cur.fetchall()
    cur.close()
    return render_template('/alumnos.html', alumnos = data)



@app.route('/')
def index():
    # cur = mysql.connection.cursor()
    # cur.execute('SELECT * FROM alumnos')
    # data = cur.fetchall()
    # cur.close()
    return render_template('index.html')

@app.route('/notas')
def notas():
  
    return render_template('cargarnotas.html')

@app.route('/contacto')
def contacto():
  
    return render_template('contacto.html')



@app.route('/add_alumno', methods=['POST'])
def add_alumno():
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        curso = request.form['curso']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO alumnos (dni, Nombre, Apellido , Curso) VALUES (%s,%s,%s,%s)", (dni,nombre,apellido,curso))
        mysql.connection.commit()
        flash('Alumno agregado satisfactoriamente')
        return redirect(url_for('trae_alumnos'))

@app.route('/edit/<string:id>', methods = ['POST', 'GET'])
def get_alumno(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos WHERE id = {0}'.format(id))
    data = cur.fetchall()
    mysql.connection.commit()
    # print(data[0])
    return render_template('edit-alumno.html', alumno = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_alumno(id):
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        curso = request.form['curso']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE alumnos
            SET dni = %s,
                Nombre = %s,
                Apellido = %s,
                Curso=%s
            WHERE id = %s
        """, (dni, nombre, apellido, curso, id))
        flash('Alumno actualizado correctamente')
        mysql.connection.commit()
        return redirect(url_for('trae_alumnos'))

# @app.route('/delete/<int:id>', methods = ['POST','GET'])
# def delete_alumno(id):
#     cur = mysql.connection.cursor()
#     cur.execute('DELETE FROM alumnos WHERE id = %s', (id))
#     mysql.connection.commit()
#     flash('Alumno eliminado satisfactoriamente')
#     return redirect(url_for('trae_alumnos'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_alumno(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM alumnos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Alumno borrado correctamente')
    return redirect(url_for('trae_alumnos'))

# starting the app
if __name__ == "__main__":
    app.run(port=5000, debug=False)
