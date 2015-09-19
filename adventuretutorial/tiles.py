import items
import enemies
import actions
import world

__author__ = 'dalton'


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        moves.append(actions.ViewInventory())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()

        return moves


class StartingRoom(MapTile):
    def intro_text(self):
        return """
            You find yourself in a cave with a flickering torch on the wall.
            You can make out four paths, each equally dark and foreboding.
            """

    def modify_player(self, player):
        # Room has no action on player
        pass


class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, player):
        #  Checks to see if the items name is equal to Gold
        if self.item.__class__.__name__ == 'Gold':
            player.inventory[0].value += items.Gold(5).value
        else:
            player.inventory.append(self.item)

    def modify_player(self, player):
            self.add_loot(player)


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
            Another unremarkable part of the cave. You must forge onwards.
            """

    def modify_player(self, player):
        # Room has no action on player
        pass


class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
                    A giant spider jumps down from its web in front of you.
                    """
        else:
            return """
                    The corpse of a dead spider rots on the ground.
                    """


class SnakePitRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Snake())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
                You fall into a pit with a snake. Kill it and use it as a rope to get out.
                """
        else:
            return """
                You see a snake carcass on the ground
                """


class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())

    def intro_text(self):
        return """
            You notice something shiny in the corner.
            It's a dagger! You pick it up.
                """


class Find5GoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Gold(5))

    def intro_text(self):
        return """
        You see that the floor is littered with coins!
        You pick them up.
        """


class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
            You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!


        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True