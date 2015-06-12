#!/usr/bin/python3.4

import model.entity
import control.db.entity

if __name__ == "__main__":

    shoe = model.entity.Entity()
    shoe.type = "entity"
    shoe.uid = 20
    shoe.name = "shoe"
    shoe.symbol = "*"
    shoe.cur_loc = (1, 3)
    shoe.cur_hp = 10
    shoe.max_hp = 10
    shoe.short_desc = "This is an old shoe."
    shoe.long_desc = "This is a really old shoe. It's floppy."
    shoe.weight = 1
    shoe.volume = .5
    shoe.friction = .1
    temp_entities = {}
    temp_entities[shoe.name] = shoe

    entities = control.db.entity.load_entities("pent.txt")
    control.db.entity.save_all_entities(entities, "2pent.txt")
