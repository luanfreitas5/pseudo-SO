"""
    Módulo responsável pelo gerenciamento da filas 
"""

from moduloMemoria import Memoria


class Fila():

    def __init__(self, dicionario_processo_pid):

        self.lista_fila_prioridade = [[], [], [], []] 
        self.dicionario_processo_pid = dicionario_processo_pid
        self.memoria = Memoria()
        self.ultimo_executado = None
        self.quantidade_processos = len(dicionario_processo_pid)
        self.aging = 5  # tecnica de envelhecimento.
        self.contador_processos_finalizado = 0

    def insere_processo_fila_prioridade(self, processo) :
        # # insere um processo de acordo com sua prioridade na lista 
        """verifico aqui se há espaço para ser executado ou na hora de executar? """
        prioridade = processo.prioridade
        if (prioridade == 0):
            self.lista_fila_prioridade[0].append(processo.pid)
        elif (prioridade == 1):
            self.lista_fila_prioridade[1].append(processo.pid)
        elif (prioridade == 2):
            self.lista_fila_prioridade[2].append(processo.pid)
        elif (prioridade == 3):
            self.lista_fila_prioridade[3].append(processo.pid)
            
    def buscar_processo_executado(self):
        set_processo_executado = set()
        for lista_pid in self.lista_fila_prioridade:
            for pid in lista_pid:
                set_processo_executado.add(pid)

        return set_processo_executado if len(set_processo_executado) > 0 else set([None])
    
    def remove_processo(self, indice_lista_fila_prioridade):
        # # remove  um processo de acordo com sua fila
        self.lista_fila_prioridade[indice_lista_fila_prioridade] = self.lista_fila_prioridade[indice_lista_fila_prioridade][1:]

    def executa_processo(self):
        """ verifica qual é o processoa  ser executado.
            e executa o mesmo.
            se acabar o tempo, apaga ele da fila.
        """

        self.ultimo_executado = None   
        for i in range(0, 4):
            if (len(self.lista_fila_prioridade[i]) > 0):
                executado = self.executa_processo_selecionado(self.lista_fila_prioridade[i][0] , i)
                return executado
            
        return False

    def executa_processo_selecionado(self, pid , indice_lista_fila_prioridade):
        """retorna true se um processo acabou. Falso se não. """
        self.ultimo_executado = pid

        processo = self.dicionario_processo_pid[pid]
        if (processo.tempo_processador > 0):
            processo.tempo_processador -= 1
            
        if (processo.tempo_processador == 0) :
            self.contador_processos_finalizado += 1
            self.remove_processo(indice_lista_fila_prioridade)
            return True 
        
        return False

    def aumenta_prioridade(self):
        
        for fila in self.lista_fila_prioridade:
            for processo_pid in fila:
                processo = self.dicionario_processo_pid[processo_pid]
                if (processo_pid != self.ultimo_executado):
                    
                    processo.tempo_ultima_execucao += 1

                    # se tiver passado de 10 sem executar aumenta em 1 a prioridade.
                    if (processo.tempo_ultima_execucao >= self.aging and processo.prioridade > 1):
                            prioridade = processo.prioridade 

                            # remove o processo_pid da fila antiga
                            self.lista_fila_prioridade[prioridade] = [x for x in self.lista_fila_prioridade[prioridade] if x != processo_pid]
                            processo.prioridade -= 1
                            self.insere_processo(processo)
                            processo.tempo_ultima_execucao = 0
                else:
                    processo.tempo_ultima_execucao = 0
                    
                    