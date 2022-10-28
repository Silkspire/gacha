import db

class User():
    def __init__(self, tupple):
        self.id = tupple[0]
        self.discord_id = tupple[1]
        self.stamina = tupple[2]
        self.roll_currency = tupple[3]
        self.normal_currency = tupple[4]
        self.founder = tupple[5]
        self.premium = tupple[6]
        self.selected_character = tupple[7]
    def spend_roll_currency(self, number):
        db.spend_roll_currency(self.id, number)
    def switch_selected_character(self, id):
        db.set_selected_character(self.id, id)