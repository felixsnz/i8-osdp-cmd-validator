

class Singleton:
    _instance = None
    

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'inicializado'):
            self.inicializado = True


            # Inicializar variables aquí
            self.baud_rate = None
            self.today_str = None
            
       
            