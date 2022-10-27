
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

# class PlayerCharacter(InstantiatedCharacter):
#     def __init__():
#         pass

class InstantiatedCharacter():
    def __init__(self, tupple):
        self.id = tupple[0]
        self.base_id = tupple[1]
        self.base_name = tupple[2]
        self.owner = tupple[3]
        self.name = tupple[4]
        self.named = tupple[5]
        self.series = tupple[6]
        self.rarity = tupple[7]
        self.type = tupple[8]
        self.level = tupple[9]
        self.exp = tupple[10]
        self.max_health = tupple[11]
        self.max_mana = tupple[12]
        self.armor = tupple[13]
        self.attack = tupple[14]
        self.image = tupple[15]

class User():
    def __init__(self, tupple):
        self.id = tupple[0]
        self.discord_id = tupple[1]
        self.stamina = tupple[2]
        self.roll_currency = tupple[3]
        self.normal_currency = tupple[4]

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