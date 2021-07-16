from app import app
from flask import render_template


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def index(u_path):
    # return '123'
    return render_template('index.html')