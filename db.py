import sqlite3
import atexit
import classes

db = 'database.db'
conn = sqlite3.connect(db)
print(conn.execute("SELECT name FROM keys LIMIT 1").fetchone()[0])


def get_discord_token():
    return conn.execute("SELECT key FROM keys WHERE name = ?", ('discord',)).fetchone()[0]


def close_database():
    conn.close()
    print(">>>>>>>>>SUCCESSFULLY CLOSED DATABASE")




#db.instantiate_character(base_character_id, owner_id)





def check_user(discord_id):
    #try:
    user = classes.User(conn.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,)).fetchone())
    #print(conn.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id,)).fetchone())
    print(str(user.discord_id))
    return user
    # except:
    #     print("user doesn't exist")
    #     add_user(discord_id)
    #     return False

def add_user(discord_id):
    conn.execute("INSERT INTO users (discord_id) VALUES (?)", (discord_id,))
    conn.commit()


def get_base_character(id):
    return classes.BaseCharacter(conn.execute("SELECT * FROM base_characters WHERE id = ?", (id,)).fetchone())


def get_instantiated_character(id):
    pass#TODO


def instantiate_character(owner_id, base_character_id):
    base = get_base_character(base_character_id)

    conn.execute(
    """INSERT INTO character_instances 
    (base_id, base_name, owner, series, rarity, max_health, max_mana, armor, attack, image) 
    VALUES (?,?,?,?,?,?,?,?,?,?)""", 
    (base.id, base.name, owner_id, base.series, base.rarity, base.max_health, base.max_mana, base.armor, base.attack, base.image,))
    conn.commit()

    print("Instantiated character")

def clear_all():
    conn.execute("DELETE FROM users")
    conn.execute("DELETE FROM character_instances")
    conn.commit()

# insert base character
# INSERT INTO base_characters (name, series, rarity, max_health, max_mana, armor, attack, image) VALUES ("Creation #1", 1, "Common", 100, 100, 5, 15, "img/characters/tmp_mdtvdek.png");