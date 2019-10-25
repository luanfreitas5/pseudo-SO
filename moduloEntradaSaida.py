"""
    Módulo responsável pelos métodos de exibição de dados na tela
"""


class Impressao:
    
    """
        Classe dos métodos de impressao de dados
    """

    def __init__(self):
        pass

    """
        Imprime a mensagem do dispatcher do referido processo
    """

    def imprimir_dispatcher(self, processo):
        print('dispatcher =>')
        print('\tPID:\t\t {}'.format(processo.pid))
        print('\toffset:\t\t {}'.format(processo.offset_memoria))
        print('\tblocks:\t\t {}'.format(processo.bloco_memoria))
        print('\tpriority:\t {}'.format(processo.prioridade))
        print('\ttime:\t\t {}'.format(processo.tempo_processador))
        print('\tprinters:\t {}'.format(bool(processo.codigo_impressora)))
        print('\tscanner:\t {}'.format(bool(processo.scanner)))
        print('\tmodem:\t\t {}'.format(bool(processo.modem)))
        print('\tdrives:\t\t {}'.format(bool(processo.codigo_disco)))

