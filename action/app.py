from flask import Flask, render_template, session, redirect
from DB_utils import db_connect

from login import login


# Global Flask app (SUBJECT TO CHANGE) static_folder="../frontend/assets"
app = Flask(__name__, template_folder="../frontend/html")

app.register_blueprint(login)

def init_app():
    db_connect()
    
@app.route('/')
def index():
    if session.get("login"):
        return redirect("/category")
    else:
        return redirect("/login") 

if __name__ == '__main__':
    init_app()
    app.run()
