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
        existe_processo_prioridade_1 = False;
        existe_processo_prioridade_2 = False;

        for processo in lista_processo_pronto:      
          
            if processo.prioridade == 0:
                existe_processo_sistema = True
            
            elif processo.prioridade == 1:
                existe_processo_prioridade_1 = True 
            
            elif processo.prioridade == 2:
                existe_processo_prioridade_2 = True   
                    
        """
           Gerar as listas de todas as prioridades
        """
        for processo in lista_processo_pronto:          
              
            if processo.tempo_inicializacao <= tempo_execucao:
     
                if processo.prioridade == 0:
                    self.lista_prioridade_0.append(processo)
                    existe_processo_sistema = False
                    
                if existe_processo_sistema == False:
                    
                    if processo.prioridade == 1:
                        self.lista_prioridade_1.append(processo)
                        existe_processo_prioridade_1 = False 
                         
                    elif processo.prioridade == 2 and existe_processo_prioridade_1 == False:
                        self.lista_prioridade_2.append(processo)
                        existe_processo_prioridade_2 = False 
                        
                    elif processo.prioridade == 3 and existe_processo_prioridade_2 == False:
                        self.lista_prioridade_3.append(processo)

    def alterar_fila_prioridade_usuario(self, lista_processo_pronto, tempo_execucao):

        """
            EVITAR STARVATION
            Método responsável por alterar a prioridade dos processos  
            que estiverem mais de 10 unidades de tempo esperando 
            sem nunca terem sidos executados na fila de prioridade.
        """       

        existe_processo_prioridade_2 = False;

        for processo in lista_processo_pronto:      
            if processo.prioridade == 2:
                existe_processo_prioridade_2 = True   
    
        for processo in lista_processo_pronto:
            
            if processo.prioridade == 2 and not self.lista_prioridade_2:
               
                if processo.tempo_inicializacao + 10 <= tempo_execucao :
                    self.lista_prioridade_1.append(processo)
                
                elif processo.tempo_inicializacao + 20 < tempo_execucao:
                    self.lista_prioridade_1.append(processo)
        
            if processo.prioridade == 3 and not self.lista_prioridade_3 and existe_processo_prioridade_2 == False:
               
                if processo.tempo_inicializacao + 10 <= tempo_execucao:
                    self.lista_prioridade_2.append(processo)
                    
