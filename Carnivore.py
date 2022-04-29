import random
import Gamedata
import Map
def create(position : tuple) -> dict:
    skin = "▲"
    return {"skin" : skin, 'position' : position, 'manger' : False}

def get_skin(creature : dict) -> str:
    assert type(creature) is dict
    return creature["skin"]

def get_position(creature : dict) -> bool:
    assert type(creature) is dict
    return creature["position"]

def get_manger(creature : dict) -> bool:
    assert type(creature) is dict
    return creature['manger']

def set_position(creature : dict, newposition) -> dict:
    """
    Return a dict with new position
    """
    creature['position'] = newposition
    return creature

def set_manger(creature : dict, etat : bool) -> dict :
    creature["manger"] = etat
    return creature 

def valid_move(gamedata: dict, allposition : list, newposition : tuple) -> dict:
    """
    Tells you if a move is possible or not
    """
    assert type(newposition) is tuple
    assert type(allposition) is list
    if newposition not in allposition and Map.isinmap(newposition, gamedata['carte']) :
        return True
    else:
        return False

def move(creature : dict, gamedata : dict, direction : str, allposition : list()) -> dict:
    """Move character"""
    actualposition = creature['position']

    if direction == 'Down':
        newposition = (actualposition[0], actualposition[1]+1)
        if valid_move(gamedata, allposition, newposition):
            return set_position(creature, newposition)
        else:
            return creature

    elif direction == 'Up':
        newposition = (actualposition[0], actualposition[1]-1)
        if valid_move(gamedata, allposition, newposition):
            return set_position(creature, newposition)
        else:
            return creature

    elif direction == "Left":
        newposition = (actualposition[0]-1, actualposition[1])
        if valid_move(gamedata, allposition, newposition):
            return set_position(creature, newposition)
        else:
            return creature
    
    elif direction == 'Right':
        newposition = (actualposition[0]+1, actualposition[1])
        if valid_move(gamedata, allposition, newposition):
            return set_position(creature, newposition)
        else:
            return creature
    else :
        print('error')
        assert 'pasdemove'

def can_reproduce(creature, gamedata, allposition) -> bool:
    """return True if there's room"""
    if Gamedata.count_nearby_entities(gamedata, creature, allposition) == 8:
        return False
    return True

def reproduce(creature, gamedata, allposition) -> dict:
    """place another Carnivore around"""
    position = creature['position']
    nearbyposition = Gamedata.get_allposition_nearby(gamedata, position)
    for i in nearbyposition:
        if i not in allposition and Map.isinmap(i, gamedata['carte']):
            gamedata = Gamedata.addCarnivore(gamedata, i)
            return gamedata

def caneat(creature, gamedata) -> bool:
    """return True if herbivore nearby""" 
    herbivorepos = Gamedata.get_herbivore_position(gamedata)
    if Gamedata.count_nearby_entities(gamedata, creature, herbivorepos) >= 1:
        return True
    return False

def eat(creature, gamedata) -> dict:
    """found herbivore nearby and pop it"""
    herbivores = Gamedata.get_herbivore(gamedata)
    for i in range(len(herbivores)):
        if Gamedata.distance(herbivores[i]['position'], creature['position']) == 1:
            gamedata = Gamedata.kill_herbivore(gamedata, i)
            return gamedata

def gotofood(creature, gamedata, allposition) -> tuple:
    herbivorepos = Gamedata.get_herbivore_position(gamedata)
    creaturepos = creature['position']
    closestherbivore = (Gamedata.distance(creaturepos, herbivorepos[0]), herbivorepos[0])
    for i in herbivorepos:
        distance = Gamedata.distance(creaturepos, i)
        if distance < closestherbivore[0]:
            closestherbivore = (distance,i)

    herbivorepos = closestherbivore[1]
    if creaturepos[0] != herbivorepos[0] and creaturepos[1] != herbivorepos[1]:
        i = random.randint(0,1)
        if i == 0:
            if herbivorepos[0] > creaturepos[0]:
                return move(creature, gamedata, "Right", allposition)
            else:
                return move(creature, gamedata, "Left", allposition)
        else :
            if herbivorepos[1] > creaturepos[1]:
                return move(creature, gamedata, "Down", allposition)
            else:
                return move(creature, gamedata, "Up", allposition)

    elif creaturepos[1] != herbivorepos[1]:
        if herbivorepos[1] > creaturepos[1]:
            return move(creature, gamedata, "Down", allposition)
        else:
            return move(creature, gamedata, "Up", allposition)

    elif creaturepos[0] != herbivorepos[0]:
        if herbivorepos[0] > creaturepos[0]:
            return move(creature, gamedata, "Right", allposition)
        else:
            return move(creature, gamedata, "Left", allposition)
    else:
        return creature
if __name__ == "__main__":
    gamedata = {
    'carte' : [[[] for i in range(0,10)] for y in range(0,10)], 
    'entities' : {
        'plante': [{'position' : (3,0)},{'position' : (3,4)}],
        'carnivores': [{'position' : (1,2)}],
        'herbivores': [{'position' : (5,2)}]}}
    creature = create((0,0),"?", 10)
    print(creature)
    creature, asmoved = move(creature,'Right',gamedata)
    print(creature)
    print(asmoved)


