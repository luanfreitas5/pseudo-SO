"""
    Módulo responsável pelo gerenciamento da processos 
"""

from moduloFilas import Fila
from moduloMemoria import Memoria
from moduloRecursos import Recurso
from moduloEntradaSaida import Impressao

    
class Processo():
    
    def __init__(self, processo, pid):
        
        """ FORMATO ENTRADA: 
            <tempo de inicialização>, <prioridade>, <tempo de processador>, <blocos em memória>, <número-
            código da impressora requisitada>, <requisição do scanner>, <requisição do modem>, <número-
            código do codigo_disco> 
        """

        self.tempo_inicializacao = processo[0]
        self.prioridade = processo[1]
        self.tempo_processador = processo[2]
        self.bloco_memoria = processo[3]
        self.codigo_impressora = processo[4]
        self.scanner = processo[5]
        self.modem = processo[6]
        self.codigo_disco = processo[7]
        self.pid = pid
        
        self.tempo_arquivo = processo[2]
        self.offset_memoria = None
        self.tempo_ultima_execucao = 0

    
class GerenciandorProcessos:
    
    def __init__(self):
        self.dicionario_processo_pid = {}
        self.dicionario_lista_processo_tempo_execucao = {}
        
    def verificar_tamanho_bloco(self, processo):
        if (processo.prioridade == 0 and processo.bloco_memoria > 64):
            return True 
        if (processo.prioridade == 1 and processo.bloco_memoria > 960):
            return True
        return False
    
    def ler_arquivo_processos(self, nome_arquivo_processo):
        
        pid = 0
        impressao = Impressao()
        
        with open(nome_arquivo_processo, "r") as arquivoProcesso:
            for linha in arquivoProcesso:
                processo = Processo([int(campo) for campo in linha.split(',')], pid)
 
                if (self.verificar_tamanho_bloco(processo)):
                    continue
                
                # Dicionario de processos
                self.dicionario_processo_pid[pid] = processo
                pid += 1
        
                # Dicionario de tempo de processos
                if (processo.tempo_inicializacao in  self.dicionario_lista_processo_tempo_execucao):
                    self.dicionario_lista_processo_tempo_execucao[processo.tempo_inicializacao].append(processo)
                else:
                    self.dicionario_lista_processo_tempo_execucao[processo.tempo_inicializacao] = [processo]
                
                impressao.imprimir_dispatcher(processo)
        
    def executar_processos(self):
   
        recurso = Recurso()    
        fila = Fila(self.dicionario_processo_pid)
        memoria = Memoria()
        dicionario_processos_executados = {}
        contador_tempo_inicializacao = 1
    
        while(True):
            self.verificar_processo_recurso_memoria_disponivel(recurso, fila, memoria, contador_tempo_inicializacao)
            
            print('Luan', contador_tempo_inicializacao, '\t', fila , 'UE: ', end='')
    
            # salva os processos executados.
            dicionario_processos_executados[contador_tempo_inicializacao] = fila.buscar_processo_executado()
    
            # executa o processo com mais prioridade.
            if fila.executa_processo() :
                recurso.liberar_recursos()
                memoria.liberar_memoria(fila.dicionario_processo_pid[fila.ultimo_executado])
    
            # print(fila.ultimo_executado)
            fila.aumenta_prioridade()
            
            contador_tempo_inicializacao += 1
            
            if(fila.contador_processos_finalizado == fila.quantidade_processos):
                break
    
            if(contador_tempo_inicializacao > 15):
                break

        print(contador_tempo_inicializacao, '\t', fila, 'UE:', fila.ultimo_executado)
        print(dicionario_processos_executados)
    
        return dicionario_processos_executados
    
    # verifica se existem items chegando na fila de prioridade.
    def verificar_processo_recurso_memoria_disponivel(self, recurso, fila, memoria, contador_tempo_inicializacao):
    
        if (contador_tempo_inicializacao in self.dicionario_lista_processo_tempo_execucao):
            lista_processos = self.dicionario_lista_processo_tempo_execucao[contador_tempo_inicializacao]
            
            # trata os itens que foram encontrados na fila de prioridade.
            for elemento_processo in lista_processos:
            
                # valida se possuem os moduloRecursos necessários disponíveis para ser executado.
                if (recurso.verificar_disponibilidade_recursos(elemento_processo) and memoria.verificar_disponibilidade_memoria(elemento_processo)):
                    fila.insere_processo_fila_prioridade(elemento_processo)
                
                else:
                    # Se o recurso não pode ser utilizado naquele momento, modifica o tempo inicial do
                    # processo e faz com que ele seja inicializado mais tarde.
                    elemento_processo.tempo_inicializacao += 1
                    
                    # Acresenta um elemento na lista ou cria chave de lista de processos
                    if ((contador_tempo_inicializacao + 1) in self.dicionario_lista_processo_tempo_execucao):
                        self.dicionario_lista_processo_tempo_execucao[contador_tempo_inicializacao + 1].append(elemento_processo)
                    else:
                        self.dicionario_lista_processo_tempo_execucao[contador_tempo_inicializacao + 1] = [elemento_processo]
    

