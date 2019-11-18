"""
    Módulo responsável pelo gerenciamento de processos.
    Classes e estruturas de dados relativas ao processo. 
    Basicamente, mantém informações específicas do processo.
"""
import sys
from moduloMemoria  import Memoria
from moduloArquivos import GerenciadorArquivos
from moduloRecursos import Recurso
from moduloFilas import Fila
from moduloEntradaSaida import LeitorArquivo, Impressao

TAMANHO_MAXIMO_PROCESSOS = 1000
TAMANHO_PROCESSO_REAL = 64
TAMANHO_PROCESSO_USUARIO = 960 


class Processo:
    """
        Classe responsável pelo carregamento de dados dos processos.
    """

    def __init__(self, processo):
        """
            Construtor da classe de Processo
        """
        self.tempo_inicializacao = processo[0]
        self.prioridade = processo[1]
        self.tempo_processador = processo[2]
        self.bloco_memoria = processo[3]
        self.codigo_impressora = processo[4]
        self.scanner = processo[5]
        self.modem = processo[6]
        self.codigo_disco = processo[7]
        self.pid = None
        self.lista_instrucoes = []
        self.posicao_bloco_disco = 0

    def setar_instrucao(self, lista_instrucoes):
        """
            Metódo responsável por receber uma de operações
            e fazer referência ao processo corrente
        """
        for linha in lista_instrucoes:
            instrucao = linha.split(',')
            if self.pid == int(instrucao[0]):
                # codigo de operação = 0 criar  ou  1 deletar
                if int(instrucao[1]) == 0:
                    self.lista_instrucoes.append([int(instrucao[0]), int(instrucao[1]), instrucao[2].strip(" "), int(instrucao[3]), int(instrucao[4]) ])
                else:
                    self.lista_instrucoes.append([int(instrucao[0]), int(instrucao[1]), instrucao[2].strip(" "), int(instrucao[3])])


