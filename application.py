import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
# from flask_session.__init__ import Session
from datetime import datetime

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Usando BD de Melba (tabla users)
conn = sqlite3.connect('melba.db')
print ("Opened database successfully*")


@app.route("/")
def index():
    """Show presentacion principal"""
    return render_template("index.html")

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    """datos de contacto"""
    # Usando BD de Melba (tabla users)
    conn = sqlite3.connect('melba.db')
    print ("Opened database successfully*")

    # Forget any user_id
    # session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        name = request.form.get("name")
        # Ensure username was submitted
        # if not request.form.get("name"):
            # return apology("Favor indicar nombre", 403)

        apellidos = request.form.get("apellidos")
        # Ensure surnames were submitted
        # elif not request.form.get("apellidos"):
            # return apology("Favor indicar apellidos", 403)

        telefono = request.form.get("telefono")
        correo = request.form.get("correo")
        comentario = request.form.get("comentario")
        print ("name", name, type(name))
        print ("apellidos", apellidos, type(apellidos))
        print ("comentario", comentario, type(comentario))
        
        # Query database for number of users
        cur = conn.cursor()
        nusers = cur.execute("SELECT MAX(id) FROM users")
        n = nusers.fetchone()[0]

        # Remember which user has logged in
        session["user_id"] = n + 1
        print ("session user_id ", session["user_id"])
        fecha = datetime.now()
        cur.execute("INSERT INTO users (name, apellidos, telefono, correo, comentario, fecha) VALUES(?, ?, ?, ?, ?, ?)", (name, apellidos, telefono, correo, comentario, fecha));
        conn.commit()
        conn.close()
        
        # Remain in actual page so user can verifiy the sending of data
        return ("", 204)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("contacto.html")

@app.route('/facebook/<user>')
def facebook(user):
    return redirect("https://www.facebook.com/%s/" % user, code=302)

@app.route('/linkedin/<user>')
def linkedin(user):
    return redirect("https://www.linkedin.com/in/%s/" % user, code=302)

@app.route('/instagram/<user>')
def instagram(user):
    return redirect("http://instagram.com/%s/" % user, code=302)

@app.route('/ai1')
def ai1():
        # permanecer en la pagina para que usuario revise calmadamente
        return render_template("ai1.html")

@app.route('/ai2')
def ai2():
        # permanecer en la pagina para que usuario revise calmadamente
        return render_template("ai2.html")

@app.route('/ai3')
def ai3():
        # permanecer en la pagina para que usuario revise calmadamente
        return render_template("ai3.html")

@app.route('/ai4')
def ai4():
        # permanecer en la pagina para que usuario revise calmadamente
        return render_template("ai4.html")
        
@app.route('/ai5')
def ai5():
        # permanecer en la pagina para que usuario revise calmadamente
        return render_template("ai5.html")      
        
@app.route('/ai6')
def ai6():
        # permanecer en la pagina para que usuario revise calmadamente
        return render_template("ai6.html") 
        
@app.route('/ai7')
def ai7():
        # permanecer en la pagina para que usuario revise calmadamente
        return render_template("ai7.html")        
        
@app.route('/ai8')
def ai8():
        # permanecer en la pagina para que usuario revise calmadamente
        return render_template("ai8.html")        
        