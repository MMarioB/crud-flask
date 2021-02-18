from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Iniciar un servidor
app = Flask(__name__)

if __name__ == "__main__":
    app.run(port=5000,debug=True)

# settings de sesion
app.secret_key='mysecretkey'

# CONEXION
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudanimes'
mysql = MySQL(app)

# Ruta inicial
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM animes')
    datos = cur.fetchall()
    return render_template('index.html', animes=datos)

# ALTA
@app.route('/alta_anime', methods=['POST'])
def altaAnime():
    if request.method == 'POST':
        nombre = request.form['nombre']
        estudio = request.form['estudio']
        episodios = request.form['episodios']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO animes (nombre,estudio,episodios) ' 'VALUES (%s, %s, %s)',(nombre,estudio,episodios))
        mysql.connection.commit()
        flash('Añadido correctamente')
    return redirect(url_for('index'))

# ACTUALIZAR
@app.route('/edit_anime/<id>', methods = ['POST', 'GET'])
def editarAnime(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM animes WHERE id LIKE %s', [id])
    datos = cur.fetchall()
    print(datos[0])
    cur.close()
    return render_template('edit.html', anime=datos[0])
@app.route('/actualizar/<id>', methods=['POST'])
def actualizaranime(id):
    if (request.method == 'POST'):
        nombre = request.form['nombre']
        estudio = request.form['estudio']
        episodios = request.form['episodios']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE animes
            SET nombre=%s, estudio=%s, episodios=%s
            WHERE id=%s
        
        """, (nombre, estudio, episodios, id))
        mysql.connection.commit()
        flash('Anime Actualizado!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return redirect(url_for('index'))

# BORRAR
@app.route('/baja_anime/<string:id>')
def bajaAnime(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM animes WHERE id={0}'.format(id))
    mysql.connection.commit()
    
    flash('Anime eliminado')
    return redirect(url_for('index'))