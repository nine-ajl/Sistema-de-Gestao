const productForm = document.querySelector("#form-produto");
const productDialog = document.querySelector("#modal-produto");
const deleteDialog = document.querySelector("#modal-confirmar-exclusao");
const productTable = document.querySelector("#tabela-produtos");
const searchInput = document.querySelector("#input-busca");
const saveButton = document.querySelector("#salvar-produto");
const confirmDeleteButton = document.querySelector("#confirmar-exclusao");

const requiredElements = [
    productForm,
    productDialog,
    deleteDialog,
    productTable,
    searchInput,
    saveButton,
    confirmDeleteButton
];

if (requiredElements.some((element) => element === null)) {
    throw new Error("Não foi possível inicializar os controles do painel.");
}

const metrics = {
    totalItems: document.querySelector("#metrica-total-itens"),
    stockValue: document.querySelector("#metrica-valor-estoque"),
    outOfStock: document.querySelector("#metrica-sem-estoque"),
    productCount: document.querySelector("#contador-produtos")
};

if (Object.values(metrics).some((element) => element === null)) {
    throw new Error("Não foi possível inicializar as métricas do painel.");
}

const currencyFormatter = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL"
});

let products = [];
let pendingDeleteId = null;

function showToast(message, isError = false) {
    if (typeof Toastify !== "function") {
        window.alert(message);
        return;
    }

    Toastify({
        text: message,
        duration: 3200,
        gravity: "top",
        position: "right",
        close: true,
        stopOnFocus: true,
        style: {
            background: isError ? "#be123c" : "#0f766e",
            borderRadius: "10px",
            boxShadow: "0 12px 24px rgba(15, 23, 42, .18)"
        }
    }).showToast();
}

async function requestApi(url, options = {}) {
    const response = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...options
    });
    const result = await response.json();

    if (!response.ok || !result.success) {
        throw new Error(result.message || "Não foi possível concluir a solicitação.");
    }

    return result;
}

function createCell(value, className = "px-6 py-4 text-slate-600") {
    const cell = document.createElement("td");
    cell.className = className;
    cell.textContent = value;
    return cell;
}

function getStockStatus(quantity) {
    if (quantity <= 0) {
        return { label: "Sem estoque", styles: "bg-rose-50 text-rose-700 ring-rose-600/20" };
    }
    if (quantity <= 5) {
        return { label: "Estoque baixo", styles: "bg-amber-50 text-amber-700 ring-amber-600/20" };
    }
    return { label: "Disponível", styles: "bg-emerald-50 text-emerald-700 ring-emerald-600/20" };
}

function updateMetrics(items) {
    const totalUnits = items.reduce((total, product) => total + Number(product.quantidade), 0);
    const stockValue = items.reduce(
        (total, product) => total + Number(product.preco) * Number(product.quantidade),
        0
    );
    const outOfStock = items.filter((product) => Number(product.quantidade) === 0).length;

    metrics.totalItems.textContent = new Intl.NumberFormat("pt-BR").format(totalUnits);
    metrics.stockValue.textContent = currencyFormatter.format(stockValue);
    metrics.outOfStock.textContent = new Intl.NumberFormat("pt-BR").format(outOfStock);
    metrics.productCount.textContent = `${items.length} ${items.length === 1 ? "produto" : "produtos"}`;
}

function renderProducts(items) {
    productTable.replaceChildren();

    if (items.length === 0) {
        const row = document.createElement("tr");
        const cell = createCell(
            products.length === 0
                ? "Nenhum produto cadastrado. Adicione seu primeiro item para começar."
                : "Nenhum produto encontrado para esta busca.",
            "px-6 py-12 text-center text-sm text-slate-500"
        );
        cell.colSpan = 6;
        row.append(cell);
        productTable.append(row);
        return;
    }

    items.forEach((product) => {
        const row = document.createElement("tr");
        row.className = "transition hover:bg-slate-50/80";

        const nameCell = document.createElement("td");
        nameCell.className = "px-6 py-4";
        const name = document.createElement("p");
        name.className = "font-medium text-slate-900";
        name.textContent = product.nome;
        const id = document.createElement("p");
        id.className = "mt-1 text-xs text-slate-400";
        id.textContent = `ID #${product.id}`;
        nameCell.append(name, id);

        const status = getStockStatus(Number(product.quantidade));
        const statusCell = document.createElement("td");
        statusCell.className = "px-6 py-4";
        const badge = document.createElement("span");
        badge.className = `inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset ${status.styles}`;
        badge.textContent = status.label;
        statusCell.append(badge);

        const actionCell = document.createElement("td");
        actionCell.className = "px-6 py-4 text-right";
        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.dataset.productId = String(product.id);
        deleteButton.setAttribute("aria-label", `Excluir ${product.nome}`);
        deleteButton.className = "inline-flex items-center justify-center rounded-lg p-2 text-slate-400 transition hover:bg-rose-50 hover:text-rose-600 focus:outline-none focus:ring-4 focus:ring-rose-50";
        deleteButton.innerHTML = '<i data-lucide="trash-2" class="h-4 w-4"></i>';
        actionCell.append(deleteButton);

        row.append(
            nameCell,
            createCell(product.categoria),
            createCell(currencyFormatter.format(Number(product.preco))),
            createCell(new Intl.NumberFormat("pt-BR").format(Number(product.quantidade))),
            statusCell,
            actionCell
        );
        productTable.append(row);
    });

    if (window.lucide) {
        window.lucide.createIcons();
    }
}

