"""Pickleball Tournament
12 teams 6 courts, 11 rounds
2 pickleball courts
1 dink court
1 left handed court
1 swim noodle court
1 one-bounce court

Each team should play 3-4 rounds PB
 1 or 2 rounds each of the other games"""

import random
import time
from itertools import combinations

start = time.time()
POPN = 20000
population = []


class Team(object):
    def __init__(self, num):
        self.num = num
        # count game types
        self.types = dict()
        self.types['trad'] = 0
        self.types['dink'] = 0
        self.types['lefty'] = 0
        self.types['noodle'] = 0
        self.types['one_bounce'] = 0
        # list of opponents
        self.opponents = []
        self.score = 0

    def assign(self, opponent, type):
        self.opponents.append(opponent.num+1)
        self.types[type] += 1

    def repeats(self):
        output = 0
        for opp in range(1,13):
            if self.opponents.count(opp) > 1:
                output += 1
        return output


class Tournament(object):
    def __init__(self, numteams, rounds):
        self.numteams = numteams
        self.n_rounds = rounds
        self.teams = [Team(i) for i in range(numteams)]
        self.error = 0
        self.rounds = []
        self.mutated = 0
        self.generated = False

    def generate_rounds(self):

        for j in range(self.n_rounds):
            #get random numbers to be matchups every round
            nums = random.sample(range(self.numteams), self.numteams)
            #pair them up
            round1 = [[self.teams[nums[2 * i]].num, self.teams[nums[2 * i + 1]].num] for i in
                      range(int(self.numteams / 2))]

            self.rounds.append(round1)

    def assign_games(self):
        # assign game to teams
        for r in self.rounds:
            for i, game in enumerate(r):
                if i in [0, 1]:
                    self.teams[game[0]].assign(self.teams[game[1]], 'trad')
                    self.teams[game[1]].assign(self.teams[game[0]], 'trad')
                if i == 2:
                    self.teams[game[0]].assign(self.teams[game[1]], 'dink')
                    self.teams[game[1]].assign(self.teams[game[0]], 'dink')
                if i == 3:
                    self.teams[game[0]].assign(self.teams[game[1]], 'lefty')
                    self.teams[game[1]].assign(self.teams[game[0]], 'lefty')
                if i == 4:
                    self.teams[game[0]].assign(self.teams[game[1]], 'noodle')
                    self.teams[game[1]].assign(self.teams[game[0]], 'noodle')
                if i == 5:
                    self.teams[game[0]].assign(self.teams[game[1]], 'one_bounce')
                    self.teams[game[1]].assign(self.teams[game[0]], 'one_bounce')

    def print_rounds(self):
        for i, rd in enumerate(self.rounds):
            print()
            print("      Round {}".format(i + 1))
            for j, game in enumerate(rd):
                if j in [0, 1]:
                    print('Pickleball   {:2d} {:2d}'.format(game[0] + 1, game[1] + 1))
                if j == 2:
                    print('Dink:        {:2d} {:2d}'.format(game[0] + 1, game[1] + 1))
                if j == 3:
                    print('Lefty:       {:2d} {:2d}'.format(game[0] + 1, game[1] + 1))
                if j == 4:
                    print('Swim Noodle: {:2d} {:2d}'.format(game[0] + 1, game[1] + 1))
                if j == 5:
                    print('One Bounce:  {:2d} {:2d}'.format(game[0] + 1, game[1] + 1))

    def mutate(self,n):
        '''Mutates n rounds of Tournament'''
        new_rounds = []
        newt = Tournament(self.numteams,self.n_rounds)
        newt.rounds = list(self.rounds)

        mutated_rounds = random.sample(range(self.n_rounds),n)
        for num in mutated_rounds:
            rand_games = random.randint(2,6)
            indices = random.sample(list(range(6)),rand_games)
            for i in range(rand_games - 1):
                newt.rounds[num][indices[i]], newt.rounds[num][indices[(i + 1) % rand_games]] = \
                    newt.rounds[num][indices[(i + 1) % rand_games]], newt.rounds[num][indices[i]]
            #ind1,ind2 = random.sample(range(int(self.numteams/2)),2)
            #newt.rounds[num][ind1],newt.rounds[num][ind2] = newt.rounds[num][ind2],newt.rounds[num][ind1]
        newt.mutated += 1
        newt.assign_games()
        return newt


    def score_teams(self,test = False):
        """checks if teams have played each other, have played variety of games
        Returns False if it doesn't check out"""

        if not self.generated:
            self.generated = True
            self.generate_rounds()
            self.assign_games()
        for team in self.teams:
            #reset score to 0
            team.score=0
            #get the number of repeats
            rp = team.repeats()
            if rp > 1:
                team.score += 2 * rp - 1
                if test:
                    print("Repeat")
                    print(team.score)
            # for opp in range(1,13):
            #     count_opp = team.opponents.count(opp)
            #     if count_opp > 1:
            #         # print("opps:",team.opponents)
            #         team.score += 2*count_opp - 1
            #         if test:
            #             print("opponents")
            #             print(team.score)
            for type in team.types:
                if type in ['dink', 'lefty', 'noodle', 'one_bounce']:
                    if team.types[type] == 0:
                        team.score += 1
                        if test:
                            print("TYpe 0")
                            print(team.score)
                    if team.types[type] > 2:
                        team.score += team.types[type] - 2
                        if test:
                            print("TYpe over 2")
                            print(team.score)
            if team.types['trad'] < 4:
                team.score += 4 - team.types['trad']
                if test:
                    print("trad < 4")
                    print(team.score)
            if team.types['trad'] > 5:
                team.score += team.types['trad'] - 5
                if test:
                    print("trad > 5")
                    print(team.score)
        team_list = [team.score for team in self.teams]
        #print(team_list)
        self.error = sum([team.score for team in self.teams])
        return self.error


