import sys
import os
import requests
from dotenv import load_dotenv

class Omie:
    def __init__(self, empresa):
        self.ListarCenarios = OmieListarCenarios(empresa)
        self.ListarClientes = OmieListarClientes(empresa)
        self.ListarProdutos = OmieListarProdutos(empresa)

class OmieListarCenarios:
    def __init__(self, empresa):
        self.empresa = empresa
        self.caminho = "geral/cenarios/"
        self.call = 'ListarCenarios'
        self.nPagina = 1
        self.nRegPorPagina = 20

    def executar(self):
        return OmieApi().executar(self, self.empresa) 

class OmieListarClientes:
    def __init__(self, empresa):
        self.empresa = empresa
        self.caminho = "geral/clientes/"
        self.call = 'ListarClientes'
        self.pagina = 1
        self.registros_por_pagina = 50

    def executar(self):
        return OmieApi().executar(self, self.empresa) 

    def todos(self):
        nome_lista_omie = "clientes_cadastro"
        self.registros_por_pagina = 500
        consulta = self.executar()
        total_de_paginas = consulta['total_de_paginas']
        lista = consulta[nome_lista_omie]
        while self.pagina < total_de_paginas:
            self.pagina += 1
            produtos = self.executar()[nome_lista_omie]
            for produto in produtos:
                lista.append(produto)

        return lista


class OmieListarProdutos:
    def __init__(self, empresa):
        self.empresa = empresa
        self.caminho = "geral/produtos/"
        self.call = 'ListarProdutos'
        self.pagina = 1
        self.registros_por_pagina = 50
        self.apenas_importado_api = 'N'
        self.filtrar_apenas_omiepdv = 'N'

    def executar(self):
        return OmieApi().executar(self, self.empresa)

    def todos(self):
        nome_lista_omie = "produto_servico_cadastro"
        self.registros_por_pagina = 500
        consulta = self.executar()
        total_de_paginas = consulta['total_de_paginas']
        lista = consulta[nome_lista_omie]
        while self.pagina < total_de_paginas:
            self.pagina += 1
            produtos = self.executar()[nome_lista_omie]
            for produto in produtos:
                lista.append(produto)

        return lista




class OmieApi:
    def __init__(self):
        self.caminho = ""
        self.call = ""

    def executar(self, metodo, empresa):

        self.__obter_empresa(empresa)

        metodo_json = self.__converter_json(metodo)

        parametros = metodo_json.copy()
        parametros.pop('caminho')
        parametros.pop('call')
        parametros.pop('empresa')

        json_data = {}
        json_data['app_key'] = self.__key
        json_data['app_secret'] = self.__secret
        json_data['call'] = metodo_json['call']
        json_data['param'] = [parametros]
        
        response = requests.post('https://app.omie.com.br/api/v1/' + metodo_json['caminho'], json=json_data)
        return response.json()

    def __obter_empresa(self, empresa):
        load_dotenv()

        self.__key = os.getenv(empresa + '_KEY')
        self.__secret = os.getenv(empresa + '_SECRET')

    def __converter_json(self, metodo):

        antigo = metodo.__dict__
        classe = metodo.__class__.__name__
        novo = {}

        for atributo in antigo:
            valor = antigo[atributo]
            atributo = atributo.replace("_" + classe + "__", "")
            atributo = atributo.replace("_" + classe + "_", "")
            atributo = atributo.replace("_" + classe, "") 
            novo[atributo] = valor     

        return novo