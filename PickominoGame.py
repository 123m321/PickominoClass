"""
The game of Pickomino, Regenwormen (NL) or Heckmeck (DE) is played with 8
dice and a lot of tiles.

"""
import random
import pandas as pd
import matplotlib.pyplot as plt
from game import game
from player import player



pl = player
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
stay_in_turn = True
turndict = {}

if __name__ == "__main__":
    albert = pl('Albert')
    boris = pl('Boris')
    chris = pl('Chris')
    albert.tactic = 1
    boris.tactic = 2
    print('Rules. Try to win most worms. Tiles on table have worms,\
  21 - 24 have 1 worm')
    print('25-28 2 worms, 29 - 32 : 3 worms and higher 4 worms.\n')
    print('Start with 8 dice, you need to pick a side to keep it apart.\
  \nYou need a worm too (worth 5 points) - the Worm replaced the 6 on the die')
    print('you can steal from other players, or grab from table. If you die,\
  you lose top of your stack')
    print('Check \
  https://frozenfractal.com/blog/2015/5/3/how-to-win-at-pickomino/ for\
  more details')
    players = [albert, boris, chris]
    stealList = gam.create_stealList(players)
#    number_of_games = int(input(f'Number of games? (For AI analysis) : '))
#    if pl.add_human():
#        chris.human = True
    number_of_games = 1

    for i in range(0, number_of_games):
        playerID = random.randint(0, 2)  # random start of player
        i += 1
        print(chris.human)       
        for singleplayers in players:
            singleplayers.own_tiles = []
        stealList = gam.create_stealList(players)  # rest stealList
        while gam.check_first_tiles_int(TILES):  # the main loop of the game
            while True:  # the loop of throwing dice and picking numbers
                fail = False  # at start of throwing, there is no fail yet

                #  dice are thrown here for first time - may put below in a 
                # function in game.py?
                thrown = players[playerID].throw_dice(NR_OF_DICE)
                hand = players[playerID].orden_dices_in_dict(thrown)
                gam.print_flathand(hand, playerID, players)

                # next step, pick a number if possible
                possible_sides = gam.possible_sides_to_pick(hand, FREE_SIDES)
                if possible_sides:
                    # dice are thrown, and able to pick a number (or R)
                    if not players[playerID].human:
                        if players[playerID].tactic == 1:
                            pick_one = players[playerID].auto_thief(hand, possible_sides, stealList, playerID, SCORE, FREE_SIDES)
                            print('player tactic 1.')
                        elif players[playerID].tactic == 2:
                            print ('player tactic 2')
                            pick_one = players[playerID].think_one_step_ahead(hand, possible_sides, FREE_SIDES, SCORE, playerID)
                        else:
                            print('player tactic 0')
                            pick_one = players[playerID].auto_mx_point(hand, possible_sides, players, playerID)  # max pick
                        FREE_SIDES.remove(pick_one)
                        NR_OF_DICE = gam.new_nr_of_dice(hand, pick_one)
                        points = gam.calculate_points(hand, pick_one)
                    else:
                        while True:
                            # routine for human question of picking a side
                            print(f'Possible choices : {possible_sides}')
                            pick_one = input(f'Which one will you pick? :')
                            pick_one = gam.work_with_int_and_string(pick_one)
                            if pick_one in gam.possible_sides_to_pick(hand, FREE_SIDES):  # valid choice
                                FREE_SIDES.remove(pick_one)
                                NR_OF_DICE = gam.new_nr_of_dice(hand, pick_one)
                                points = gam.calculate_points(hand, pick_one)
                                print(f'Points is {points}')
                                break
                            else:
                                print("Sorry, that isn't possible \n")
                else:
                    fail = True
                    break
    #  after throwing, and picking a side - calculate SCORE etc
                SCORE = players[playerID].calculate_SCORE(SCORE, points)
                if players[playerID].human:
                    print(f'SCORE is {SCORE}, dice left = {NR_OF_DICE},\
 picked sides = {gam.picked_sides(FREE_SIDES)} ')
                if gam.is_turn_over(NR_OF_DICE, FREE_SIDES):  # no dice/sides
                    # check here if SCORE is high enough
                    if gam.found_the_W(FREE_SIDES):
                        
                        if gam.SCORE_high(SCORE, gam.minmax_tiles_calc(TILES)[0]):
                            fail = False
                        elif pl.steal_possible(SCORE, stealList, playerID):
                            fail = False
                        else:
                            fail = True
                        break
                    print('no W found')
                    fail = True
                    break
                rfound = gam.found_the_W(FREE_SIDES)
                if rfound:
                    NR_OF_DICE = gam.new_nr_of_dice(hand, pick_one)
                    if gam.SCORE_high(SCORE, gam.minmax_tiles_calc(TILES)[0]) \
                        or pl.steal_possible(SCORE, stealList, playerID):
                        if not players[playerID].human:
                            print(f'player not human and stay {stay_in_turn}')
                            print(f'score is {SCORE}')
                            stay_in_turn = pl.strategy_thief(SCORE, stealList, playerID, NR_OF_DICE, FREE_SIDES)
                            print(f'nogmaals {stay_in_turn}')
                        else:
                            # keep rolling or stop for humans
                            stay_in_turn = gam.stop_rolling_again_question()
                    if stay_in_turn:
                        continue
                    else:
                        break
                continue

    # here doing the stuff after finishing the turn
            steal = False
            if not fail:
                if pl.steal_possible(SCORE, stealList, playerID):
                    print(f'succesful steal {SCORE} from\
 {players[stealList.index(SCORE)].name}\n')
                    steal = True
                    players[stealList.index(SCORE)].own_tiles.remove(SCORE)
                    players[playerID].own_tiles.append(SCORE)
                else:
                    tilenr = gam.find_tile(TILES, SCORE)
                    TILES.remove(tilenr)
                    players[playerID].own_tiles.append(tilenr)
                    gam.update_stealList(players, stealList)
                    print(f'{players[playerID].name} added {tilenr}\
 on top of his stack\n')

            else:
                print(f'{players[playerID].name} died.\n')
                TILES = gam.remove_last_tile(TILES)
                if players[playerID].own_tiles:
                    tileback = players[playerID].own_tiles.pop(-1)
                    TILES = gam.give_back_tile(tileback, TILES)
                    gam.update_stealList(players, stealList)
            print(f'Tiles on the table : {TILES}')
            for each_player in players:
                print(f'{each_player.name} : {each_player.own_tiles}')
            stay_in_turn = True
            if players[playerID].human:
                waiting_a_moment = input('<press any key>')
            stealList = gam.update_stealList(players, stealList)
