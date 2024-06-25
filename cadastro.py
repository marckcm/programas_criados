from tkinter import *
from tkinter import ttk
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

"""
Parei na aula 15
https://www.youtube.com/watch?v=ACDYzd-S3SA&list=PLqx8fDb-FZDFznZcXb_u_NyiQ7Nai674-&index=16&ab_channel=RafaelSerafim
"""

root = Tk()


# Back End
class Funcoes():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.endereco_entry.delete(0, END)
    
    def conectar_bd(self):
        self.conectar = sqlite3.connect("clientes.bd")
        self.cursor = self.conectar.cursor(); print("Banco de dados Conectado com sucesso")
    
    def desconectar_bd(self):
        self.conectar.close(); print("Banco de dados desconectado com sucesso")
    
    def montar_tabelas(self):
        self.conectar_bd()
        # Criando a Tabela
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS clientes (
                            cod INTEGER PRIMARY KEY,
                            nome_cliente CHAR(40) NOT NULL,
                            telefone INTEGER(20),
                            endereco CHAR(40)
                            );
                            """)        
        self.conectar.commit(); print("Banco de dados Criado")
        self.desconectar_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.endereco = self.endereco_entry.get()

    def add_cliente(self):
        self.variaveis()
        self.conectar_bd()
        self.cursor.execute("""INSERT INTO clientes (nome_cliente, telefone, endereco)
                            VALUES (?, ?, ?)""", (self.nome, self.telefone, self.endereco))
        self.conectar.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpa_tela()
    
    def select_lista(self):
        self.lista_cliente.delete(*self.lista_cliente.get_children())
        self.conectar_bd()
        lista = self.cursor.execute("""SELECT cod, nome_cliente, telefone, endereco FROM clientes
                                    ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.lista_cliente.insert("", END, values = i)
        self.desconectar_bd()

    def ondoubleclick(self, event):
        self.limpa_tela()
        self.lista_cliente.selection()
        for n in self.lista_cliente.selection():
            col1, col2, col3, col4 = self.lista_cliente.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.endereco_entry.insert(END, col4)

    def deleta_cliente(self):
        self.variaveis()
        self.conectar_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conectar.commit()
        self.desconectar_bd()
        self.limpa_tela()
        self.select_lista()

    def alterar_cliente(self):
        #criado self variareis para não ficar repetindo codigos caso
        #coloque mais campos pode ser alterado nessas variaveis
        self.variaveis()
        self.conectar_bd()
        self.cursor.execute("""UPDATE clientes SET nome_cliente = ?, telefone = ?, endereco = ?
                            WHERE cod = ? """, (self.nome, self.telefone, self.endereco, self.codigo))
        self.conectar.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpa_tela()

    def buscar_cliente(self):
        self.conectar_bd()
        self.lista_cliente.delete(*self.lista_cliente.get_children())
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute("""SELECT cod, nome_cliente, telefone, endereco FROM clientes
                            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        busca_nome_cliente = self.cursor.fetchall()
        for i in busca_nome_cliente:
            self.lista_cliente.insert("", END, values=i)
        self.limpa_tela()
        self.desconectar_bd()

class Relatorios():
    # Salva e abre o PDF feito com reportlab "pip install reportlab"
    def printcliente(self):
        webbrowser.open("cliente.pdf")
    
    # Gera o Pdf
    def gera_rel_cliente(self):
        # variavel 
        self.c = canvas.Canvas("cliente.pdf")
        
        # pega os dados
        self.codigo_rel = self.codigo_entry.get()
        self.nome_rel = self.nome_entry.get()
        self.telefone_rel = self.telefone_entry.get()
        self.endereco_rel = self.endereco_entry.get()
        
        # fonts do Titulo
        self.c.setFont("Helvetica-Bold", 24)
        # titulo linha 100 a 600 (margem) x coluna 100 a 800 (margem altura)
        self.c.drawString(200, 790, "Ficha do Cliente")

        # Corpo do Texto
        self.c.setFont("Helvetica-Bold", 16)
        self.c.drawString(50, 700, "Código: ")
        self.c.drawString(50, 670, "Nome: ")
        self.c.drawString(50, 640, "Telefone: ")
        self.c.drawString(50, 610, "Endereço: ")
        # Dados do banco de dados
        self.c.setFont("Helvetica", 16)
        self.c.drawString(150, 700, self.codigo_rel)
        self.c.drawString(150, 670, self.nome_rel)
        self.c.drawString(150, 640, self.telefone_rel)
        self.c.drawString(150, 610, self.endereco_rel)

        # Borda dos dados do cliente pode virar linha também mudando o fill e stroke e o 4 numero (120)
        self.c.rect(20, 600, 550, 120, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printcliente()


# Front End
class Aplication(Funcoes, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.widgets_frame2()
        self.montar_tabelas()
        self.select_lista()
        self.menus()
        root.mainloop()
    
    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background="#1e3743")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)
    
    def frames_da_tela(self):

        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee',
                              highlightbackground='#759fe6', highlightthickness=3)
        #tipos de frames place(rely relx) *** pack *** grid 
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6',
                             highlightthickness=3)
        #tipos de frames place(rely relx) *** pack *** grid 
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        # Criando botões:
        # Criando botão limpar
        self.bt_limpar = Button(self.frame_1, text="Limpar",
                                bd=2, bg="#107db2", fg="white", font=('verdana', 8, 'bold'),
                                command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15) 

        # criando botão buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar",
                                bd=2, bg="#107db2", fg="white", font=('verdana', 8, 'bold'),
                                command=self.buscar_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15) 
        
        # criando botão Novo
        self.bt_novo = Button(self.frame_1, text="Novo",
                                bd=2, bg="#107db2", fg="white", font=('verdana', 8, 'bold'),
                                command= self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15) 
        
        # criando botão Alterar
        self.bt_alterar = Button(self.frame_1, text="Alterar",
                                bd=2, bg="#107db2", fg="white", font=('verdana', 8, 'bold'),
                                command=self.alterar_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15) 

        # criando botão Apagar
        self.bt_apagar = Button(self.frame_1, text="Apagar",
                                bd=2, bg="#107db2", fg="white", font=('verdana', 8, 'bold'),
                                command= self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15) 

        # Criando as labels e entrada de dados:
        #labels do código (texto)
        self.lb_codigo = Label(self.frame_1, text="Código", bg='#dfe3ee', fg="#107db2")
        self.lb_codigo.place(relx=0.05, rely=0.05) 
        # Input do Código (Entradade dados)
        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.07)

        #labels do Nome (texto)
        self.lb_nome = Label(self.frame_1, text="Nome", bg='#dfe3ee', fg="#107db2")
        self.lb_nome.place(relx=0.05, rely=0.35) 
        # Input do Nome (Entradade dados)
        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.50)

        #labels do Telefone (texto)
        self.lb_telefone = Label(self.frame_1, text="Telefone", bg='#dfe3ee', fg="#107db2")
        self.lb_telefone.place(relx=0.05, rely=0.6) 
        # Input do Telefone (Entradade dados)
        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.2)

        #labels do Endereço (texto)
        self.lb_endereco = Label(self.frame_1, text="Endereço", bg='#dfe3ee', fg="#107db2")
        self.lb_endereco.place(relx=0.3, rely=0.6) 
        # Input do Endereço (Entradade dados)
        self.endereco_entry = Entry(self.frame_1)
        self.endereco_entry.place(relx=0.3, rely=0.7, relwidth=0.5)

    def widgets_frame2(self):
        # Criação das Colunas
        self.lista_cliente = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3", "col4"))
        self.lista_cliente.heading("#0", text="")
        self.lista_cliente.heading("#1", text="Código")
        self.lista_cliente.heading("#2", text="Nome")
        self.lista_cliente.heading("#3", text="Telefone")
        self.lista_cliente.heading("#4", text="Endereço")
        #Tamanho Das Proporções das colunas 
        self.lista_cliente.column("#0", width=1)
        self.lista_cliente.column("#1", width=50)
        self.lista_cliente.column("#2", width=200)
        self.lista_cliente.column("#3", width=125)
        self.lista_cliente.column("#4", width=125)
        # Posição da Coluna referente ao 2 frame
        self.lista_cliente.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85) 
        # Barra de rolagem
        self.scrool_lista = Scrollbar(self.frame_2, orient="vertical")
        self.lista_cliente.configure(yscroll=self.scrool_lista.set)
        self.scrool_lista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.lista_cliente.bind("<Double-1>", self.ondoubleclick)

    def menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def quit():
            self.root.destroy()
        # Primeira Guia do menu
        menubar.add_cascade(label= "Tela", menu=filemenu)
        menubar.add_cascade(label= "Opções", menu=filemenu2)
        filemenu.add_command(label= "Ficha do Cliente", command=self.gera_rel_cliente )
        filemenu.add_command(label= "Sair", command=quit)
        # Segundo Guia do menu
        filemenu2.add_command(label= "Limpa Tela", command=self.limpa_tela)
        filemenu2.add_command(label= "Adicionar", command=self.add_cliente)
        filemenu2.add_command(label= "Alterar", command=self.alterar_cliente)
        filemenu2.add_command(label= "Deletar", command=self.deleta_cliente)


Aplication()
