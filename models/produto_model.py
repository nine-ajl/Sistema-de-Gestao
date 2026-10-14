import sqlite3

DATABASE = 'database.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria a tabela no SQLite caso não exista."""
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL CHECK(preco > 0),
                quantidade INTEGER NOT NULL DEFAULT 0 CHECK(quantidade >= 0),
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

class ProdutoModel:
    @staticmethod
    def listar_todos():
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM produtos ORDER BY id DESC')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def criar(nome, categoria, preco, quantidade):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO produtos (nome, categoria, preco, quantidade) VALUES (?, ?, ?, ?)',
                (nome, categoria, preco, quantidade)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def deletar(produto_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
            conn.commit()
            return cursor.rowcount > 0