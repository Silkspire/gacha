import sqlite3
import atexit
from classes.BaseCharacter import *
from classes.Enemy import *
from classes.GameState import *
from classes.InstantiatedCharacter import *
from classes.Monster import *
from classes.Player import *
from classes.User import *

db = 'database.db'
conn = sqlite3.connect(db)


def get_discord_token():
    return conn.execute("SELECT key FROM keys WHERE name = ?", ('discord',)).fetchone()[0]


def close_database():
    conn.close()
    print(">>>>>>>>>SUCCESSFULLY CLOSED DATABASE")




#db.instantiate_character(base_character_id, owner_id)





def get_user(discord_id):
    try:
        user = User(conn.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,)).fetchone())
        return user
    except:
        print("user doesn't exist")
        user = add_user(discord_id)
        return user

def add_user(discord_id):
    conn.execute("INSERT INTO users (discord_id) VALUES (?)", (discord_id,))
    conn.commit()
    return User(
        conn.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,)).fetchone())

def get_roll_currency(id):
    return conn.execute("SELECT roll_currency FROM users WHERE id = ?", (id,)).fetchone()[0]
    
def set_roll_currency(id, number):
    conn.execute("UPDATE users SET roll_currency = ? WHERE id = ?", (number,id))
    conn.commit()

def get_selected_character(id):
    # replace with nested SELECT statement
    char_id = conn.execute("SELECT selected_character FROM users WHERE id=?", (id,)).fetchone()[0]
    #ic = get_instantiated_character(char_id)
    ic = conn.execute("SELECT * FROM character_instances WHERE id = ?", (char_id,)).fetchone()
    return ic

def set_selected_character(user_id, char_id):
    conn.execute("UPDATE users SET selected_character = ? WHERE id = ?",
    (char_id, user_id,))
    conn.commit()

def get_base_character(id):
    return BaseCharacter(
        conn.execute("SELECT * FROM base_characters WHERE id = ?", (id,)).fetchone())

def get_instantiated_character(id):
    return InstantiatedCharacter(
        conn.execute("SELECT * FROM character_instances WHERE id = ?", (id,)).fetchone())

def get_owned_characters(owner_id):
    return conn.execute("SELECT id, base_name FROM character_instances WHERE owner = ?", (owner_id,)).fetchall()

def get_monster(difficulty):
    return conn.execute("SELECT * FROM monsters WHERE difficulty = ? ORDER BY RANDOM() LIMIT 1", (difficulty,)).fetchone()

def instantiate_character(owner_id, base_character_id):
    base = get_base_character(base_character_id)

    conn.execute(
    """INSERT INTO character_instances 
    (base_id, base_name, owner, series, rarity, max_health, max_mana, armor, attack, image) 
    VALUES (?,?,?,?,?,?,?,?,?,?)""", 
    (base.id, base.name, owner_id, base.series, base.rarity, base.max_health, base.max_mana, base.armor, base.attack, base.image,))
    conn.commit()

    print(f"Instantiated character {base.name} to user {owner_id}")

def gacha_character(owner_id, number):
    gacha_list = []
    for n in range(number):
        gacha = conn.execute("SELECT id FROM base_characters ORDER BY RANDOM() LIMIT 1").fetchone()[0]
        gacha_list.append(gacha)
    for id in gacha_list:
        instantiate_character(owner_id, id)
    return gacha_list

def reset():
    conn.execute("DELETE FROM users")
    conn.execute("DELETE FROM character_instances")
    conn.commit()

# insert base character
# INSERT INTO base_characters (name, series, rarity, max_health, max_mana, armor, attack, image) VALUES ("Creation #1", 1, "Common", 100, 100, 5, 15, "img/characters/tmp_mdtvdek.png");
# INSERT INTO monsters (name, series, rarity, difficulty, max_health, max_mana, armor, attack, image) VALUES ("Monster #1", 1, "Common", "easy", 75, 25, 0, 7, "img/monsters/1.png");