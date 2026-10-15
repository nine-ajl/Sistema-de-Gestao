"""Routes for the inventory dashboard and product REST API."""

import math
from typing import Any, Tuple

from flask import Blueprint, Response, render_template, request

from models.produto_model import ProdutoModel
from utils.api_response import api_response


produto_bp: Blueprint = Blueprint("produto", __name__)


@produto_bp.route("/")
def index() -> str:
    """Render the inventory dashboard.

    Returns:
        The rendered dashboard HTML.
    """
    return render_template("index.html")


@produto_bp.route("/api/produtos", methods=["GET"])
def get_produtos() -> Tuple[Response, int]:
    """Return all products using the standard API response envelope.

    Returns:
        A JSON response containing the product list.
    """
    produtos = ProdutoModel.listar_todos()
    return api_response(
        success=True,
        data=produtos,
        message="Produtos carregados com sucesso.",
    )


@produto_bp.route("/api/produtos", methods=["POST"])
def add_produto() -> Tuple[Response, int]:
    """Validate and create a product from a JSON request.

    Returns:
        A JSON response containing the new product ID or validation error.
    """
    payload: Any = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return api_response(
            success=False,
            data=None,
            message="Envie os dados do produto em formato JSON.",
            status_code=400,
        )

    raw_nome = payload.get("nome")
    raw_categoria = payload.get("categoria", "Geral")
    raw_preco = payload.get("preco")
    raw_quantidade = payload.get("quantidade", 0)

    if not isinstance(raw_nome, str) or not raw_nome.strip():
        return api_response(
            success=False,
            data=None,
            message="Informe o nome do produto.",
            status_code=400,
        )
    if not isinstance(raw_categoria, str):
        return api_response(
            success=False,
            data=None,
            message="A categoria deve ser um texto.",
            status_code=400,
        )
    if isinstance(raw_preco, bool) or not isinstance(raw_preco, (str, int, float)):
        return api_response(
            success=False,
            data=None,
            message="Informe um preço numérico válido.",
            status_code=400,
        )
    if isinstance(raw_quantidade, bool) or not isinstance(
        raw_quantidade, (str, int)
    ):
        return api_response(
            success=False,
            data=None,
            message="Informe uma quantidade inteira válida.",
            status_code=400,
        )

    try:
        preco = float(raw_preco)
        quantidade = int(raw_quantidade)
    except ValueError:
        return api_response(
            success=False,
            data=None,
            message="Preço ou quantidade com formato inválido.",
            status_code=400,
        )

    if (
        not math.isfinite(preco)
        or preco <= 0
        or quantidade < 0
        or quantidade > 9223372036854775807
    ):
        return api_response(
            success=False,
            data=None,
            message="O preço deve ser positivo e a quantidade deve ser um inteiro válido.",
            status_code=400,
        )

    categoria = raw_categoria.strip() or "Geral"
    novo_id = ProdutoModel.criar(
        raw_nome.strip(),
        categoria,
        preco,
        quantidade,
    )
    return api_response(
        success=True,
        data={"id": novo_id},
        message="Produto cadastrado com sucesso.",
        status_code=201,
    )


@produto_bp.route("/api/produtos/<int:produto_id>", methods=["DELETE"])
def delete_produto(produto_id: int) -> Tuple[Response, int]:
    """Delete a product by ID.

    Args:
        produto_id: ID from the product resource URL.

    Returns:
        A JSON response indicating whether the product was deleted.
    """
    sucesso = ProdutoModel.deletar(produto_id)
    if not sucesso:
        return api_response(
            success=False,
            data=None,
            message="Produto não encontrado.",
            status_code=404,
        )
    return api_response(
        success=True,
        data={"id": produto_id},
        message="Produto excluído com sucesso.",
    )
