from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
# Criação de uma secret key
app.config['SECRET_KEY'] = "your_secret_key"
# Criação do caminho de conexão com o bd
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
# Informa a rota que será utilizada no login
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=['POST'])
def login():
    # Recebe as credenciais passadas pelo usuário no corpo da requisição
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Verifica se o usuário e password foram passados
    if username and password:
        # Consulta o usuário no banco de dados
        user = User.query.filter_by(username=username).first()

        # Verifica se o usuário existe e se a password está correta
        if user and user.password == password:
            # Autenticação do usuário
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": f"Usuario: {user.username}, logado"})

    return jsonify({"message": "Credenciais inválidas"}), 400 

@app.route("/logout", methods=['GET'])
@login_required # Proteje a rota só permitindo acesso se o usuário estiver logado
def logout():
    logout_user() # Efetua o logout do usuário
    return jsonify({"message": "Logout efetuado com sucesso!"})

@app.route("/user", methods=['POST'])
@login_required # Rota protegida
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        # Consulta o usuário no banco de dados
        user = User.query.filter_by(username=username).first()
        
        # Se o usuário não existir
        if not user:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "Usuário inserido com sucesso."})
        
        return jsonify({"message": "Usuário já cadastrado."}), 409

    return jsonify({"message": "Usuário não cadastrado."}), 401

@app.route("/user/<int:id_user>", methods=['GET'])
@login_required
def get_user(id_user):
    user = User.query.filter_by(id=id_user).first()

    if user:
        return jsonify({"id": user.id,
                        "username": user.username
                       })
    
    return jsonify({"message": "Usuário não encontrado."}), 404

@app.route("/user/<int:id_user>", methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json
    password = data.get("password")
    if password:
        user = User.query.filter_by(id=id_user).first()

        if user:
            user.password = password
            db.session.commit()
            return jsonify({"message": f"Usuário {user.username} atualizado com sucesso."})
        
        return jsonify({"message": "Usário não econtrado."}), 404
    
    return jsonify({"message": "Preencha o campo password."}), 401

@app.route("/user/<int:id_user>", methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.filter_by(id=id_user).first()
    user_logged = int(current_user.get_id())

    if id_user != user_logged:
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": f"Usuário {user.username} deletado com sucesso."})
        return jsonify({"message": "Usuário não localizado."}), 404
    return jsonify({"message": "Não é possível deletar um usuário logado."}), 401

@app.route("/", methods=['GET'])
def hello_world():

    return "API Flask Auth"

if __name__ == '__main__':
    app.run(debug=True)