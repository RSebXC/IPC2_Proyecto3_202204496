class hashtag:
    def __init__(self,nombre,menciones=1):
        self.nombre = nombre
        self.menciones = menciones
    
    def plus_menciones(self):
        self.menciones += 1