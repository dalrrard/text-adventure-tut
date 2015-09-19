__author__ = 'dalton'

import world
from player import Player

visited = []

def play():
    world.load_tiles()
    player = Player()
    room = world.tile_exists(player.location_x, player.location_y)
    print(room.intro_text())
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        if (room in visited) and ('LootRoom' in str(room.__class__.__bases__)):
            pass
        else:
            visited.append(room)
            room.modify_player(player)
        #  check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:
            print('Choose an action:\n')
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            action_input = input('Action: ')
            print('\n')
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break

if __name__ == '__main__':
    play()