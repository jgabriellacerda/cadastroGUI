# -*- coding: utf-8 -*-

from sql_db_handler import SQL_DB_Handler
import pygame
# import pyodbc
from tkinter import *
from tkinter import messagebox
import pygame, sys, random
from PIL import Image, ImageTk
import firebase_connection as firebase_con

import frontend
import dataChecker


email = 'gabriel.lacerda@engenharia.ufjf.br'
password = '654321'
login = {'email': email, 'password': password}

class MyApp():
    def __init__(self) -> None:
        self.firebase_con = firebase_con.FirebaseConnection()

        self.nDias = 5
        self.nHorarios = 12
        self.strDias = ['Segunda','Terça','Quarta','Quinta','Sexta']
        self.strHoras = [str(x+7)+"h" for x in range(self.nHorarios)]

        self.var_keys = ['nome', 'email', 'dataNascimento', 'cargo', 'categoria_area', 'dataIngresso',
                         'cidadeOrigem', 'curso', 'previsaoConclusao', 'cidadeAtual', 'tamCamisa', 'celular']

        self.database_type = 'firebase'

        self.sql_db = SQL_DB_Handler(self.strDias, self.strHoras)

        pygame.init()

        kwargs = {  'funcBuscarDados': self.buscarDados,
                'funcConfirmarAtt': self.confirmarAtt,
                'funcNovoMembro': self.novoMembro
                }

        self.root = frontend.MyRoot(self, **kwargs)

        self.btnMtxHorarios = [[0 for x in range(self.nDias)] for y in range(self.nHorarios)]
        self.boolMtxHorarios = [[1 for x in range(self.nDias)] for y in range(self.nHorarios)]
        self.corMatriz = [[StringVar() for x in range(self.nDias)] for y in range(self.nHorarios)]

        lblHorarios = [Label(self.root.frameHorario,text=self.strHoras[x],width=3,font=('arial',15,'bold'),padx=9,bg="red",fg="white",justify=CENTER).grid(row=x+1,column=0,sticky=E) for x in range(self.nHorarios)]
        lblDias = [Label(self.root.frameHorario,text=self.strDias[x],width=8,font=('arial',25,'bold'),padx=9,pady=5,bg="red",fg="white",justify=CENTER).grid(row=0,column=x+1,sticky=E) for x in range(self.nDias)]
        for i in range(self.nHorarios):
            for j in range(self.nDias):
                self.btnMtxHorarios[i][j] = Button(self.root.frameHorario,width=10,command=lambda x1=i,y1=j: self.alternarBotao(x1,y1),text="Disponível",bg='pale green',font=('arial',10,'bold'),fg="gray25")
                self.btnMtxHorarios[i][j].grid(row=i+1,column=j+1,sticky=W+E+N+S)

        frameComparar = Frame(self.root.mainFrame, bg="red", bd=5, relief=RIDGE)
        frameComparar.grid(row=2,column=0,sticky=E+W+N+S)
        frameComparar.grid_remove()


    def novoMembro(self):
        data = {}
        for var_key in self.var_keys:
            if var_key == 'dataNascimento':
                data[var_key] = f"{self.root.dict_vars[var_key][0].get()}/{self.root.dict_vars[var_key][1].get()}/{self.root.dict_vars[var_key][2].get()}"
            else:
                data[var_key] = self.root.dict_vars[var_key].get()

        if not dataChecker.checkDate(data['dataNascimento']):
            messagebox.showinfo(self.root.Nome.get(), 'Data de nascimento inválida!')
            return
        elif not dataChecker.checkEmail(data['email']):
            messagebox.showinfo(self.root.Nome.get(), 'E-mail inválido!')
            return
        elif not dataChecker.checkName(data['nome']):
            messagebox.showinfo(self.root.Nome.get(), 'Nome inválido!')
            return
        elif not dataChecker.checkCargo(data['cargo']):
            messagebox.showinfo(self.root.Nome.get(), 'Cargo inválido!')
            return
        if self.database_type == 'firebase':
            new_id = str(self.firebase_con.new_user_id())
            print("New ID: ",new_id)
            data['ID'] = new_id
            self.root.ID.set(new_id)
            self.firebase_con.new_person(data)
        else:
            new_id = self.sql_db.new_person(data, self.boolMtxHorarios)


    def buscarDados(self):
        if self.database_type == 'firebase':
            dados = self.firebase_con.get_data(self.root.ID.get())
            if bool(dados):
                print("Dados buscados:",dados)
                for var_key in self.var_keys:
                    if var_key == 'dataNascimento':
                        dataNascimento = dados['dataNascimento'].split('/')
                        print(dataNascimento)
                        self.root.dict_vars[var_key][0].set(dataNascimento[0])
                        self.root.dict_vars[var_key][1].set(dataNascimento[1])
                        self.root.dict_vars[var_key][2].set(dataNascimento[2])
                    else:
                        self.root.dict_vars[var_key].set(dados[var_key])
        else:
            dados = self.sql_db.get_data(self.root.ID.get())
            self.root.nome.set(dados[1])
            self.root.email.set(dados[3])
            self.root.cargo.set(dados[4])
            self.root.diaNasc.set(dados[2].day)
            self.root.mesNasc.set(dados[2].month)
            self.root.anoNasc.set(dados[2].year)

            for j in range(self.nDias):
                dados = self.sql_db.get_schedule(self.strDias[j], self.root.ID.get())

                for i in range(self.nHorarios):
                    self.boolMtxHorarios[i][j] = int(dados[i+1])
                    self.formatarBotao(i,j)
                # conexao.commit()


    def confirmarAtt(self):
        resposta = messagebox.askquestion(self.root.nome.get(),"Deseja mesmo atualizar os dados?")
        if resposta == 'yes':
            self.atualizarDados()
            return


    def formatarBotao(self, i, j):
        if self.boolMtxHorarios[i][j] == 0:
            self.btnMtxHorarios[i][j].config(bg='tomato',text='Ocupado',relief=SUNKEN)
        else:
            self.btnMtxHorarios[i][j].config(bg='pale green',text='Disponível',relief=RAISED)


    def alternarBotao(self, i, j):
        self.boolMtxHorarios[i][j] = int(not self.boolMtxHorarios[i][j])
        self.formatarBotao(i,j)


    def atualizarDados(self):
        data = {}
        for var_key in self.var_keys:
            if var_key == 'dataNascimento':
                data[var_key] = f"{self.root.dict_vars[var_key][0].get()}/{self.root.dict_vars[var_key][1].get()}/{self.root.dict_vars[var_key][2].get()}"
            else:
                data[var_key] = self.root.dict_vars[var_key].get()
        if self.database_type == 'firebase':

            self.firebase_con.update_data(self.root.ID.get(), data)
        else:
            self.sql_db.update_data(data, self.boolMtxHorarios)


    def load_logo(self):
        load = Image.open("../logo2.png")
        width, height = load.size
        load = load.resize((round(140/height*width) , round(140)))
        self.logo = ImageTk.PhotoImage(load)
        img = Label(self.root.frameLogo, image=self.logo, bg='red').grid(row=0, column=0, padx=202, columnspan=2, sticky=W+E)

    def run(self):
        # self.load_logo()
        self.root.mainloop()

if __name__ == "__main__":
    app = MyApp().run()
