
"""
    Módulo de inicialiazação do pseudoSO
"""

from moduloProcessos import GerenciadorProcessos

if __name__ == '__main__':
    print('Inicio\n')
    try:
        gerenciador_processos = GerenciadorProcessos()
        gerenciador_processos.carregar_arquivos()
        gerenciador_processos.verificar_tamanho_processo()
        gerenciador_processos.executar_fila_processo_pronto()
    except Exception as e:
        print ("Programa foi abortado  : %s" % e) 
    print('Fim\n')
