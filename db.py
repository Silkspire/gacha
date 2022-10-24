import sqlite3
import atexit

db = 'database.db'
conn = sqlite3.connect(db)
print(conn.execute("SELECT name FROM keys LIMIT 1").fetchone()[0])


def get_discord_token():
    return conn.execute("SELECT key FROM keys WHERE name = ?", ('discord',)).fetchone()[0]



def close_database():
    conn.close()
    print(">>>>>>>>>SUCCESSFULLY CLOSED DATABASE")




#db.instantiate_character(base_character_id, owner_id)

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

def get_base_character(id):
    return BaseCharacter(conn.execute("SELECT * FROM base_characters WHERE id = ?", (id,)).fetchone()[0])


def get_instantiated_character(id):
    pass#TODO

def check_user(discord_id):
    try:
        user = conn.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,)).fetchone()[0]
        return
    except:
        print("user doesn't exist")
        add_user(discord_id)
        return False

def user_exists(discord_id):
    try:
        user = conn.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,)).fetchone()[0]
        repr(user)
        return True
    except:
        print("user doesn't exist")
        return False

def add_user(discord_id):
    conn.execute("""INSERT INTO users (discord_id) VALUES (?)""", (discord_id,))


def instantiate_character(owner_id, base_character_id):
    base_character = get_base_character(base_character_id)

    conn.execute("""INSERT INTO characters_instances 
    (base_id, base_name, owner, series, rarity, max_health, max_mana, armor, attack, image) VALUES 
    (?,?,?,?,?,?,?,?,?,?)""", 
    ('asd',))