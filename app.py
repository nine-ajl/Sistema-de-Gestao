from flask import Flask
from models.produto_model import init_db
from controllers.produto_controller import produto_bp

app = Flask(__name__)

# Inicializa a tabela no banco SQLite ao subir a aplicação
init_db()

# Registra as rotas do Controller
app.register_blueprint(produto_bp)

if __name__ == '__main__':
    print("Servidor iniciado em: http://127.0.0.1:5000")
    app.run(debug=True)