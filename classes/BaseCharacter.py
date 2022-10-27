class BaseCharacter():
    def __init__(self, tupple):
        self.id = tupple[0]
        self.name = tupple[1]
        self.type = tupple[2]
        self.series = tupple[3]
        self.rarity = tupple[4]
        self.max_health = tupple[5]
        self.max_mana = tupple[6]
        self.armor = tupple[7]
        self.attack = tupple[8]
        self.image = tupple[9]