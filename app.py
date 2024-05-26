from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'usuarios'

# Inicialización de la extensión MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    if 'user_name' in session:
        return redirect(url_for('gestioninventario'))
    else:
        return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Manejar la solicitud GET, por ejemplo, mostrar el formulario de inicio de sesión
        return render_template('login.html')
    elif request.method == 'POST':
        # Manejar la solicitud POST para procesar el inicio de sesión
        email = request.form['email']
        password = request.form['password']

        try:
            # Abrir un cursor para interactuar con la base de datos
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Ejecutar una consulta SQL para verificar las credenciales
            query = "SELECT * FROM user WHERE Email = %s AND Password = %s"
            cur.execute(query, (email, password))
            user = cur.fetchone()

            if user:
                # Login exitoso
                if user['Password'] == password:
                    session['user_name'] = user['User_name']
                    return redirect(url_for('gestioninventario'))
                else:
                    flash('contraseña incorrecta.', 'error')
                    return redirect(url_for('login'))
            else:
                flash('Email incorrecto', 'error')
                return redirect(url_for('login'))
            
        except Exception as e:
            import traceback
            return traceback.format_exc()


@app.route('/gestioninventario')
def gestioninventario():
    if 'user_name' in session:
        user_name = session['user_name']
        return render_template('gestioninventario.html', user_name=user_name)
    else:
        return redirect(url_for('home'))
        
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_name', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
