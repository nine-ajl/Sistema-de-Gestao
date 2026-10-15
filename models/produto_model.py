"""Persistence layer for inventory products."""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, List, Optional, TypedDict


DATABASE: str = os.getenv("DATABASE_PATH", "database.db")


class Produto(TypedDict):
    """Represent a product row returned by the inventory database."""

    id: int
    nome: str
    categoria: str
    preco: float
    quantidade: int
    data_criacao: Optional[str]


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Yield a SQLite connection configured to return named columns.

    Yields:
        A managed SQLite connection using ``sqlite3.Row`` records.
    """
    database_path = Path(DATABASE)
    if database_path.parent != Path("."):
        database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(database_path))
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def init_db() -> None:
    """Create the products table when it does not already exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL CHECK(preco > 0),
                quantidade INTEGER NOT NULL DEFAULT 0 CHECK(quantidade >= 0),
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()


class ProdutoModel:
    """Provide database operations for inventory products."""

    @staticmethod
    def listar_todos() -> List[Produto]:
        """Return every product, newest first.

        Returns:
            Product records in descending ID order.
        """
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM produtos ORDER BY id DESC"
            ).fetchall()
            return [
                {
                    "id": int(row["id"]),
                    "nome": str(row["nome"]),
                    "categoria": str(row["categoria"]),
                    "preco": float(row["preco"]),
                    "quantidade": int(row["quantidade"]),
                    "data_criacao": (
                        str(row["data_criacao"])
                        if row["data_criacao"] is not None
                        else None
                    ),
                }
                for row in rows
            ]

    @staticmethod
    def criar(
        nome: str, categoria: str, preco: float, quantidade: int
    ) -> Optional[int]:
        """Insert a product into the inventory.

        Args:
            nome: Product name.
            categoria: Product category.
            preco: Unit price, which must be positive.
            quantidade: Initial stock quantity, which cannot be negative.

        Returns:
            The generated product ID, if SQLite provides one.
        """
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO produtos (nome, categoria, preco, quantidade)
                VALUES (?, ?, ?, ?)
                """,
                (nome, categoria, preco, quantidade),
            )
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def deletar(produto_id: int) -> bool:
        """Delete a product by its identifier.

        Args:
            produto_id: ID of the product to delete.

        Returns:
            ``True`` when a row was deleted, otherwise ``False``.
        """
        with get_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM produtos WHERE id = ?", (produto_id,)
            )
            connection.commit()
            return cursor.rowcount > 0
