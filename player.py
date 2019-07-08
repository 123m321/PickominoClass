import random
import pandas as pd
from game import game
print('this is player')
gam = game()
NR_OF_DICE = 8
FREE_SIDES = [1, 2, 3, 4, 5, 'W']
SCORE = 0
TILES = [x for x in range(21, 36)]
TILESoriginal = [x for x in range(21, 36)]
WORMS = [1]*4 + [2] * 4 + [3] * 4 + [4] * 4
TILES.append('X')
throw_number = 1
turn_number = 1
turncol = ['playerID', 'fail', 'W_found', 'SCORE', 'steal']
df = pd.DataFrame(columns=turncol)
playerID = 0
overallWinners = []
#stay_in_turn = True
turndict = {}

class player:
    """
    This is my first class I ever used. It's made to create players,
    and currently there are 3 of them. Each with a slightly different 
    strategy.
    """
    def __init__(self, playername):
        self.name = playername
        self.human = False
        self.own_tiles = []
        self.tactic = 0

    def throw_dice(self, NR_OF_DICE):
        """
        Method to throw a number of dice. Only throw as many dice as
        you have left
        """
        self.thrown_dice = []
        for x in range(NR_OF_DICE):
            self.thrown_dice.append(random.randint(1, 6))
        return self.thrown_dice

    def orden_dices_in_dict(self, dicelist):
        """
        The dice thrown are ordered in a dictionary : hand
        """
        self.hand = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 'W': 0}
        for keys in self.hand:
            self.hand[keys] = dicelist.count(keys)
            self.hand['W'] = dicelist.count(6)
        return self.hand

    def calculate_SCORE(self, SCORE, points):
        """
        after throwing dice, and ordering in them, pick a value
        and calculate the new subtotal of thrown numbers : the score
        """
        self.SCORE = SCORE + points
        return self.SCORE

    def auto_mx_point(self, hand, possible_sides, players, playerID):
        mx_pick = []
        for pos_sides in possible_sides:
            mx_pick.append(hand[pos_sides] * pos_sides)
        if isinstance(mx_pick[-1], str):
            worms = mx_pick[-1].count('W')
            del mx_pick[-1]
            mx_pick.append(worms * 5)
        mx = max(mx_pick)
        mx_index = mx_pick.index(mx)
        print(f'{players[playerID].name} picks {possible_sides[mx_index]}\
 (score now {SCORE + mx})')
        return possible_sides[mx_index]

    def auto_thief(self, hand, possible_sides, stealList, playerID, SCORE, FREE_SIDES):
        mx_pick = []
        steal_opp = False
        steal_others = stealList[:]
        del steal_others[playerID]
        for pos_sides in possible_sides:
            mx_pick.append(hand[pos_sides] * pos_sides)
        if isinstance(mx_pick[-1], str):
            worms = mx_pick[-1].count('W')
            del mx_pick[-1]
            mx_pick.append(worms * 5)
        for steal in steal_others:
            for pick in mx_pick:
                if SCORE + pick == steal:
                    print('yes! steal possible')
                    mx = pick
                    mx_index = mx_pick.index(pick)
                    steal_opp = True
        if not gam.found_the_W(FREE_SIDES):
            steal_opp = False
        if not steal_opp:
            pick_one = players[playerID].think_one_step_ahead(hand, possible_sides, FREE_SIDES, SCORE, playerID)
            return pick_one
        print(f'{players[playerID].name} picks autothief {possible_sides[mx_index]},\
 score now {SCORE+mx}')
        return possible_sides[mx_index]

    def think_one_step_ahead(self, hand, possible_sides, FREE_SIDES, SCORE, playerID):
        mx_pick = []
        for pos_sides in possible_sides:
            mx_pick.append(hand[pos_sides] * pos_sides)
        if isinstance(mx_pick[-1], str):
            worms = mx_pick[-1].count('W')
            del mx_pick[-1]
            mx_pick.append(worms * 5)
        FREE_SIDES2 = FREE_SIDES[:]
        bothsteps = []
        for t in possible_sides:
            step1SCORE = mx_pick[possible_sides.index(t)] + SCORE
            FREE_SIDES2.remove(t)
            dice_left = gam.new_nr_of_dice(hand, t)
            FREE_SIDES2_sum = gam.FREE_SIDES_sum(FREE_SIDES2)
            step2SCORE = dice_left * (FREE_SIDES2_sum / 6)
            FREE_SIDES2.append(t)
            bothsteps.append(step1SCORE + step2SCORE)
        maxstep = max(bothsteps)
        print(f'{players[playerID].name} picks 1stepahead\
 {possible_sides[bothsteps.index(maxstep)]}\
 (score now {SCORE + mx_pick[bothsteps.index(maxstep)]})')
        return possible_sides[bothsteps.index(maxstep)]
    
    def add_human():
        add_human = input('A human player joining? (y/n)  ')
        if add_human.upper() == 'Y':
            return True

    def next_player(players, playerID):
        playerID += 1
        if playerID == len(players):
            playerID = 0
        return playerID


    def pay_off_worms(FREE_SIDES, dice_left, SCORE, playerID):
        avg = int(dice_left) * (gam.FREE_SIDES_sum(FREE_SIDES) / 6)
        top_of_stack = 0
        print(f'name in payoff is {players[playerID].name}')
        print(f'top of stack = {players[playerID].own_tiles}')
        if players[playerID].own_tiles:
            top_of_stack = players[playerID].own_tiles[-1]
        print(f'now {players[playerID].name} would \
 win {gam.worms_quantity(SCORE)} worms with {SCORE} points')
        extra_worms = gam.worms_quantity(SCORE+avg) - gam.worms_quantity(SCORE)
        print(f'if he throws again he expects to gain {extra_worms} extra worms with {avg}')
        print(f'but if he loses, he loses {gam.worms_quantity(top_of_stack)} worms')
    
        extra_worms_odds = (gam.survival_rate(FREE_SIDES, dice_left) / 100) * extra_worms
        lose_worms_odds = gam.worms_quantity(top_of_stack) * 0.01 * (1 - gam.survival_rate(FREE_SIDES, dice_left))
        print(f'sum is {extra_worms_odds + lose_worms_odds}')
        return extra_worms_odds + lose_worms_odds


    def most_worms(players):
        # calculate most worms
        total_worms = []
        for playerID in players:
            ownWorms = []
            for tile in playerID.own_tiles:
                spot = gam.worms_quantity(tile)
                ownWorms.append(spot)
            print(f'Worms {playerID.name} = {sum(ownWorms)}')
            total_worms.append(sum(ownWorms))
        winner = (total_worms.index(max(total_worms)))
    # check draw
        if total_worms.count(max(total_worms)) > 1:
            print('draw in worms')
            draw = []
            for play1 in players:
                draw.append(sum(play1.own_tiles))
            winner = draw.index(max(draw))
        print(f'{players[winner].name} is the winner')
        return players[winner].name
    
    
    def steal_possible(SCORE, stealList, playerID):
        print(f'{SCORE} in steal possible')
        if SCORE in stealList:
            if stealList.index(SCORE) != playerID:
                print(stealList, SCORE)
                return True
        return False
    
    
    def strategy_thief(SCORE, stealList, playerID, NR_OF_DICE, FREE_SIDES):
        print(f'strategy thief tiles : {players[playerID].own_tiles}')
        print(f'strategy thief name : {players[playerID].name}')
        print(f'tactic = {players[playerID].tactic}')
        if player.steal_possible(SCORE, stealList, playerID):
            print('going to steal!')
            return False
        exp_result = player.pay_off_worms(FREE_SIDES, NR_OF_DICE, SCORE, playerID)
        print(f'strategy thief name2 : {players[playerID].name}')
        if exp_result > 0:
            return True
        return False

    def reset_tiles():
        TILES = [x for x in range(21, 36)]
        TILES.append('X')
        players[playerID].own_tiles = []
        throw_number = 1
        turn_number = 1
        winnaar = ""
        return TILES, players[playerID].own_tiles,\
            throw_number, turn_number, winnaar
    
albert = player('Albert')
boris = player('Boris')
chris = player('Chris')
players = [albert, boris, chris]