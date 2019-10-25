


class Arquivo():

    def __init__(self, dic_processos_id, log_executados):
        self.quantidade_bloco_disco = None
        self.log_executados = log_executados
        self.dicionario_arquivos_existentes = dict()
        self.dicionario_processos = dic_processos_id
    
    def ler_arquivo_file(self, nome_arquivo_file):

        file = open(nome_arquivo_file) 
        self.quantidade_bloco_disco = [-1 for x in range(0, int(next(file)))]
        
        quantidade_segmentos_disco = (int(next(file)))

        for i in range(0, quantidade_segmentos_disco):
            nome_arquivo, primeiro_bloco_gravado, quantidade_blocos = next(file).split(',')
            
            primeiro_bloco_gravado = int(primeiro_bloco_gravado)
            quantidade_blocos = int(quantidade_blocos)

            self.dicionario_arquivos_existentes[nome_arquivo] = None 

            for i in range(primeiro_bloco_gravado, primeiro_bloco_gravado + quantidade_blocos):
                self.quantidade_bloco_disco[i] = nome_arquivo

        print(self.quantidade_bloco_disco)
        