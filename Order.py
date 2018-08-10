class Order:
    def __init__(self, name, flavor, ice="Normal", sugar="Normal"):
        self.name = name
        self.flavor = flavor
        self.ice = ice
        self.sugar = sugar
        
    def __repr__(self):
        return (f"{self.__class__.__name__}({self.name}, {self.flavor},"
                f" {self.ice} ice, {self.sugar} sugar)")
                
    def __str__(self):
        return (f"{self.name} - {self.flavor}\n")
                
        
class OrderQueue:
    def __init__(self):
        self.queue = []
    
    def __repr__(self):
        string = ""
        for order in self.queue:
            string = string + order
        return string
    
    def __str__(self):
        return (f"{len(self.queue)} orders"}
    
    def add_order(self, order):
        self.queue.append(order)
      
    def work_order(self):
        if self.queue:
            return self.queue.pop([0])
        return None

        

        
# Doesn't need to be an OrderQueue class since there will only be 1.
def add_order(self, order):
    self.queue.append(order)
  
def work_order(self):
    if self.queue:
        return self.queue.pop([0])
    return None

    
