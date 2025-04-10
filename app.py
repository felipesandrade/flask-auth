from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Criação de uma secret key
app.config['SECRET_KEY'] = "your_secret_key"
# Criação do caminho de conexão com o bd
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
# Criação da conexão com o bd
db = SQLAlchemy(app)



@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)