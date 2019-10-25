"""
    Módulo responsável pelo gerenciamento da memoria 
"""


class Recurso():

    def __init__(self):
        """
            1 scanner
            2 impressoras
            1 modem
            2 dispositivos SATA
        """

        self.scanner = False
        self.impressora1 = False
        self.impressora2 = False
        self.modem = False
        self.dispositivo_sata1 = False
        self.dispositivo_sata2 = False

    def __repr__(self):

        return (""" scanner  => %s , impressora1 => %s, impressora2 => %s, modem => %s, dispositivo_sata1 => %s, dispositivo_sata2 => %s""") % (
            self.scanner, self.impressora1, self.impressora2, self.modem, self.dispositivo_sata1, self.dispositivo_sata2)
        
    def verificar_disponibilidade_recursos(self, processo):
        """retorna Falso se já estiverem utilizando algusn dos recursos necessários. """
        # condições que não podem ocorrer.
        scanner = ((self.scanner == True) and (processo.scanner == 1))
        impressora1 = ((self.impressora1 == True) and processo.codigo_impressora == 1)
        impressora2 = ((self.impressora2 == True) and processo.codigo_impressora == 2)
        modem = ((self.modem == True) and processo.modem == 1)
        dispositivo_sata1 = ((self.dispositivo_sata1 == True) and processo.codigo_disco == 1)
        dispositivo_sata2 = ((self.dispositivo_sata2 == True) and processo.codigo_disco == 2)
        
        condicoes = [scanner, impressora1, impressora2, modem, dispositivo_sata1, dispositivo_sata2]

        """ se algum dos dispositivos que não podem ser utilizados já está sendo
            retorna falso"""
        if any(condicoes):
            return False

        # salva qual dispositivo deve ser utilizado.
        if not scanner:
            self.scanner = (processo.scanner == 1)
        if not impressora1:
            self.impressora1 = processo.codigo_impressora == 1
        if not impressora2:
            self.impressora2 = processo.codigo_impressora == 2
        if not modem:
            self.modem = processo.modem == 1
        if not dispositivo_sata1:
            self.dispositivo_sata1 = processo.codigo_disco == 1
        if not dispositivo_sata2:
            self.dispositivo_sata2 = processo.codigo_disco == 2
        
        return True
    
    def liberar_recursos(self):
        """ libera os recursos.""" 

        self.impressora1 = False
        self.impressora2 = False
        self.scanner = False
        self.dispositivo_sata1 = False
        self.dispositivo_sata2 = False
        self.modem = False

        
class GerenciadorRecursos:
    """ 
    
    """

    def __init__(self):
        pass

