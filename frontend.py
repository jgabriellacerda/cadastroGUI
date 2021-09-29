from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
from PIL import Image, ImageTk

class MyRoot(Tk):
    def __init__(self, app, **kwargs) -> None:
        super().__init__()

        self.app = app
        self.btn_style = {'font': ('arial',18,'bold'), 'bg': "white", 'fg': "gray"}
        self.lbl_style = {'font': ('arial',30,'bold'), 'padx': 9, 'pady': 9, 'bg': "red", 'fg': "white"}

        self.ID = StringVar()
        self.Nome = StringVar()
        self.diaNasc = StringVar()
        self.mesNasc = StringVar()
        self.anoNasc = StringVar()
        self.EMail = StringVar()
        self.Cargo = StringVar()
        #self.Cargo = ttk.combobox(

        self.content_list = []

        self.title("CADASTRO MEMBROS")
        #root.geometry('1352x750+0+0')
        self.resizable(False,False)
        #self.wm_iconbitmap("rinoceronte.ico")
        self.configure(background='red')

        self.mainFrame = Frame(self, bg = "red", bd=10, relief=RIDGE).grid()

        self.frameLogo = FrameLogo(master=self.mainFrame, bg="red", bd=5, relief=RIDGE)
        self.frameLogo.grid(row=0,column=0,sticky=W+E)


        self.frameMenu = FrameMenu(self.mainFrame, self, bg = "red", bd=5, relief=RIDGE)
        self.frameMenu.grid(row=1,column=0,sticky=E+W+N+S)

        self.frameCadastro = FrameCadastro(master=self.mainFrame, root=self, bg = "red", bd=5, relief=RIDGE, **kwargs)
        self.frameCadastro.grid(row=2,column=0,sticky=E+W+N+S)
        # self.frameCadastro.grid_remove()
        self.content_list.append(self.frameCadastro)

        self.frameHorario = FrameHorario(self.mainFrame, bg = "red", bd=5, relief=RIDGE)
        self.frameHorario.grid(row=2,column=0,sticky=E+W+N+S)
        self.frameHorario.grid_remove()
        self.content_list.append(self.frameHorario)

        self.frameLogin = FrameLogin(self.mainFrame, self, bg = "red", bd=5, relief=RIDGE)
        self.frameLogin.grid(row=2,column=0,sticky=E+W+N+S)
        self.frameLogin.grid_remove()
        self.content_list.append(self.frameLogin)

        self.frameRodape = FrameRodape(self.mainFrame, self, bg = "red", bd=5, relief=RIDGE)
        self.frameRodape.grid(row=3,column=0,sticky=W+E)

        
        #run:
        self.updateContent('Login')

    def updateContent(self,frame_name):
        for frame in self.content_list:
            if frame.name == frame_name:
                frame.grid()
            else:
                frame.grid_remove()

    def show_buttons(self):
        self.frameMenu.show_buttons()


class FrameLogo(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)

        load = Image.open("logo2.png")
        width, height = load.size
        load = load.resize((round(140/height*width) , round(140)))
        self.logo = ImageTk.PhotoImage(load)
        img = Label(self, image=self.logo, bg='red').grid(row=0, column=0, padx=202, columnspan=2, sticky=W+E)


class FrameMenu(Frame):
    def __init__(self, frame, root, **kwargs) -> None:
        super().__init__(frame, **kwargs)

        self.root = root
        self.btnCadastro = Button(self,text='Cadastro',command= lambda: root.updateContent('Cadastro'),**self.root.btn_style)
        self.btnCadastro.grid(row=0,column=0)
        self.btnHorarios = Button(self,text='Horários',command= lambda: root.updateContent('Horario'),**self.root.btn_style)
        self.btnHorarios.grid(row=0,column=1)
        self.btnLogin = Button(self,text='Login',command= lambda: root.updateContent('Login'),**self.root.btn_style)
        self.btnLogin.grid(row=0,column=2,sticky=E)

        self.btnCadastro.grid_remove()
        self.btnHorarios.grid_remove()
    
    def show_buttons(self):
        self.btnCadastro.grid()
        self.btnHorarios.grid()
        self.btnLogin.grid_remove()
        

