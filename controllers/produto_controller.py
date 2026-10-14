from flask import Blueprint, render_template, request, jsonify
from models.produto_model import ProdutoModel

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/')
def index():
    """Renderiza a página principal (View)."""
    return render_template('index.html')

@produto_bp.route('/api/produtos', methods=['GET'])
def get_produtos():
    """Retorna todos os produtos em JSON."""
    produtos = ProdutoModel.listar_todos()
    return jsonify({'sucesso': True, 'dados': produtos}), 200

@produto_bp.route('/api/produtos', methods=['POST'])
def add_produto():
    """Recebe dados via JSON, valida regras de negócio e insere no banco."""
    data = request.get_json()
    
    if not data or not data.get('nome') or not data.get('preco'):
        return jsonify({'sucesso': False, 'mensagem': 'Preencha todos os campos obrigatórios!'}), 400

    try:
        nome = data['nome'].strip()
        categoria = data.get('categoria', 'Geral').strip()
        preco = float(data['preco'])
        quantidade = int(data.get('quantidade', 0))

        # Validação de Segurança / Regra de Negócio (Laudo de Qualidade)
        if preco <= 0 or quantidade < 0:
            return jsonify({'sucesso': False, 'mensagem': 'O preço deve ser maior que zero e a quantidade não pode ser negativa!'}), 400

        novo_id = ProdutoModel.criar(nome, categoria, preco, quantidade)
        return jsonify({'sucesso': True, 'id': novo_id, 'mensagem': 'Produto cadastrado com sucesso!'}), 201

    except ValueError:
        return jsonify({'sucesso': False, 'mensagem': 'Valores numéricos inválidos!'}), 400
    except Exception as e:
        return jsonify({'sucesso': False, 'mensagem': str(e)}), 500

@produto_bp.route('/api/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    """Deleta o produto pelo ID."""
    sucesso = ProdutoModel.deletar(produto_id)
    if sucesso:
        return jsonify({'sucesso': True, 'mensagem': 'Produto excluído com sucesso!'}), 200
    return jsonify({'sucesso': False, 'mensagem': 'Produto não encontrado.'}), 404