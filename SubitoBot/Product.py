
class Product:
    def __init__(self, id, link, price):
        self.id = id
        self.link = link
        self.price = price

    def get_id(self):
        return self.id
    
    def get_link(self):
        return self.link
    
    def get_price(self):
        return self.price
    
    def equals(self, product) -> bool: 
        return isinstance(product, Product) and self.get_id() == product.get_id()

    def compare(self, product) -> bool: 
        '''returns True if product that calls the function has higher price or is equalt to the other, otherwise returns False'''
        return self.get_price() >= product.get_price()
    
    def to_string(self) -> str:
        return f'{self.get_id()} {self.get_link()} {self.get_price()}\n'