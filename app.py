from flask import Flask, render_template, request, redirect, url_for, session
from firebase_config import auth, db

app = Flask(__name__)
app.secret_key = "clave_super_secreta"  # Cambia esto por algo más seguro

@app.route('/')
def index():
    if "user" in session:
        user = session["user"]
        return render_template('index.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session["user"] = email
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            return render_template('login.html', error="Correo o contraseña incorrectos")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
