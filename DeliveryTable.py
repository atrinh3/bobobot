# Delivery
# Assume table is 27"D
# Can fit at least 4 drinks per "slice"

# Create assignable positions
class DeliverySlice:
    interal_positions = 4
    
    def __init__(self, overall_position):
        self.position = overall_position
        self.occupied = False
        self.internal = [False] * internal_positions
    
    def ready_delivery(drinks):
        self.occupied = True
        for i in range(0, drinks):
            self.internal[i] = True;
    
    def delivery_taken():
        self.occupied = False
        self.internal = [False] * internal_positions
        
        
class DeliveryTable:
    available_positions = 5
    
    def __init__(self):
        s = Slice(0)
        for i in range(1, available_positions):
            s = s.append(Slice(i))
        self.slices = s
        
    
