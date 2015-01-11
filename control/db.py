#!/usr/bin/python3.4

import sqlite3
import model.tile

db = "game.db"

def save_world(world):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for coord in world.keys():
        tile = world[coord]
        # TODO: save the entities!!!
        x, y = tile.coord
        c.execute("INSERT INTO world VALUES (?, ?, ?, ?, ?)",
            (tile.uid, tile.ground, tile.default_symbol, x, y))

    conn.commit()
    conn.close()


def load_world():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    world = {}
    for row in c.execute("SELECT * FROM world"):
        tile = model.tile.Tile()
        uid, ground, def_sym, x, y = row
        tile.uid = uid
        tile.ground = ground
        tile.default_symbol = def_sym
        tile.coord = (x, y)
        # don't forget about the entities!
        world[(x,y)] = tile
        #print(row)
    conn.close()
    return world


def save_entities(entities):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for entity in entities:
        x, y = entity.cur_loc
        c.execute("INSERT INTO entities VALUES (?, ?, ?, ?, ?, ?)",
            (entity.symbol, entity.name, x, y, entity.hp,
            entity.default_hp))
    conn.commit()
    conn.close()


def load_entities():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    entities = []
    for row in c.execute("SELECT * FROM entities"):
        entity = model.tile.Entity()
        symbol, name, x, y, hp, default_hp = row
        entity.symbol = symbol
        entity.name = name
        entity.cur_loc = (x, y)
        entity.hp = hp
        entity.default_hp = default_hp
        entities.append(entity)
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

    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE world (uid text, ground text, def_symbol text,
        x real, y real)''')
    c.execute("INSERT INTO world VALUES ('0', 'plain', '.', 0, 0)")
    conn.commit()
    conn.close()
