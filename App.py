from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# instanciando la aplicación tipo Flask
app = Flask(__name__)

# configurando MySQL 
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB']       = 'flaskcontacts'
mysql = MySQL( app )  # passamos la aplicacion como parámetro

# configuramos la session
app.secret_key = 'miclavesecreta'



@app.route('/')             # ruta principal
def Index():
    # consultar en la base de datos
    cursor = mysql.connection.cursor()          # creamos la conexion a la base de datos
    cursor.execute('SELECT * FROM contacts')    # creamos la consulta
    datos = cursor.fetchall()                   # ejecutamos la consulta
    print( datos )

    return render_template( 'index.html', contactos = datos )      # Flask tiene predeterminda la carpeta templates



@app.route('/add_contact', methods = ['POST'])  # ruta para agregar un contacto
def add_contact():
    if request.method == 'POST':                # recuperando datos que vienen del formulario
        fullname = request.form['fullname']
        phone    = request.form['phone']
        email    = request.form['email']
 
        # Manejo de datos en MySQL
        cursor = mysql.connection.cursor()      # creamos la conexion a la base de datos
        cursor.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',     # creamos la consulta 
                       (fullname, phone, email))
        cursor.connection.commit()                  # ejecutamos la consulta
        flash('Contacto adicionado correctamente')  # enviamos un mensaje a la vista

        return redirect( url_for('Index') )     # redireccionamos a la vista ppal mediante la función Index




@app.route('/edit/<id>')         # ruta para editar recibiendo un 'id' como parámetro
def get_contact(id):
    cursor = mysql.connection.cursor()          # crear la conexión a la base de datos
    cursor.execute('SELECT * FROM contacts WHERE id = %s', (id))    # creamos la consulta
    datos = cursor.fetchall()                   # recibimos el resultado de la consulta en la variable 'datos'
    print( datos[0] )
    
    return render_template('edit_contact.html', contacto = datos[0])

@app.route('/update/<id>', methods = ['POST'])       # ruta para actualizar los datos de un contacto recibiendo el 'id'
def update_contact(id):
    if request.method == 'POST':                    # si el método es 'POST' entonces...
        fullname = request.form['fullname']
        phone    = request.form['phone']
        email     = request.form['email']

        cursor = mysql.connection.cursor()      # creamos la conexion
        cursor.execute("""                      
            UPDATE contacts
            SET fullname = %s, email = %s, email = %s
            where id = %s
        """, (fullname, phone, email, id))
        cursor.connection.commit()              # ejecutamos la consulta

        flash('Contacto actualizado satisfactoriamente')
        return redirect( url_for('Index') )


@app.route('/delete/<string:id>')       # ruta para eliminar recibiendo un 'id' como parámetro
def delete_contact( id ):               # recibimos el id como parámetro en la función
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = {0}'.format(id))   # pasamos el 'id' en la posición '{0}'
    cursor.connection.commit()
    
    flash('Se ha eliminado el contacto satisfactoriamente')
    
    return redirect( url_for('Index') )



if __name__ == '__main__':                      # comprobar que el archivo es el principal
    app.run( port = 3000, debug = True )        # puerto, autoriniciar_server