class GerenciadorProcessos:
    
    """
        Classe responsável por manipulação de processos, executar_operacao de processos,
        adicionar/remover/alterar/ordenar processos na fila de prioridade e
        verificar disponibilidade de recursos e memoria.
    """

    def __init__(self):
        """
            Construtor da classe de GerenciadorProcessos
        """
        self.quantidade_processo = 0
        self.fila = Fila()
        self.memoria = Memoria()
        self.recurso = Recurso()
        self.impressao = Impressao()
        self.leitor_arquivo = LeitorArquivo()
        self.gerenciador_arquivo = None
        self.lista_processo_usuario_execucao = []
        self.lista_processo_sistema_execucao = []
        self.lista_processo_pronto = []

    def verificar_tamanho_processo(self):
 
        """
            Verifica se todos os processos requisitam moduloMemoria sem extrapolar o valor
            máximo que eles podem assumir, ou seja, 64 para processos de tempo real e
            960 para processos de Usuario. Se requisitarem a mais eles são excluidos.
        """
        lista_processo_analisados = []
    
        for processo in self.lista_processo_pronto:       
            if (processo.bloco_memoria > TAMANHO_PROCESSO_REAL) and (processo.prioridade == 0):
                pass
            
            elif (processo.bloco_memoria > TAMANHO_PROCESSO_USUARIO) and (processo.prioridade != 0):
                pass
            
            else:        
                lista_processo_analisados.append(processo)
       
        self.lista_processo_pronto = lista_processo_analisados
        self.quantidade_processo = len(lista_processo_analisados)
       
    def carregar_arquivos(self):
        """
            Responsavel por realizar leitura dos arquivos de entrada
        """
        argtam = len(sys.argv)

        arquivo_processo = ""
        arquivo_file = ""
        
        if argtam > 2:

            arquivo_processo = sys.argv[1]
            arquivo_file = sys.argv[2]

        else:
            arquivo_processo = "processes_0.txt"
            arquivo_file = "files_0.txt"
        
        # Abre o arquivo para leitura e gera um lista de processos.
        self.lista_processo_pronto = self.leitor_arquivo.leitura_arquivo_processos(arquivo_processo)
        
        [lista_arquivos, lista_operacoes] = self.leitor_arquivo.leitura_arquivo_file(arquivo_file)
        
        self.gerenciador_arquivo = GerenciadorArquivos(lista_arquivos)
        
        for processo in self.lista_processo_pronto:
            processo.setar_instrucao(lista_operacoes)
    
    def executar_fila_processo_pronto(self):
        """
            Responsável por executar_operacao do gerenciador de processos.
        """
        quantidade_processo_usuario_executado = 0
        quantidade_processo_sistema_excutado = 0   
        tempo_execucao = 1;
        
        while(True):
            self.lista_processo_usuario_execucao = []
            self.lista_processo_sistema_execucao = []
            
            self.fila.inicializar_fila()
        
            # Ordena a fila de prioridade dos processos tem como prioridade maior os processos de sistema
            self.fila.ordenar_filas_prioridade(self.lista_processo_pronto, tempo_execucao)
         
            # Altera prioridade dos processos que estão esperando muito para serem executado na fila de prioridade de usuário.
            self.fila.alterar_fila_prioridade_usuario(self.lista_processo_pronto, tempo_execucao)
           
            # Adiciona os processos na fila de processos de real e de usuario
           
            if len(self.fila.lista_prioridade_0) > 0:
                self.memoria.verificar_disponibilidade_memoria_real(self.fila.lista_prioridade_0, self.lista_processo_sistema_execucao)   
            
            if len(self.fila.lista_prioridade_1) > 0:
                self.memoria.verificar_disponibilidade_memoria_recurso_usuario(self.fila.lista_prioridade_1, self.lista_processo_usuario_execucao, self.recurso)   
            if len(self.fila.lista_prioridade_2) > 0:
                self.memoria.verificar_disponibilidade_memoria_recurso_usuario(self.fila.lista_prioridade_2, self.lista_processo_usuario_execucao, self.recurso)    
            
            if len(self.fila.lista_prioridade_3) > 0:
                self.memoria.verificar_disponibilidade_memoria_recurso_usuario(self.fila.lista_prioridade_3, self.lista_processo_usuario_execucao, self.recurso)   
            
            if len(self.lista_processo_sistema_execucao) > 0 :
                quantidade_processo_sistema_excutado += self.executar_operacao_processo(self.lista_processo_sistema_execucao)
            
            if len(self.lista_processo_usuario_execucao) > 0:
                quantidade_processo_usuario_executado += self.executar_operacao_processo(self.lista_processo_usuario_execucao)
            
            # Limpa a memoria de usuario
            self.memoria.liberar_memoria_usuario()
            
            # Libera os drivers que foram alocados
            self.recurso.liberar_recursos()
            
            # Aumenta o tempo de execução
            tempo_execucao += 1
            
            if(self.quantidade_processo == (quantidade_processo_sistema_excutado + quantidade_processo_usuario_executado)):
                break
            
            if((quantidade_processo_sistema_excutado + quantidade_processo_usuario_executado) >= TAMANHO_MAXIMO_PROCESSOS):
                break

    def executar_operacao_processo(self, lista_processo_execucao):
        """
            Responsável por executar_operacao processos de tempo-real
        """
        quantidade_processo_executado = 0
        contador = 0
        
        for processo in lista_processo_execucao:  
            quantidade_processo_executado += 1
            sequencia_execucao = 0
            
            self.impressao.imprimir_dispatcher(processo)
            self.impressao.log_operacao.clear()
            
            print("\nProcesso {}\n".format(processo.pid))
            print("P{} STARTED\n".format(processo.pid))
            for instrucao in processo.lista_instrucoes:
              
                if sequencia_execucao <= len(instrucao):
                   
                    if sequencia_execucao >= processo.tempo_processador:
                        numero_operacao_processo = processo.lista_instrucoes[sequencia_execucao][4]
                        mensagem = "P{} instruction {}".format(processo.pid, numero_operacao_processo)
                        mensagem += " - Falha!\n"
                        mensagem += "O processo {} esgotou o seu tempo de CPU!\n".format(processo.pid)
                        self.impressao.log_operacao.append(mensagem)
                    else: 
                        instrucao = processo.lista_instrucoes[sequencia_execucao][1]
                       
                        # verificar precisa executar a CPU, conforme a especificação
                        if instrucao == 0:  # criar arquivo
                            numero_operacao_processo = processo.lista_instrucoes[sequencia_execucao][4]
                            
                            if numero_operacao_processo != sequencia_execucao + contador:
                                contador = 1
                                mensagem_cpu = "P{} instruction {}".format(processo.pid, sequencia_execucao)
                                mensagem_cpu += " - Sucesso CPU!\n"
                                self.impressao.log_operacao.append(mensagem_cpu)
                                
                        else:  # deletar arquivo
                            numero_operacao_processo = processo.lista_instrucoes[sequencia_execucao][3]
                           
                            if numero_operacao_processo != sequencia_execucao + contador:
                                contador = 1
                                mensagem_cpu = "P{} instruction {}".format(processo.pid, sequencia_execucao)
                                mensagem_cpu += " - Sucesso CPU!\n"   
                                self.impressao.log_operacao.append(mensagem_cpu) 
                      
                        resultado = self.gerenciador_arquivo.executar_operacao(processo, sequencia_execucao)
                        self.impressao.log_operacao.append(resultado) 
            
                sequencia_execucao += 1
            
            if not processo.lista_instrucoes:
                contador = 1
                for contador in range(processo.tempo_processador):
                    mensagem_cpu = "P{} instruction {}".format(processo.pid, contador)
                    mensagem_cpu += " - Sucesso CPU!\n"
                    self.impressao.log_operacao.append(mensagem_cpu)
            
            self.impressao.imprimir_log()
            self.lista_processo_pronto.remove(processo)
            print("P{} return SIGINT".format(processo.pid))
            self.memoria.liberar_memoria_sistema(processo)
            self.impressao.imprimir_mapa_disco(self.gerenciador_arquivo) 
        return quantidade_processo_executado

