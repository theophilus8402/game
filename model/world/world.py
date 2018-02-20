
from math import sqrt,floor,ceil

from model.entity.basic_entity import Entity
from model.entity.armor import Armor
from model.entity.weapons import Weapon
from model.entity.living.living import Living
from model.entity.living.skills import SkillName
from model.entity.dead import DeathInfo,determine_who_gets_xp
from .input import handle_input,get_all_input
from model.map import Coord

class World:

    def __init__(self):
        self.tiles = {}
        self.basic_ents = {}
        self.weapon_ents = {}
        self.armour_ents = {}
        self.living_ents = {}
        self.spells = {}
        self.socket_entity_map = {}
        self.ai_entities = []
        self.actions = None
        self.server_socket = None

        # these max uids are the current highest uid
        # so, to create a new uid, return max_uid++
        self.max_tile_uid = 0
        self.max_ent_uid = 0

    def add_entity(self, entity):
        name = entity.name.lower()
        if isinstance(entity, Living):
            self.living_ents[name] = entity
        elif isinstance(entity, Armor):
            self.armor_ents[name] = entity
        elif isinstance(entity, Weapon):
            self.weapon_ents[name] = entity
        elif isinstance(entity, Entity):
            self.basic_ents[name] = entity
        else:
            print("Eep! Got a weird entity to add! {}".format(entity))

    def find_entity(self, name):
        name = name.lower()
        entity = self.living_ents.get(name)
        if not entity:
            entity = self.weapon_ents.get(name)
        if not entity:
            entity = self.armour_ents.get(name)
        if not entity:
            entity = self.basic_ents.get(name)
        return entity

    def action_search(self, searcher):
        search_result = searcher.skill_check(SkillName.perception)
        total = search_result.total
        found_entities = []
        for ent in self.living_ents.values():
            if ent.sneaking and total >= ent.sneaking:
                found_entities.append(ent)
        return search_result, found_entities

    def action_look(self, entity):
        # determines map to display to the user
        map_rows = self.map.get_map(entity.coords, 4)
        print("\n".join(map_rows))

    def action_hit(self, attacker, defender, full_hit=False):

        # determine if we're doing a two weapon attack
        # TODO: not gonna do this yet
        #attacker.roll_attack(full_hit=full_hit, main_hand=False)

        # get attack results
        mresults, oresults = attacker.roll_attack(full_hit=full_hit)

        # determine ac of defender
        # TODO: determine if defender is flat footed
        flat_footed = False
        ac = defender.ac.total if not flat_footed else defender.ac.flat_footed

        # roll dmg when appropriate
        final_results = []
        mlen = len(mresults)
        mresults.extend(oresults)
        for att_roll, i in zip(mresults, range(len(mresults))):
            if att_roll.total >= ac:
                main_hand = True if i < mlen else False
                dmg_info = attacker.roll_damage(main_hand=main_hand)
                # TODO: apply the dmg
                defender.apply_damage(attacker, dmg_info)
            else:
                dmg_info = None
            final_results.append((att_roll, dmg_info))

        # see if the defender died
        if defender.cur_hp <= 0:
            death_info = self.kill(defender)
        else:
            death_info = None

        return final_results, death_info

    def kill(self, dead_guy):
        # determine if his death should be permanent or if he can come back
        # non-permanent are simple animals/monsters
        # permanent, are NPCs that are pertanent to a story or quest?
        #   or PCs
        # TODO: permanent guys should have their "souls" put some where safe
        body_coords = dead_guy.coords
        if dead_guy.permanent:
            # put his normal body in different place to be resurrected later
            self.move_entity(dead_guy, Coord(-99, -99))

        # start gathering DeathInfo
        death_info = DeathInfo(dead_guy)

        # TODO: leave a body (and loot?) on the ground
        self.place_entity(death_info.body, body_coords)

        # add xp to the appropriate peeps
        # have each entity keep track of both bad and good things done to them
        # if an entity is killed, look through all of it's bads
        #   give xp to those guys, AND
        #   look through all those guys who have recently done good things
        #   to them... need a way to age things off
        attackers = determine_who_gets_xp(dead_guy)

        # divy up the xp equally
        xp_per_peep = floor(dead_guy.xp_to_give / max(len(attackers), 1))

        for peep in attackers:
            gained_level = peep.gain_xp(xp_per_peep)
            # TODO: if they gain a level, notify them!!!
        death_info.xp_per_attacker = xp_per_peep
        death_info.attackers = attackers

        return death_info

    def place_entity(self, entity, coords):
        # Doesn't do any checks what so ever
        # set's the entities coords to that location
        # TODO: tiles?
        entity.coords = coords
        self.map.add_symbol(entity.coords, entity.symbol)

    def remove_entity(self, entity):
        self.map.remove_symbol(entity.coords)
        entity.coords = None

    def move_entity(self, entity, coords):
        # doesn't do any checks
        # TODO: tiles?

        # removes the entity from it's original location
        self.remove_entity(entity)

        # places the entity in the new location
        self.place_entity(entity, coords)

    # handling user input
    handle_input = handle_input

    get_all_input = get_all_input


def distance_between(coord1, coord2):
    distance = sqrt((coord1.x - coord2.x)**2 + 
                    (coord1.y - coord2.y)**2)
    return ceil(distance)


def world_add_entity(world, entity):
    """
    Adds the entity to the world.  Adds the entity to the appropriate tile and the
    appropriate list of entities within the world.
    """
    tile = get_tile(world, entity.coord)
    tile_add_entity(tile, entity)
    input_handle = entity.comms.get_input_handle()
    world.socket_entity_map[input_handle] = entity
    if isinstance(entity, Living):
        #world.living_ents[entity.name.lower()] = entity
        area_entity_check(world, entity)
    else:
        #TODO: add the other types
        pass
