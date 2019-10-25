
from moduloProcessos import GerenciandorProcessos
from moduloArquivos import Arquivo

if __name__ == "__main__":              

    print('Inicio\n')
    print('Processos\n')
    
    nome_arquivo_processo = "processes.txt"
    gerenciandorProcessos = GerenciandorProcessos()
    gerenciandorProcessos.ler_arquivo_processos(nome_arquivo_processo)
    
    print(gerenciandorProcessos.dicionario_lista_processo_tempo_execucao)
    
    dicionario_processos_executados = gerenciandorProcessos.executar_processos()
    
    nome_arquivo_file = "files.txt"
    
    arquivo = Arquivo(gerenciandorProcessos.dicionario_processo_pid, dicionario_processos_executados)
    arquivo.ler_arquivo_file(nome_arquivo_file)
   
    print('fim\n')