#            Fill turn df
            if fail:
                SCORE = 0
            turndict = {turncol[0]: players[playerID].name, turncol[1]: fail,
                        turncol[2]: rfound, turncol[3]: gam.worms_quantity(SCORE),
                        turncol[4]: steal}
            df = df.append(turndict, ignore_index=True)
            playerID = pl.next_player(players, playerID)
            print(f'Next player will be {players[playerID].name} and his tiles\
 are {players[playerID].own_tiles}')
            NR_OF_DICE, FREE_SIDES, SCORE = gam.reset_vars()

        overallWinners.append(pl.most_worms(players))
        TILES, players[playerID].own_tiles, throw_number, turn_number,\
            winnaar = pl.reset_tiles()
        gam.winner_count(overallWinners, players)
        print('\n')
        bool_col = ['W_found', 'fail', 'steal']
        for bc in bool_col:
            df[bc] = df[bc].astype(bool)
        df.SCORE = df.SCORE.astype(int)
    df2 = df.groupby('playerID').mean()
    print(df2)
    fig, ax = plt.subplots(3, 1)
    ax[0].bar(df2.index, df2.steal)
    ax[0].set_ylabel('steal')
    ax[1].bar(df2.index, df2.fail)
    ax[1].set_ylabel('fail')
    ax[2].bar(df2.index, df2.SCORE)
    ax[2].set_ylabel('SCORE')
    ax[2].set_xlabel('player')
    plt.show()
