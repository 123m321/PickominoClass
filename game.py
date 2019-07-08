#import config
#import player
#albert = player('Albert')
#boris = player('Boris')
#chris = player('Chris')
#players = [albert, boris, chris]
#from player import player
print ('this is game.py')

class game:
    # def __init__(self):
    #     self.thisgame = thisgame

    def work_with_int_and_string(self, decided):
        # humans only
        if decided.upper() != 'W':
            decided = int(decided)
        else:
            decided = decided.upper()
        return decided

    def print_flathand(self, hand, playerID, players):
        flat = []
        for key in hand:
            flat.append(str(key) * hand[key],)
        flat = ''.join(str(e) for e in flat)
        print(f'{players[playerID].name} throws ' + flat)

    def winner_count(self, list, players):
        for play in players:
            print(f'{play.name} won {list.count(play.name)} times')

    def find_tile(self, tiles, lastSCORE):
        while True:
            if lastSCORE in tiles:
                break
            lastSCORE = lastSCORE - 1
        return lastSCORE

    def possible_sides_to_pick(self, hand, FREE_SIDES):
        thrown_numbers = [key for key in hand if hand[key] > 0]
        return [x for x in thrown_numbers if x in FREE_SIDES]

    def FREE_SIDES_sum(self, free):
        if 'W' in free:
            free.remove('W')
            free.append(5.01)
            sum_free = sum(free)
            del free[-1]
            free.append('W')
        else:
            sum_free = sum(free)
        return sum_free
    
    def calculate_points(self, hand, pick_one):
        if pick_one != 'W':
            points = pick_one * hand[pick_one]
        elif pick_one == 'W':
            points = 5 * hand[pick_one]
        return points


    def found_the_W(self, FREE_SIDES_of_dice):
        if 'W' not in FREE_SIDES_of_dice:
            return True
        return False
    
    
    def stop_rolling_again_question(self):
        """This function asks if human user will throw again"""
        stop_or_not = input('Roll again? (y/n) .. ')
        if stop_or_not.upper() == "N":
            return False
        return True
    
    
    def survival_rate(self, FREE_SIDES, dice_left):
        free = len(FREE_SIDES)
        notfree = 6 - free
        notfreepower = notfree ** dice_left
        allsixsides = 6 ** dice_left
        deadrate = notfreepower / allsixsides
        return int(100 * (1 - deadrate))
    
    
    def worms_quantity(self, nr):
        if nr < 21:
            return 0
        if 25 > nr > 20:
            return 1
        if 29 > nr > 24:
            return 2
        if 33 > nr > 28:
            return 3
        if nr > 32:
            return 4
        
    def remove_last_tile(self, tiles):
        last_tiles = -1
        while True:
            if isinstance(tiles[last_tiles], int):
                tiles[last_tiles] = 'X'
                break
            else:
                last_tiles -= 1
        return tiles
    
    def SCORE_high(self, SCORE, min_tiles):
        if SCORE >= min_tiles:
            return True
        return False
    
    def minmax_tiles_calc(self, TILES):
        tiles_range = []
        tiles_range.append(min(n for n in TILES if isinstance(n, int)))
        return min(tiles_range), max(tiles_range)
    
    def give_back_tile(self, number, TILES):
        TILES.insert(0, number)
        TILES = [n for n in TILES if isinstance(n, int)]
        TILES.sort()
        TILES.append('X')
        return TILES
    
    
    def picked_sides(self, FREE_SIDES):
        taken = [1, 2, 3, 4, 5, 'W']
        picked = [e for e in taken if e not in FREE_SIDES]
        picked = ''.join(str(e) for e in picked)
        return picked
    
    def create_stealList(self, players):
        stealList = []
        for play in players:
            stealList.append(0)
        return stealList


    def update_stealList(self, players, stealList):
        nr_of_players_min1 = (len(players))
        for x in range(0, nr_of_players_min1):
            if players[x].own_tiles:
                stealList[x] = players[x].own_tiles[-1]
            else:
                stealList[x] = 0
        return stealList
    

    def new_nr_of_dice(sel, hand, pick):
        return sum(hand.values()) - hand[pick]
    
    def check_first_tiles_int(self, first_tile):
        if len(first_tile) < 1:
            print('tiles empty!')
            return True
        return isinstance(first_tile[0], int)

    def is_turn_over(self, NR_OF_DICE_left, FREE_SIDES_left):
        if NR_OF_DICE_left and FREE_SIDES_left:
            return False  # not dead, because dice left and sides left
        return True
    
    
    def reset_vars(self):
        NR_OF_DICE = 8
        FREE_SIDES = [1, 2, 3, 4, 5, 'W']
        SCORE = 0
        return NR_OF_DICE, FREE_SIDES, SCORE
    
    
