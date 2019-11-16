"""
    Módulo responsável pelo gerenciamento das filas.
    Mantém as interfaces e funções que operam sobre os processos.
"""


class Fila:

    def __init__(self):

        self.lista_prioridade_0 = []
        self.lista_prioridade_1 = []
        self.lista_prioridade_2 = []
        self.lista_prioridade_3 = []
    
    def inicializar_fila(self):
        self.lista_prioridade_0 = []
        self.lista_prioridade_1 = []
        self.lista_prioridade_2 = []
        self.lista_prioridade_3 = []
             
    def ordenar_filas_prioridade(self, lista_processo_pronto, tempo_execucao):
        """
            Método responsável por ordenar os processos processos 
            na fila de prioridade, em ordem crescente de menor para maior.     
        """
       
        """
           Verificar que lista de processo pronto existe algum processo de sistema 
        """
        existe_processo_sistema = False;
        for processo in lista_processo_pronto:      
            if processo.prioridade == 0:
                existe_processo_sistema = True
                    
        """
           Gerar as listas de todas as prioridadea 
        """
        for processo in lista_processo_pronto:          
              
            if processo.tempo_inicializacao <= tempo_execucao:
                
                if processo.prioridade == 0:
                    self.lista_prioridade_0.append(processo)
                    existe_processo_sistema = False
                    
                if existe_processo_sistema == False:
                    if processo.prioridade == 1:
                        self.lista_prioridade_1.append(processo)
                         
                    elif processo.prioridade == 2:
                        self.lista_prioridade_2.append(processo)
                        
                    elif processo.prioridade == 3:
                        self.lista_prioridade_3.append(processo)

    def alterar_fila_prioridade_usuario(self, tempo_execucao):
        """
            EVITAR STARVATION
            Método responsável por alterar a prioridade dos processos  
            que estiverem mais de 10 unidades de tempo esperando 
            sem nunca terem sidos executados na fila de prioridade.
        """       
        for processo in self.lista_prioridade_2:
          
            if((processo.tempo_inicializacao + 9 < tempo_execucao) and (not processo.lista_prioridade)):
                processo.lista_prioridade = True
                self.lista_prioridade_1.append(processo)
            elif((processo.tempo_inicializacao + 19 < tempo_execucao) and (processo.lista_prioridade)):
                self.lista_prioridade_1.append(processo)
       
        for processo in self.lista_prioridade_3:
            if((processo.tempo_inicializacao + 9 < tempo_execucao) and (not processo.lista_prioridade)):
                processo.lista_prioridade = True 
                self.lista_prioridade_2.append(processo)
   
