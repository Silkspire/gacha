class Monster():
    def __init__(self, tupple):
        self.id = tupple[0]
        self.name = tupple[1]
        self.type = tupple[2]
        self.series = tupple[3]
        self.rarity = tupple[4]
        self.difficulty = tupple[5]
        self.max_health = tupple[6]
        self.max_mana = tupple[7]
        self.armor = tupple[8]
        self.attack = tupple[9]
        self.image = tupple[10]