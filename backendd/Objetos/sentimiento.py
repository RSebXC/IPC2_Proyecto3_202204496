class sentimientos:
    def __init__(self,positivo=0,negativo=0,neutro=0):
        self.positivo = positivo
        self.negativo = negativo
        self.neutro = neutro
    
    def plus_positivo(self):
        self.positivo += 1

    def plus_negativo(self):
        self.negativo += 1

    def plus_neutro(self):
        self.neutro += 1
    
    def reset(self):
        self.positivo = 0
        self.negativo = 0
        self.neutro = 0