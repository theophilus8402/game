
from .base_input import input_map

def input_attack(self, attacker, input_str):
    # input_str could be:
    #   "hit bob"
    #   "fullhit bob"
    #   "fh bob"

    # find the victim
    pieces = input_str.split()
    if len(pieces) >= 2:
        victim_name = pieces[1]
    else:
        print("Huh?")
        return False

    victim = self.find_entity(victim_name)
    if not victim:
        print("I don't know who {} is!".format(victim_name))
        return False

    # determine if it's supposed to be a full hit
    hit_str = pieces[0]
    full_hit = False
    if hit_str in {"fullhit", "fh"}:
        full_hit = True

    # determine if attacker can attack
    # TODO

    # determine if attacker and defender are close enough
    # TODO

    # attack!
    results,death_info = self.action_hit(attacker, victim, full_hit=full_hit)

    # display results
    print(results)
    print(death_info)

input_map["hit"] = input_attack
input_map["fullhit"] = input_attack
input_map["fh"] = input_attack

