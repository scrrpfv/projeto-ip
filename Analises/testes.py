class Dados:
    def __init__(self):
        self.dados = [1, 2, 3]
        self.proj = Projection(self.dados)
      
      
class Projection:
    def __init__(self, data):
        self.dados = data
        
        
    def make_projection(self, index):
        print(self.dados[index])
    	
    
dado = Dados()
dado.proj.make_projection(2)