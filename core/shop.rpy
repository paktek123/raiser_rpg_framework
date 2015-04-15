##############################################################################
# SKILL DEFINITIONS
#

init -1 python:
    
    class ShopItem:
        def __init__(self, name, price, role='heal', health=0, chakra=0, quantity=0):
            self.name = name
            self.price = price
            self.role = role
            self.quantity = quantity
            self.health = health
            self.chakra = chakra
            
        def consume(self, player):
            if player.has_item(self) and player.get_item(self).quantity > 0:
                self.quantity -= 1
            else:
                return None
            
            if self.health and self.chakra:
                player.increase_hp(self.health)
                player.increase_chakra(self.chakra)
                return
                
            if self.health:
                player.increase_hp(self.health)
            elif self.chakra:
                player.increase_chakra(self.chakra)
                
        def half_price(self):
            self.price = self.price / 2
            
            return self
            
        def double_price(self):
            self.price = self.price * 2
            
            return self
                
        def __repr__(self):
            return "<Item: {} {} {}>".format(self.name, self.price, self.quantity)
            
    class Shop:
        def __init__(self, name, background, keeper=None, items=[]):
            self.name = name
            self.items = items
            self.discount = 0
            self.keeper = keeper
            self.background = background
            self.price_halved = False
            
        def half_prices(self):
            self.price_halved = True
            for item in self.items:
                item.half_price()
                
        def double_prices(self):
            self.price_halved = False
            for item in self.items:
                item.double_price()