class FrameCadastro(Frame):
    def __init__(self, master, root, **kwargs):

        self.root = root
        buscarDados = kwargs.pop('funcBuscarDados')
        confirmarAtt = kwargs.pop('funcConfirmarAtt')
        novoMembro = kwargs.pop('funcNovoMembro')

        super().__init__(master, **kwargs)

        self.name = 'Cadastro'

        frameID = Frame(self, bg = "red", relief=RIDGE)
        frameID.grid(row=0,column=1,columnspan=2)
        lblID = Label(self,text='ID:',**self.root.lbl_style,justify=RIGHT).grid(row=0,column=0,sticky=E)
        txtID = Entry(frameID,textvariable=root.ID,font=('arial',30,'bold'),bg="white",fg="gray",justify=LEFT).grid(row=0,column=0,padx=5,sticky=W+E)
        btnSearch = Button(frameID,text='Buscar',command=buscarDados,pady=1,**self.root.btn_style,justify=LEFT).grid(row=0,column=1,padx=5,sticky=W)

        lblNome = Label(self,text='Nome:',**self.root.lbl_style,justify=RIGHT).grid(row=1,column=0,sticky=E)
        txtNome = Entry(self,textvariable=root.Nome,font=('arial',30,'bold'),bg="white",fg="gray",justify=LEFT).grid(row=1,column=1,padx=5,sticky=W+E,columnspan=2)

        frameNasc = Frame(self, bg = "red", bd=0, relief=RIDGE)
        frameNasc.grid(row=2,column=1,sticky=W,columnspan=2)
        lblNasc = Label(self,text='Nascimento:',**self.root.lbl_style,justify=RIGHT).grid(row=2,column=0,sticky=E)
        txtNasc1 = Entry(frameNasc,width=2,textvariable=root.diaNasc,font=('arial',30,'bold'),bg="white",fg="gray",justify=LEFT).grid(row=2,column=1,padx=5,sticky=E)
        lblBarra1 = Label(frameNasc,text='/',font=('arial',30,'bold'),bg="red",fg="white",justify=RIGHT).grid(row=2,column=2,padx=5)
        txtNasc2 = Entry(frameNasc,width=2,textvariable=root.mesNasc,font=('arial',30,'bold'),bg="white",fg="gray",justify=LEFT).grid(row=2,column=3,padx=5)
        lblBarra2 = Label(frameNasc,text='/',font=('arial',30,'bold'),bg="red",fg="white",justify=RIGHT).grid(row=2,column=4,padx=5)
        txtNasc3 = Entry(frameNasc,width=4,textvariable=root.anoNasc,font=('arial',30,'bold'),bg="white",fg="gray",justify=LEFT).grid(row=2,column=5,padx=5)

        lblEMail = Label(self,text='E-mail:',**self.root.lbl_style,justify=RIGHT).grid(row=3,column=0,sticky=E)
        txtEMail = Entry(self,textvariable=root.EMail,font=('arial',30,'bold'),bg="white",fg="gray",justify=LEFT).grid(row=3,column=1,sticky=E+W,padx=5,columnspan=2)

        frameCargo = Frame(self, bg = "red", bd=0, relief=RIDGE)
        frameCargo.grid(row=4,column=1,sticky=W,columnspan=2)
        lblCargo = Label(self,text='Cargo:',**self.root.lbl_style,justify=RIGHT).grid(row=4,column=0,sticky=E)
        cargoOptions = ttk.Combobox(frameCargo, values=['Membro', 'Coordenador', 'Gerente'], textvariable=root.Cargo, font=('arial', 30, 'bold'), state='readonly')
        cargoOptions.grid(row=4,column=1,padx=5,sticky=E)
        cargoOptions.current(0)

        btnSend = Button(self,text='Atualizar Dados',command=confirmarAtt,**self.root.btn_style).grid(row=6,column=1,padx=5,pady=9,sticky=W)

        btnNew = Button(self,text='Cadastrar Novo Membro',command=novoMembro,**self.root.btn_style).grid(row=6,column=2,padx=5,sticky=W)


