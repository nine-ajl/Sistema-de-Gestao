document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-produto');
    const tabela = document.getElementById('tabela-produtos');
    const inputBusca = document.getElementById('input-busca');

    let todosProdutos = [];

    // Carrega a lista de produtos do Back-end
    async function carregarProdutos() {
        try {
            const response = await fetch('/api/produtos');
            const resultado = await response.json();

            if (resultado.sucesso) {
                todosProdutos = resultado.dados;
                renderizarTabela(todosProdutos);
            }
        } catch (erro) {
            console.error('Erro ao buscar dados:', erro);
        }
    }

    // Renderiza a lista na tabela (com tratamento de estado vazio)
    function renderizarTabela(produtos) {
        tabela.innerHTML = '';

        if (produtos.length === 0) {
            tabela.innerHTML = '<tr><td colspan="6" style="text-align:center; color:#666; padding:1.5rem;">Nenhum produto cadastrado.</td></tr>';
            return;
        }

        produtos.forEach(prod => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${prod.id}</td>
                <td><strong>${prod.nome}</strong></td>
                <td>${prod.categoria}</td>
                <td>R$ ${parseFloat(prod.preco).toFixed(2)}</td>
                <td>${prod.quantidade}</td>
                <td>
                    <button class="btn-danger" onclick="deletarProduto(${prod.id})">Excluir</button>
                </td>
            `;
            tabela.appendChild(tr);
        });
    }

    // Submissão do Formulário (Cadastrar)
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const novoProduto = {
            nome: document.getElementById('nome').value,
            categoria: document.getElementById('categoria').value,
            preco: document.getElementById('preco').value,
            quantidade: document.getElementById('quantidade').value
        };

        try {
            const response = await fetch('/api/produtos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(novoProduto)
            });

            const resultado = await response.json();

            if (resultado.sucesso) {
                form.reset(); // Limpa os campos após cadastrar (Ajuste do Laudo)
                carregarProdutos();
            } else {
                alert('Atenção: ' + resultado.mensagem);
            }
        } catch (erro) {
            console.error('Erro ao enviar dados:', erro);
        }
    });

    // Exclusão com confirmação prévia de segurança (Ajuste do Laudo)
    window.deletarProduto = async (id) => {
        if (!confirm('Deseja realmente excluir este registro?')) return;

        try {
            const response = await fetch(`/api/produtos/${id}`, {
                method: 'DELETE'
            });

            const resultado = await response.json();

            if (resultado.sucesso) {
                carregarProdutos();
            } else {
                alert('Erro ao excluir: ' + resultado.mensagem);
            }
        } catch (erro) {
            console.error('Erro ao deletar:', erro);
        }
    };

    // Busca rápida dinamicamente no front-end
    inputBusca.addEventListener('input', (e) => {
        const termo = e.target.value.toLowerCase();
        const filtrados = todosProdutos.filter(prod => 
            prod.nome.toLowerCase().includes(termo) || 
            prod.categoria.toLowerCase().includes(termo)
        );
        renderizarTabela(filtrados);
    });

    // Inicialização
    carregarProdutos();
});