# Automate-Phishing-Academic

## Project: Cloned Site & Integrated Keylogger

This project is a Python/Flask web application designed to clone the HTML, CSS, JavaScript, and images of a target website and inject data capture functionalities, specifically a keylogger and a login form phishing mechanism.

The application acts as a social engineering tool (for educational and security testing purposes only) by presenting the user with an exact copy of the desired webpage, while capturing both keystrokes and submitted login credentials.


## Key Features

-Website Cloning: Uses requests and BeautifulSoup to download the main HTML file, along with associated CSS, JavaScript, and image resources, storing them locally in the cloned_site directory.

-Malicious Code Injection: Dynamically modifies the cloned HTML code to:

-Form Phishing: Rewrite the action attribute of all forms to point to the Flask application's /login endpoint, enabling the capture of usernames and passwords.

-Client-Side Keylogger (JavaScript): Inject a small JavaScript snippet that listens for the keydown event and sends each keystroke to the Flask application's /log_keystroke endpoint via a fetch (POST) request.

-Server-Side Keylogger (Python): A native keylogger using pynput runs in a separate thread. It listens for keystrokes on the host machine and logs them to the log.txt file.

-Data Persistence: Captured login credentials (username, password) from the phishing form are stored in a SQLite database (credentials.db) using SQLAlchemy and Pandas.

-Redirection: After form submission, the user is redirected to an error page (/error.html) or potentially back to the original site.

-File Monitoring (watchdog): A mechanism to monitor changes to the main script and automatically restart it.

### Project Structure

-projet_2.py: The main file containing the Flask application, cloning logic, keylogging functions, and database management.

-cloned_site/: The directory where the HTML, CSS, JS, and image assets of the target site are stored.

-credentials.db: The SQLite database containing the captured credentials.

-log.txt: The text file where keystrokes are logged by the Python keylogger.

-templates/: Contains HTML templates like index.html and error.html.

Dependencies
Bash

### pip install Flask requests beautifulsoup4 sqlalchemy pandas pynput watchdog

