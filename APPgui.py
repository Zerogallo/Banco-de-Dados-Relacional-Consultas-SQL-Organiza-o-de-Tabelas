import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2


class AppBD:
    """Classe para gerenciar a conexão e operações com o banco de dados"""
    
    def __init__(self):
        self.conn = psycopg2.connect(
            host="127.0.0.1",
            database="postgresDB",
            user="postgres",
            password="admin123"
        )
        self.cursor = self.conn.cursor()
        self.criar_tabela()
    
    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS PRODUTOS (
                codigo SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                preco DECIMAL(10,2) NOT NULL
            )
        """)
        self.conn.commit()
    
    def inserir_dados(self, nome, preco):
        sql = "INSERT INTO PRODUTOS (nome, preco) VALUES (%s, %s)"
        self.cursor.execute(sql, (nome, preco))
        self.conn.commit()
    
    def selecionar_dados(self):
        self.cursor.execute("SELECT codigo, nome, preco FROM PRODUTOS ORDER BY CODIGO")
        return self.cursor.fetchall()
    
    def atualizar_dados(self, codigo, nome, preco):
        sql = "UPDATE PRODUTOS SET nome = %s, preco = %s WHERE CODIGO = %s"
        self.cursor.execute(sql, (nome, preco, codigo))
        self.conn.commit()
    
    def excluir_dados(self, codigo):
        sql = "DELETE FROM PRODUTOS WHERE CODIGO = %s"
        self.cursor.execute(sql, (codigo,))
        self.conn.commit()
    
    def fechar_conexao(self):
        self.cursor.close()
        self.conn.close()


class PrincipalBD:
    """Classe para gerenciar a interface gráfica"""
    
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Gestão de Produtos")
        self.root.geometry("600x400")
        self.root.config(bg="#333333")
        
        # Componentes da interface gráfica
        self.lblCodigo = tk.Label(root, text="Código", bg="#333333", fg="white")
        self.lblCodigo.grid(row=0, column=0, padx=5, pady=5)
        self.txtCodigo = tk.Entry(root)
        self.txtCodigo.grid(row=0, column=1, padx=5, pady=5)
        
        self.lblNome = tk.Label(root, text="Nome", bg="#333333", fg="white")
        self.lblNome.grid(row=1, column=0, padx=5, pady=5)
        self.txtNome = tk.Entry(root)
        self.txtNome.grid(row=1, column=1, padx=5, pady=5)
        
        self.lblPreco = tk.Label(root, text="Preço", bg="#333333", fg="white")
        self.lblPreco.grid(row=2, column=0, padx=5, pady=5)
        self.txtPreco = tk.Entry(root)
        self.txtPreco.grid(row=2, column=1, padx=5, pady=5)
        
        # Botões
        self.btnCadastrar = tk.Button(root, text="Cadastrar", command=self.fCadastrarProduto)
        self.btnCadastrar.grid(row=3, column=0, padx=5, pady=5)
        
        self.btnAtualizar = tk.Button(root, text="Atualizar", command=self.fAtualizarProduto)
        self.btnAtualizar.grid(row=3, column=1, padx=5, pady=5)
        
        self.btnExcluir = tk.Button(root, text="Excluir", command=self.fExcluirProduto)
        self.btnExcluir.grid(row=4, column=0, padx=5, pady=5)
        
        self.btnLimpar = tk.Button(root, text="Limpar", command=self.fLimparTela)
        self.btnLimpar.grid(row=4, column=1, padx=5, pady=5)
        
        # Treeview para listar produtos
        self.tree = ttk.Treeview(root, columns=("CODIGO", "NOME", "PRECO"), show='headings', height=10)
        self.tree.heading("CODIGO", text="Código")
        self.tree.heading("NOME", text="Nome")
        self.tree.heading("PRECO", text="Preço")
        self.tree.column("CODIGO", width=80)
        self.tree.column("NOME", width=200)
        self.tree.column("PRECO", width=100)
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.tree.bind('<ButtonRelease-1>', self.apresentarRegistrosSelecionados)
        
        # Carregar dados iniciais
        self.carregarDadosIniciais()
    
    def carregarDadosIniciais(self):
        """Carrega os dados do banco de dados na treeview"""
        # Limpar a treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar registros do banco
        registros = self.db.selecionar_dados()
        
        # Inserir na treeview
        for registro in registros:
            self.tree.insert("", "end", values=registro)
    
    def fCadastrarProduto(self):
        """Cadastra um novo produto"""
        codigo = self.txtCodigo.get()
        nome = self.txtNome.get()
        preco = self.txtPreco.get()
        
        # Validação
        if not nome or not preco:
            messagebox.showerror("Erro", "Nome e Preço são obrigatórios!")
            return
        
        try:
            preco_float = float(preco)
            self.db.inserir_dados(nome, preco_float)
            self.carregarDadosIniciais()
            self.fLimparTela()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número válido!")
    
    def fAtualizarProduto(self):
        """Atualiza um produto existente"""
        codigo = self.txtCodigo.get()
        nome = self.txtNome.get()
        preco = self.txtPreco.get()
        
        if not codigo:
            messagebox.showerror("Erro", "Selecione um produto para atualizar!")
            return
        
        if not nome or not preco:
            messagebox.showerror("Erro", "Nome e Preço são obrigatórios!")
            return
        
        try:
            preco_float = float(preco)
            self.db.atualizar_dados(codigo, nome, preco_float)
            self.carregarDadosIniciais()
            self.fLimparTela()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número válido!")
    
    def fExcluirProduto(self):
        """Exclui um produto"""
        codigo = self.txtCodigo.get()
        
        if not codigo:
            messagebox.showerror("Erro", "Selecione um produto para excluir!")
            return
        
        confirmar = messagebox.askyesno("Confirmar", "Deseja realmente excluir este produto?")
        if confirmar:
            self.db.excluir_dados(codigo)
            self.carregarDadosIniciais()
            self.fLimparTela()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
    
    def fLimparTela(self):
        """Limpa os campos de entrada"""
        self.txtCodigo.delete(0, tk.END)
        self.txtNome.delete(0, tk.END)
        self.txtPreco.delete(0, tk.END)
    
    def apresentarRegistrosSelecionados(self, event):
        """Exibe os dados do produto selecionado nos campos de entrada"""
        selecionado = self.tree.selection()
        if selecionado:
            item = selecionado[0]
            valores = self.tree.item(item, "values")
            
            self.txtCodigo.delete(0, tk.END)
            self.txtCodigo.insert(tk.END, valores[0])
            
            self.txtNome.delete(0, tk.END)
            self.txtNome.insert(tk.END, valores[1])
            
            self.txtPreco.delete(0, tk.END)
            self.txtPreco.insert(tk.END, valores[2])


# Execução principal
if __name__ == "__main__":
    root = tk.Tk()
    app_bd = AppBD()
    app_gui = PrincipalBD(root, app_bd)
    
    # Garantir que a conexão seja fechada ao fechar a janela
    def on_closing():
        app_bd.fechar_conexao()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()