class FrameHorario(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.name = 'Horario'


class FrameLogin(Frame):
    def __init__(self, master, root, **kwargs):
        super().__init__(master, **kwargs)

        self.root = root
        self.user = StringVar()
        self.password = StringVar()
        self.phone = StringVar()

        self.name = 'Login'

        email = 'gabriel.lacerda@engenharia.ufjf.br'
        password = '654321'

        self.user.set(email)
        self.password.set(password)

        lblID = Label(self,text='Usuário:',**self.root.lbl_style,justify=RIGHT).grid(row=1,column=0,sticky=E)
        txtID = Entry(self,textvariable=self.user,font=('arial',30,'bold'),bg="white",fg="gray",justify=LEFT).grid(row=1,column=1,padx=5,sticky=W+E)
        lblID = Label(self,text='Senha:',**self.root.lbl_style,justify=RIGHT).grid(row=2,column=0,sticky=E)
        txtID = Entry(self,textvariable=self.password,show="*",font=('arial',30,'bold'),bg="white",fg="gray",justify=LEFT).grid(row=2,column=1,padx=5,sticky=W+E)
        # lblID = Label(self,text='Celular:',**self.root.lbl_style,justify=RIGHT).grid(row=3,column=0,sticky=E)
        # txtID = Entry(self,textvariable=self.phone,font=('arial',30,'bold'),bg="white",fg="gray",justify=LEFT).grid(row=3,column=1,padx=5,sticky=W+E)

        frameBtns = Frame(self, bg = "red", bd=0, relief=RIDGE)
        frameBtns.grid(row=4,column=1,sticky=W)
        btnSearch = Button(frameBtns,text='Entrar',command=self.entrar,pady=1,**self.root.btn_style,justify=RIGHT).grid(row=0,column=0,padx=5,sticky=W)
        btnSearch = Button(frameBtns,text='Nova Conta',command=self.novaConta,pady=1,**self.root.btn_style,justify=LEFT).grid(row=0,column=1,padx=5,sticky=W)

    def novaConta(self):
        if self.root.app.firebase_con.signup(self.user.get(), self.password.get(), self.phone.get()):
            self.root.mostrarCadastro()
        else:
            messagebox.showinfo(self.root.Nome.get(), 'Usuário ou senha inválidos')
        print("Nova Conta")

    def entrar(self):
        if self.root.app.firebase_con.login(self.user.get(), self.password.get()):
            self.root.show_buttons()
            self.root.updateContent('Cadastro')
        else:
            messagebox.showinfo(self.root.Nome.get(), 'Usuário ou senha inválidos')
        print("Entrar")

class FrameRodape(Frame):
    def __init__(self, frame, root, **kwargs) -> None:
        super().__init__(frame, kwargs)

        self.root = root

        self.data = StringVar()
        self.hora = StringVar()

        self.data.set(time.strftime("%d/%m/%Y"))
        self.hora.set(time.strftime("%H:%M:%S"))

        self.lblData = Label(self,textvariable=self.data,font=('arial',15,'bold'),pady=5,bg="red",fg="white").grid(row=0,column=0,sticky=W)
        self.btnExit = Button(self,text='Sair',command=root.destroy,**self.root.btn_style).grid(row=0,column=1,padx=286,sticky=W+E)
        #lblSpace = Label(frameRodape,text=' ',font=('arial',15,'bold'),padx=315,bg="red",fg="white").grid(row=0,column=1)
        self.lblHora = Label(self,textvariable=self.hora,font=('arial',15,'bold'),pady=5,bg="red",fg="white").grid(row=0,column=2,sticky=E)

        self.attDataHora()

    def attDataHora(self):
        self.data.set(time.strftime("%d/%m/%Y"))
        self.hora.set(time.strftime("%H:%M:%S"))
        self.after_id = self.root.after(1000,self.attDataHora)
