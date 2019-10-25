"""
    Módulo responsável pelo gerenciamento da memoria 
"""


class Memoria():
    
    def __init__(self):

        self.tamanho_fixo_memoria = 1024
        self.tamanho_real_memoria = 64
        self.tamanho_memoria_usuario = self.tamanho_fixo_memoria - self.tamanho_real_memoria

        self.lista_blocos_kernel = [-1 for x in range (0, self.tamanho_real_memoria) ]  # -1 significa livre.
        self.lista_blocos_usuario = [-1 for x in range (0, self.tamanho_memoria_usuario) ]  # -1 significa livre.

        # armazena a quantidade de blocos livres.
        self.quantidade_blocos_kernel_livre = self.tamanho_real_memoria
        self.quantidade_blocos_usuario_livre = self.tamanho_memoria_usuario
        
        
    def verificar_disponibilidade_memoria(self, processo):
        """ retorna True se conseguir espaço livre para executar o processo."""

        disponibilidade = False

        # processo kernel
        if processo.prioridade == 0 : 
            disponibilidade = self.alocar_memoria_kernel(processo)

        # processo usuario
        else:                        
            disponibilidade = self.alocar_memoria_usuario(processo)
            
        return disponibilidade
        
    def alocar_memoria_kernel(self, processo):
        """ alocar espaço de kernel de usuario por um processo.""" 
        i = 0          
        while i < self.tamanho_real_memoria:
            
            if (self.lista_blocos_kernel[i] == -1):
                # se é vazio, começa a contar quantos tem e vê se o programa cabe.
                inicial = i
                espacos = 0
                while (i < self.tamanho_real_memoria and self.lista_blocos_kernel[i] == -1):
                    espacos += 1
                    i += 1 
                if (processo.bloco_memoria <= espacos):
                    processo.offset_memoria = inicial
                    for i in range(inicial, inicial + processo.bloco_memoria):
                        self.lista_blocos_kernel[i] = processo.pid
                    return True
            else:
                i += 1
                # se não é livre, só anda na lista de blocos.
            
        return False
    
    def alocar_memoria_usuario(self, processo):
        """ alocar espaço de memoria de usuario por um processo.""" 
        i = 0
        while i < self.tamanho_memoria_usuario:
            if (self.lista_blocos_usuario[i] == -1):
                inicial = i 
                espacos = 0 
                while(i < self.tamanho_memoria_usuario and self.lista_blocos_usuario[i] == -1):
                    espacos += 1
                    i += 1
                if(processo.bloco_memoria <= espacos):
                    processo.offset_memoria = inicial
                    for i in range(inicial, inicial + processo.bloco_memoria):
                        self.lista_blocos_usuario[i] = processo.pid          
                    return True
            else:
                i += 1
            
        return False
    
    def liberar_memoria_kernel(self, processo):
        """ libera a memoria do kernel utilizada por um processo quando ele termina sua execução.""" 
        for i in range(processo.offset_memoria, processo.offset_memoria + processo.bloco_memoria):
                self.lista_blocos_kernel[i] = -1
        
    def liberar_memoria_usuario(self, processo):
        """ libera a memoria do usuário utilizada por um processo quando ele termina sua execução.""" 
        for i in range(processo.offset_memoria, processo.offset_memoria + processo.bloco_memoria):
                self.lista_blocos_usuario[i] = -1        

    def liberar_memoria(self, processo):
        """ libera a memoria utilizada por um processo quando ele termina sua execução.""" 

        # processo kernel
        if (processo.prioridade == 0):
            self.liberar_memoria_kernel(processo)
        
        # processo usuario
        else:
            self.liberar_memoria_usuario(processo)

