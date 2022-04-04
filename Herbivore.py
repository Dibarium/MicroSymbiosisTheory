import random
import Gamedata

def create(position : tuple, skin : str, r_action : int) -> dict:
    skin = "?"
    return {"skin" : skin, 'position' : position, 'r_action' : r_action, 'manger' : False}

def get_skin(creature : dict) -> str:
    assert type(creature) is dict
    return creature["skin"]

def get_r_action(creature : dict) -> int:
    assert type(creature) is dict
    return creature["r_action"]

def get_position(creature : dict) -> bool:
    assert type(creature) is dict
    return creature["position"]

def get_manger(creature : dict) -> bool:
    assert type(creature) is dict
    return creature['manger']


def set_skin(creature : dict, newskin : str) -> dict:
    assert type(creature) is dict
    assert type(newskin) is str
    creature['skin'] = newskin
    return creature

def set_position(creature : dict, newposition) -> dict:
    """
    Return a dict with new position
    """
    creature['position'] = newposition
    return creature

def set_manger(creature : dict, etat : bool) -> dict :
    creature["manger"] = etat
    return creature

def placement(gamedata : dict) -> tuple:
    assert type(gamedata) is dict

    maplength = (len(gamedata['carte'][0]), len(gamedata['carte']))
    allpos = Gamedata.get_allposition(gamedata)
    goodposition = False
    while goodposition != True:
        newposition = (random.randint(0, maplength[0]), random.randint(0, maplength[1]))
        if newposition not in allpos:
            goodposition = True
            return newposition

def isinmap(newposition : tuple, carte : list) -> bool:
    """
    Tells you if the position is inside the map
    """
    assert type(newposition) is tuple
    assert type(carte) is list
    lenghtmap = (len(carte[0]), len(carte))
    if newposition[0] >= 0 and newposition[0] <= lenghtmap[0] and newposition[1] >= 0 and newposition[1] <= lenghtmap[1] :
        return True
    else: 
        return False 

def valid_move(creature : dict, allposition : list, newposition : tuple) -> dict:
    """
    Tells you if a move is possible or not
    """
    assert type(newposition) is tuple
    assert type(allposition) is list
    assert type(creature) is dict
    if newposition not in allposition and isinmap(newposition, gamedata['carte']) :
        return True
    else:
        return False

def move(creature : dict, direction : str, gamedata : dict) -> dict:
    actualposition = creature['position']
    allposition = get_allposition(gamedata)

    if direction == 'Down':
        newposition = (actualposition[0], actualposition[1]+1)
        if valid_move(creature, allposition, newposition):
            return set_position(creature, newposition), True
        else:
            return creature, False

    elif direction == 'Up':
        newposition = (actualposition[0], actualposition[1]-1)
        if valid_move(creature, allposition, newposition):
            return set_position(creature, newposition), True
        else:
            return creature, False

    elif direction == "Left":
        newposition = (actualposition[0]-1, actualposition[1])
        if valid_move(creature, allposition, newposition):
            return set_position(creature, newposition), True
        else:
            return creature, False
    
    elif direction == 'Right':
        newposition = (actualposition[0]+1, actualposition[1])
        if valid_move(creature, allposition, newposition):
            return set_position(creature, newposition), True
        else:
            return creature, False
    else :
        print('error')
        assert 'pasdemove'

def can_reproduce(creature, gamedata, allposition):
    c = 0
    for i in allposition:
        if Gamedata.distance(creature['position'], i) == 1:
            c += 1
    if c == 8:
        return False
    return True

def reproduce(creature, gamedata, allposition):
    position = creature['position']
    nearby = Gamedata.get_allposition_nearby(gamedata, position)
    for i in nearby:
        if i not in allposition:
            Gamedata.addHerbivore(gamedata, i, "?", 10)


def show(creature):
    pass

if __name__ == "__main__":
    gamedata = {
    'carte' : [[[] for i in range(0,10)] for y in range(0,10)], 
    'entities' : {
        'plantes': [{'position' : (2,0)},{'position' : (3,4)}],
        'carnivores': [{'position' : (1,2)}],
        'herbivores': [{'position' : (5,2)}]}}
    creature = create((0,0),"?", 10)
    print(creature)
    creature, asmoved = move(creature,'Right',gamedata)
    print(creature)
    print(asmoved)