def main():
    global best_ever,lowest_ever_error
    population = [Tournament(12, 11) for i in range(POPN)]

    best_tourn = random.choice(population)
    best_tourn.score_teams()
    lowest_error = best_tourn.error
    #best_ever = best_tourn
    #lowest_ever_error = lowest_error
    best_tourn.print_rounds()
    print()
    print("Lowest Error: ",lowest_error)
    print()
    for team in best_tourn.teams:
        print("num:", team.num + 1, "opps:", team.opponents, "types:", team.types)
    print()
    print("Best Ever:", lowest_ever_error)
    print()
    generations = 0
    generations_without_improvement = 0
    improvements = 0

    while True:
        generations += 1
        generations_without_improvement += 1
        if generations_without_improvement > 50:
            main()
        if generations % 100 == 0:
            print(f"{generations} generations.")
            print("Best Ever:", lowest_ever_error)
        population.sort(key=Tournament.score_teams)
        top_five = population[:5]
        #print([t.error for t in top_three])

        new_tourn = population[0]
        new_score = new_tourn.error
        #print("New score:",new_score)
        if new_score < lowest_error:
            lowest_error = new_score
            best_tourn = new_tourn
            improvements += 1
            if lowest_error < lowest_ever_error:
                best_ever = best_tourn
                lowest_ever_error = lowest_error

            best_tourn.print_rounds()
            print()
            for team in best_tourn.teams:
                print("num:", team.num + 1, "opps:", team.opponents, "types:", team.types)
            print()
            print("Lowest Error:", lowest_error)
            print("Mutated:", best_tourn.mutated)
            print("Improvements:", improvements)
            print()
            best_ever.print_rounds()
            print()
            for team in best_ever.teams:
                print("num:", team.num + 1, "opps:", team.opponents, "types:", team.types)
            print()
            print("Best Ever:", lowest_ever_error)

        population = population[:15]
        for i in range(50):
            for j in range(1,11):
                for t in top_five:
                    #population.append(t)
                    mutated_t = t.mutate(j)
                    population.append(mutated_t)

        # print("Time:",round(time.time() - start,1))

def test():
    best_tourn.print_rounds()
    for team in best_tourn.teams:
        print("num:", team.num + 1, "opps:", team.opponents, "types:", team.types)
    best_tourn.score_teams(True)
    new_tourn = best_tourn.mutate(5)
    for team in new_tourn.teams:
        print("num:", team.num + 1, "opps:", team.opponents, "types:", team.types)
    new_tourn.score_teams(True)


population = [Tournament(12, 11) for i in range(POPN)]

best_tourn = random.choice(population)
best_tourn.score_teams()
lowest_error = best_tourn.error
best_ever = best_tourn
lowest_ever_error = lowest_error
best_tourn.print_rounds()
main()
#test()
