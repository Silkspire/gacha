from classes.Monster import *

class Enemy(Monster):
    def __init__(self, tupple):
        super().__init__(tupple)
        self.hp = self.max_health
        self.mana = self.max_mana
    def damage(self, amount):
        self.hp -= amount
        return amount