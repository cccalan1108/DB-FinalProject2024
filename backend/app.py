from flask import Flask, render_template, session, redirect
from DB import init_db_conn

# Global Flask app (SUBJECT TO CHANGE) static_folder="../frontend/assets"
app = Flask(__name__, template_folder="../frontend/html")


