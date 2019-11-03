"""
    Módulo responsável pelo gerenciamento da memoria.
    Provê uma interface de abstração de memória RAM.
"""

TAMANHO_PROCESSO_REAL = 64
TAMANHO_PROCESSO_USUARIO = 960


class Memoria:
    """
        Classe responsável por alocação e remoção de processos na memoria.
    """

    def __init__(self):
        """
            Construtor da classe de Memoria
        """
        self.memoria = [None for _ in range(0, TAMANHO_PROCESSO_REAL + TAMANHO_PROCESSO_USUARIO)]

    def verificar_disponibilidade_memoria_real(self, fila):
        """
            Responsável por verificar disponibilidade memoria real de 64 MB
        """
        lista_fila_espera = []
        for processo_real in fila.lista_processo_0 :
            if self.verificar_dispobilidade_memoria(processo_real):
                fila.lista_processo_sistema_execucao.append(processo_real)
            else:
                lista_fila_espera.append(processo_real)
        return lista_fila_espera
       
    def verificar_disponibilidade_memoria_usuario(self, fila, tipo_lista):
        """
            Responsável por verificar disponibilidade memoria de usuário de 960 MB
        """
        lista_processo_usuario = None
        if tipo_lista == 1:
            lista_processo_usuario = fila.lista_processo_1
        elif tipo_lista == 2:
            lista_processo_usuario = fila.lista_processo_2
        else:
            lista_processo_usuario = fila.lista_processo_3
            
        lista_fila_espera = []
        for processo_usuario in lista_processo_usuario:
          
            if self.verificar_dispobilidade_memoria(processo_usuario):
                fila.lista_processo_usuario_execucao.append(processo_usuario)
            else:
                lista_fila_espera.append(processo_usuario)
        return lista_fila_espera
    
    def verificar_dispobilidade_memoria(self, processo):
        """
            Metodo responsável verificar a dispobilidade de memoria em disco
            se tiver dispobilidade aloca o processo na posição indicada na memoria e retorna True 
            se não tiver dispobilidade retornar false
        """
        dispobilidade = 0
        if (processo.prioridade == 0):
            inicio = 0
            fim = TAMANHO_PROCESSO_REAL
        else:
            inicio = TAMANHO_PROCESSO_REAL
            fim = TAMANHO_PROCESSO_REAL + TAMANHO_PROCESSO_USUARIO
        for i in range(inicio, fim):
            if(self.memoria[i] == None):
                dispobilidade += 1
                if(dispobilidade == processo.bloco_memoria):
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
    
