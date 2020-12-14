import sys
input('Chegou aqui01-')
import pandas as pd
input('Chegou aqui02-')
import pymysql
from InterfacesGraficasPyqt.admOrdens import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QErrorMessage
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
conn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="bd_ceara_satel")
cur = conn.cursor()
class Principal(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.btnBuscarCarta.clicked.connect(self.CarregaCampos)
        self.btnUpdate.clicked.connect(self.UpdateCartas)

    def abrirImagem(self):
        imagem, _ = QFileDialog.getOpenFileName(
            self.centralwidget, 'Abrir Imagem',
            r'C:/Users/Administrador Satel/Desktop/'
        )

    def CarregaCampos(self):
        try:

            campoCarta = self.txtCarta.text()
            cartafor = 'CE.' + campoCarta + '/2020'
            print(cartafor)

            sql = f"select t1.id, t1.protocolo, t1.n_carta, t1.n_ordem,t1.uc,t1.projeto, t1.nome_cliente," \
                  f"t1.parecer, t1.analista,     t1.envio_carta, t1.data_parecer, t1.status_prazo," \
                  f"t1.email, t1.art, t1.usuario, t1.data_entrada, t1.data_seg_analise, t1.data_ter_analise," \
                  f"t2.id as id_form, t2.responsavel_tec,t2.rua, t2.bairro, t2.municipio, t2.cep," \
                  f"t2.n_residencia,t2.endereco  from tb_demanda_nv t1 left   join  tb_form_docs_nv  t2 on" \
                  f" t1.protocolo = t2.protocolo where n_carta = '{cartafor}' limit 1"
            tbOrdens = pd.read_sql(sql, conn)
            lista = tbOrdens.values.tolist()

            contadorSql = f"select   CASE  WHEN data_entrada is not null and data_seg_analise is null and data_ter_analise is null THEN  '1ª Análise' " \
                          f"WHEN data_entrada is not null and data_seg_analise is not null and data_ter_analise is null THEN '2ª Análise'  " \
                          f"WHEN data_entrada is not null and data_seg_analise is not null and data_ter_analise is not null THEN '3ª Análise' " \
                          f" ELSE 'VerificarLoigica' END contador from tb_demanda_nv  where n_carta  like '%{campoCarta}%' limit 1"
            contTb = pd.read_sql(contadorSql, conn)
            listaCont = contTb.values.tolist()
            id = str(lista[0][0])
            protocolo = lista[0][1]
            n_carta = lista[0][2]
            n_ordem = lista[0][3]
            uc = str(lista[0][4])
            projeto = str(lista[0][5])
            nome_cliente = str(lista[0][6])
            parecer = lista[0][7]
            analista = lista[0][8]
            envio_carta = lista[0][9]
            data_parecer = lista[0][10]
            status_prazo = lista[0][11]
            email = lista[0][12]
            art = lista[0][13]
            usuario = lista[0][14]
            data_entrada = str(lista[0][15])
            data_seg_analise = str(lista[0][16])
            data_ter_analise = str(lista[0][17])
            id_form = lista[0][18]
            responsavel_tec = lista[0][19]
            rua = lista[0][20]
            bairro = lista[0][21]
            cidade = lista[0][22]
            cep = lista[0][23]
            n_residencia = lista[0][24]
            endereco = lista[0][25]

            self.txtCarta.setText(n_carta)
            self.txtContador.setText(listaCont[0][0])
            self.txtProtocolo.setText(protocolo)
            self.txtDataEntr.setText(data_entrada)
            self.txtOrdem.setText(n_ordem)
            self.txtUC.setText(uc)
            self.txtTipoProjeto.setText(projeto)
            self.txtCliente.setText(nome_cliente)
            self.txtParecer.setText(parecer)
            self.txtIdCarta.setText(id)
            self.txtEmail.setText(email)
            self.txtTelefone.setText('')
            self.txtRua.setText(rua)
            self.txtBairro.setText(bairro)
            self.txtCidade.setText(cidade)
            self.txtCep.setText(cep)
            self.txtEndereco.setText(endereco)



        except:
            QMessageBox.about(self, "Erro", "Falha - Não Encontrado")

    def UpdateCartas(self):
        conn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="bd_ceara_satel")
        cur = conn.cursor()

        id = self.txtIdCarta.text()
        n_carta = self.txtCarta.text()
        contador = self.txtContador.text()
        protocolo = self.txtProtocolo.text()
        data_entrada = self.txtDataEntr.text()
        ordem = self.txtOrdem.text()
        uc = self.txtUC.text()
        tipo_projeto = self.txtTipoProjeto.text()
        cliente = self.txtCliente.text()
        parecer = self.txtParecer.text()

        print('começou')
        print(id)
        sqlUpdate = f"UPDATE bd_ceara_satel.tb_demanda_nv SET parecer = '{parecer}' , uc = '{uc}', protocolo = '{protocolo}'," \
                    f" n_ordem = '{ordem}'  where  (id = '{id}')"
        try:

            print(sqlUpdate)
            cur.execute(sqlUpdate)
            print('foi01')
            conn.commit()
            conn.close()
            print('foi02')
            QMessageBox.about(self, "Atualizado", "Sucesso!")
        except:
            QMessageBox.about(self, "Erro", "Falha - Não Atualizado")

    def UpdadeDadosCliente(self):
        conn = pymysql.connect(host="localhost", port=3306, user="root", password="", db="bd_ceara_satel")
        cur = conn.cursor()

        protocolo = self.txtProtocolo.text()
        sql = f"SELECT id, protocolo FROM bd_ceara_satel.tb_form_docs_nv  where protocolo = '{protocolo}' "
        print(sql)
        tabela = pd.read_sql(sql, conn)
        print()
        lista = tabela.values.tolist()
        print(lista)

        idForm = str(lista[0][0])
        protocolo = str(lista[0][1])

        print(idForm)
        self.txtIdFormDoc.setText(idForm)
        idf = self.txtIdFormDoc.text()

        print(':: ', idf)
        email = self.txtEmail.text()
        tel = self.txtTelefone.text()
        rua = self.txtRua.text()
        bairro = self.txtBairro.text()
        cidade = self.txtCidade.text()
        cep = self.txtCep.text()
        endereco = self.txtEndereco.text()
        try:

            sqlUpDadosCli = f"UPDATE tb_form_docs_nv SET email = '{email}' , telefone = '{tel}', rua = '{rua}', " \
                            f"bairro = '{bairro}', cidade = '{cidade}', cep = '{cep}' , endereco = '{endereco}' " \
                            f"where  (`id` = '{idf}')"
            print(sqlUpDadosCli)
            cur.execute(sqlUpDadosCli)
            print('chegou')
            conn.commit()
            conn.close()
            QMessageBox.about(self, "Atualizado", "Sucesso!")
        except:
            QMessageBox.about(self, "Erro", "Falha - Não Atualizado")


# Parte Obrigatoria
if __name__ == '__main__':
    qt = QApplication(sys.argv)
    principal = Principal()
    principal.show()

    qt.exec_()
