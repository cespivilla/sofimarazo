import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
# from flask_session.__init__ import Session
from datetime import datetime
from decouple import config
from github import Github, InputGitAuthor
import os
import requests

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_userdata(ip_address):
    try:
        response = requests.get("http://ip-api.com/json/{}".format(ip_address))
        js = response.json()
        country = js['country']
        region = js['regionName']
        latitud = js['lat']
        longitud = js['lon']
        return country, region, latitud, longitud
    except Exception as e:
        return "Unknown", "Unknown","Unknown","Unknown"

# Usando BD de Melba (tabla users)
conn = sqlite3.connect('melba.db')
print ("Opened database successfully*")


@app.route("/")
def index():
    """Show presentacion principal"""
    print ("token index")
    token = os.getenv('GITHUB_TOKEN')
    file_path = "count.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    count = int(data) + 1
    data = str(count)  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating counter.", data, "main", update=True)
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

        mensaje = '\n{}\n{}\n{}\n{}\n{}\n{}\n**'.format(name, apellidos, telefono, correo, comentario, fecha)
        print ("token contacto")
        token = os.getenv('GITHUB_TOKEN')
        file_path = "contactos.txt"
        g = Github(token)
        repo = g.get_repo("cespivilla/sofimarazo")
        file = repo.get_contents(file_path, ref="main")  # Get file from branch
        data = file.decoded_content.decode("utf-8")  # Get raw string data
        data += mensaje  # Modify/Create file

        def push(path, message, content, branch, update=False):
            author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
            source = repo.get_branch("main")
            contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
            repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
        # Add, commit and push branch
        push(file_path, "Updating contacts.", data, "main", update=True)    
        
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
    fecha = datetime.now()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)
    token = os.getenv('GITHUB_TOKEN')
    file_path = "visitas_ai1.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += mensaje  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating visits ai1", data, "main", update=True) 
    
    # permanecer en la pagina para que usuario revise calmadamente
    return render_template("ai1.html")

@app.route('/ai2')
def ai2():
    fecha = datetime.now()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)
    token = os.getenv('GITHUB_TOKEN')
    file_path = "visitas_ai2.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += mensaje  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating visits ai2", data, "main", update=True) 
    
    # permanecer en la pagina para que usuario revise calmadamente
    return render_template("ai2.html")

@app.route('/ai3')
def ai3():
    fecha = datetime.now()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)
    token = os.getenv('GITHUB_TOKEN')
    file_path = "visitas_ai3.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += mensaje  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating visits ai3", data, "main", update=True) 
    
    # permanecer en la pagina para que usuario revise calmadamente
    return render_template("ai3.html")

@app.route('/ai4')
def ai4():
    fecha = datetime.now()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)
    token = os.getenv('GITHUB_TOKEN')
    file_path = "visitas_ai4.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += mensaje  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating visits ai4", data, "main", update=True) 
    
    # permanecer en la pagina para que usuario revise calmadamente
    return render_template("ai4.html")
        
@app.route('/ai5')
def ai5():
    fecha = datetime.now()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)
    token = os.getenv('GITHUB_TOKEN')
    file_path = "visitas_ai5.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += mensaje  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating visits ai5", data, "main", update=True) 
    
    # permanecer en la pagina para que usuario revise calmadamente
    return render_template("ai5.html")      
        
@app.route('/ai6')
def ai6():
        # permanecer en la pagina para que usuario revise calmadamente
        return render_template("ai6.html") 
        
@app.route('/ai7')
def ai7():
    fecha = datetime.now()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)
    token = os.getenv('GITHUB_TOKEN')
    file_path = "visitas_ai7.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += mensaje  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating visits ai7", data, "main", update=True) 
    
    # permanecer en la pagina para que usuario revise calmadamente
    return render_template("ai7.html")        
        
@app.route('/ai8')
def ai8():
        # permanecer en la pagina para que usuario revise calmadamente
        return render_template("ai8.html")        
        
@app.route('/ai9')
def ai9():
    fecha = datetime.now()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)
    token = os.getenv('GITHUB_TOKEN')
    file_path = "visitas_ai9.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += mensaje  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating visits ai9", data, "main", update=True) 
    
    # permanecer en la pagina para que usuario revise calmadamente
    return render_template("ai9.html")
    
@app.route('/ai10')
def ai10():
    fecha = datetime.now()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)
    token = os.getenv('GITHUB_TOKEN')
    file_path = "visitas_ai10.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += mensaje  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating visits ai10", data, "main", update=True) 
    
    # permanecer en la pagina para que usuario revise calmadamente
    return render_template("ai10.html")  

@app.route('/ai11')
def ai11():
    fecha = datetime.now()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)
    token = os.getenv('GITHUB_TOKEN')
    file_path = "visitas_ai11.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += mensaje  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating visits ai11", data, "main", update=True) 
    
    # permanecer en la pagina para que usuario revise calmadamente
    return render_template("ai11.html")  
    
@app.route('/ai12')
def ai12():
    fecha = datetime.now()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)
    token = os.getenv('GITHUB_TOKEN')
    file_path = "visitas_ai12.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += mensaje  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating visits ai12", data, "main", update=True) 
    
    # permanecer en la pagina para que usuario revise calmadamente
    return render_template("ai12.html")  

@app.route('/ai13')
def ai13():
    fecha = datetime.now()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)
    token = os.getenv('GITHUB_TOKEN')
    file_path = "visitas_ai13.txt"
    g = Github(token)
    repo = g.get_repo("cespivilla/sofimarazo")
    file = repo.get_contents(file_path, ref="main")  # Get file from branch
    data = file.decoded_content.decode("utf-8")  # Get raw string data
    data += mensaje  # Modify/Create file

    def push(path, message, content, branch, update=False):
        author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
        source = repo.get_branch("main")
        contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
        repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
    # Add, commit and push branch
    push(file_path, "Updating visits ai13", data, "main", update=True) 
    
    # permanecer en la pagina para que usuario revise calmadamente
    return render_template("ai13.html")  

@app.route('/ai14')
def ai14():
        # permanecer en la pagina para que usuario revise calmadamente
        return render_template("ai14.html")  
