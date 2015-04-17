#!/usr/bin/python3.4

import sqlite3
import model.tile

"""
TODO: currently, bob can ssh in and automagically start the game.
    That's his shell in /etc/passwd.  But, he needs a link to the game.db
    in family's home dir.  That's because most of the work is being done
    there.  Later, I'll have to move everything to some place else.
"""
db = "game.db"

"""
    CREATE TABLE world (uid text, ground text, def_symbol text,
        x integer, y integer)
"""
def save_world(world):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for coord in world.tiles.keys():
        tile = world.tiles[coord]
        # TODO: save the entities!!!
            # might not need to worry about this because the entity
            # will have it's current coord listed
        x, y = tile.coord
        c.execute("""UPDATE world SET
            ground='{grd}',
            def_symbol='{def_sym}',
            x={x},
            y={y}
            WHERE uid={uid}""".format(uid=tile.uid, grd=tile.ground,
                 def_sym=tile.default_symbol, x=x, y=y))

    conn.commit()
    conn.close()


def load_world():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    world = model.tile.World()
    for row in c.execute("SELECT * FROM world"):
        tile = model.tile.Tile()
        uid, ground, def_sym, x, y = row
        tile.uid = uid
        tile.ground = ground
        tile.default_symbol = def_sym
        tile.coord = (x, y)
        world.tiles[(x,y)] = tile
    conn.close()
    return world


def rebuild_entities_table(entities):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS entities")
    c.execute('''CREATE TABLE entities (name text, symbol text,
        cur_loc_x integer, cur_loc_y integer, hp integer,
        default_hp integer, vision_range integer)''')
    conn.commit()
    conn.close()
    # TODO: change these functions so that we try out the @ stuff to call
    # before calling the function... I forget what it's called :(
    for entity in entities:
        add_entity(entity)
    return True


"""
add_entity should be called when a new entity is created.  The info will
be INSERTed into the db.

    CREATE TABLE entities (name text, symbol text, cur_loc_x integer,
        cur_loc_y integer, hp integer, default_hp integer)
"""
def add_entity(bob):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    x, y = bob.cur_loc
    values = [bob.name, bob.symbol, x, y, bob.hp, bob.default_hp,
        bob.vision_range]
    ques = []
    for i in range(len(values)):
        ques.append("?")
    que_marks = ", ".join(ques)
    exec_string = "INSERT INTO entities VALUES ({})".format(que_marks)
    c.execute(exec_string, values)
    conn.commit()
    conn.close()


"""
This function will only update entity information.  Not add new entities
to the db.  We will be keying on the name of the entity.  In the future,
we should have a uid.
"""
def save_entities(entities):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for entity in entities:
        x, y = entity.cur_loc
        c.execute("""UPDATE entities SET
            symbol='{sym}',
            cur_loc_x={x},
            cur_loc_y={y},
            hp={hp},
            default_hp={def_hp},
            vision_range={vis_r}
            WHERE name='{name}'""".format(
            sym=entity.symbol, name=entity.name, x=x, y=y, hp=entity.hp,
            def_hp=entity.default_hp, vis_r=entity.vision_range))
    conn.commit()
    conn.close()


def load_entities(world):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    entities = []
    for row in c.execute("SELECT * FROM entities"):
        name, symbol, x, y, hp, default_hp, vis_r = row
        entity = model.tile.Entity()
        entity.name = name
        entity.symbol = symbol
        entity.cur_loc = (x, y)
        entity.cur_hp = hp
        entity.max_hp = default_hp
        entity.vision_range = vis_r
        entities.append(entity)
        world.tiles[(x, y)].entities.append(entity)
    conn.close()
    return entities


def drop_tables():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS world")
    c.execute("DROP TABLE IF EXISTS entities")
    conn.commit()
    conn.close()

def clean_tables():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("DELETE FROM world")
    c.execute("DELETE FROM entities")
    conn.commit()
    conn.close()

def setup_tables():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE world (uid text, ground text, def_symbol text,
        x integer, y integer)''')
    c.execute('''CREATE TABLE entities (name text, symbol text,
        cur_loc_x integer, cur_loc_y integer, hp integer,
        default_hp integer)''')
    conn.commit()
    conn.close()
    
        

if __name__ == "__main__":
    """
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE world (uid text, ground text, def_symbol text,
        x real, y real)''')
    c.execute("INSERT INTO world VALUES ('0', 'plain', '.', 0, 0)")
    conn.commit()
    conn.close()
    """