function filterProducts() {
    const searchTerm = searchInput.value.trim().toLocaleLowerCase("pt-BR");
    const filteredProducts = products.filter((product) =>
        `${product.nome} ${product.categoria}`.toLocaleLowerCase("pt-BR").includes(searchTerm)
    );
    renderProducts(filteredProducts);
}

async function loadProducts() {
    try {
        const result = await requestApi("/api/produtos");
        products = Array.isArray(result.data) ? result.data : [];
        updateMetrics(products);
        filterProducts();
    } catch (error) {
        productTable.replaceChildren();
        metrics.totalItems.textContent = "—";
        metrics.stockValue.textContent = "—";
        metrics.outOfStock.textContent = "—";
        metrics.productCount.textContent = "Não foi possível atualizar";
        const row = document.createElement("tr");
        const cell = createCell(
            "Não foi possível carregar os produtos. Verifique a conexão e tente novamente.",
            "px-6 py-12 text-center text-sm text-rose-600"
        );
        cell.colSpan = 6;
        row.append(cell);
        productTable.append(row);
        throw error;
    }
}

function setSaveLoading(isLoading) {
    saveButton.disabled = isLoading;
    saveButton.innerHTML = isLoading
        ? '<span class="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white"></span> Salvando...'
        : '<i data-lucide="check" class="h-4 w-4"></i> Salvar produto';
    if (window.lucide) {
        window.lucide.createIcons();
    }
}

productForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!productForm.reportValidity()) {
        return;
    }

    const formData = new FormData(productForm);
    const product = {
        nome: String(formData.get("nome")).trim(),
        categoria: String(formData.get("categoria")).trim() || "Geral",
        preco: Number(formData.get("preco")),
        quantidade: Number(formData.get("quantidade"))
    };

    setSaveLoading(true);
    try {
        const result = await requestApi("/api/produtos", {
            method: "POST",
            body: JSON.stringify(product)
        });
        productForm.reset();
        productDialog.close();
        searchInput.value = "";
        showToast(result.message || "Produto cadastrado com sucesso.");
        try {
            await loadProducts();
        } catch (refreshError) {
            const message = refreshError instanceof Error
                ? refreshError.message
                : "Não foi possível atualizar a lista.";
            showToast(`Produto salvo, mas a lista não foi atualizada: ${message}`, true);
        }
    } catch (error) {
        showToast(error instanceof Error ? error.message : "Não foi possível cadastrar o produto.", true);
    } finally {
        setSaveLoading(false);
    }
});

document.querySelector("#abrir-modal-produto").addEventListener("click", () => {
    productDialog.showModal();
    document.querySelector("#nome").focus();
});

["#fechar-modal-produto", "#cancelar-modal-produto"].forEach((selector) => {
    document.querySelector(selector).addEventListener("click", () => productDialog.close());
});

searchInput.addEventListener("input", filterProducts);

productTable.addEventListener("click", (event) => {
    if (!(event.target instanceof Element)) {
        return;
    }
    const button = event.target.closest("button[data-product-id]");
    if (!button) {
        return;
    }

    pendingDeleteId = Number(button.dataset.productId);
    const product = products.find((item) => Number(item.id) === pendingDeleteId);
    document.querySelector("#mensagem-confirmar-exclusao").textContent = product
        ? `O produto “${product.nome}” será removido permanentemente do estoque.`
        : "Esta ação não pode ser desfeita.";
    deleteDialog.showModal();
});

document.querySelector("#cancelar-exclusao").addEventListener("click", () => {
    pendingDeleteId = null;
    deleteDialog.close();
});

confirmDeleteButton.addEventListener("click", async () => {
    if (pendingDeleteId === null) {
        return;
    }

    confirmDeleteButton.disabled = true;
    try {
        const result = await requestApi(`/api/produtos/${pendingDeleteId}`, { method: "DELETE" });
        pendingDeleteId = null;
        deleteDialog.close();
        showToast(result.message || "Produto excluído com sucesso.");
        try {
            await loadProducts();
        } catch (refreshError) {
            const message = refreshError instanceof Error
                ? refreshError.message
                : "Não foi possível atualizar a lista.";
            showToast(`Produto excluído, mas a lista não foi atualizada: ${message}`, true);
        }
    } catch (error) {
        showToast(error instanceof Error ? error.message : "Não foi possível excluir o produto.", true);
    } finally {
        confirmDeleteButton.disabled = false;
    }
});

loadProducts().catch((error) => {
    showToast(error instanceof Error ? error.message : "Falha ao carregar os produtos.", true);
});
if (window.lucide) {
    window.lucide.createIcons();
}
