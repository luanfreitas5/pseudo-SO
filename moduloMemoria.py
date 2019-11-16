"""
    Módulo responsável pelo gerenciamento da memoria.
    Provê uma interface de abstração de memória RAM
"""

TAMANHO_PROCESSO_REAL = 64
TAMANHO_PROCESSO_USUARIO = 960


class Memoria:
    """
        Classe responsável por alocação e remoção de processos na memória.
    """

    def __init__(self):
        """
            Construtor da classe Memoria.
        """
        self.memoria = [None for _ in range(0, TAMANHO_PROCESSO_REAL + TAMANHO_PROCESSO_USUARIO)]

    def verificar_disponibilidade_memoria_real(self, lista_prioridade_0, lista_processo_sistema_execucao):
        """
            Responsável por verificar disponibilidade de memoria real nos 64 MB reservados
            aos processos de tempo real.
        """
       
        for processo_real in lista_prioridade_0:  
                if self.verificar_dispobilidade_memoria(processo_real):
                    lista_processo_sistema_execucao.append(processo_real)
          
    def verificar_disponibilidade_memoria_recurso_usuario(self, lista_prioridade, lista_processo_usuario_execucao, recurso):
        """
            Responsável por verificar disponibilidade memoria de usuário de 960 MB
        """
      
        for processo_usuario in lista_prioridade:
            if(recurso.verificar_disponibilidade_recurso(processo_usuario)):
                if self.verificar_dispobilidade_memoria(processo_usuario):
                    lista_processo_usuario_execucao.append(processo_usuario)
    
    def verificar_dispobilidade_memoria(self, processo):
        """
            Método responsável verificar a dispobilidade de memória.
            Se tiver dispobilidade aloca o processo na posição indicada na memória e retorna True,
            se não tiver dispobilidade retornar False.
        """
        dispobilidade = 0
        if processo.prioridade == 0:
            inicio = 0
            fim = TAMANHO_PROCESSO_REAL
        else:
            inicio = TAMANHO_PROCESSO_REAL
            fim = TAMANHO_PROCESSO_REAL + TAMANHO_PROCESSO_USUARIO
        for i in range(inicio, fim):
            if self.memoria[i] == None:
                dispobilidade += 1
                if dispobilidade == processo.bloco_memoria:
                    processo.posicao_bloco_disco = i - processo.bloco_memoria + 1
                    self.memoria[processo.posicao_bloco_disco:processo.posicao_bloco_disco + dispobilidade] = dispobilidade * [processo.pid]
                    return True
            else:
                dispobilidade = 0
        return False

    def liberar_memoria_sistema(self, processo):
        """
            Metodo responsável por deletar o processo referenciado
        """ 
        self.memoria[processo.posicao_bloco_disco:processo.posicao_bloco_disco + processo.bloco_memoria] = [None] * processo.bloco_memoria

    def liberar_memoria_usuario(self):
        """
            Metodo responsável por limpar a memoria de usuario 
        """
        self.memoria[TAMANHO_PROCESSO_REAL:] = TAMANHO_PROCESSO_USUARIO * [None]

