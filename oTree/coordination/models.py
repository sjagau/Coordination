from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Currency as c
)
import random
import numpy as np
import json

doc = """
Coordination games without feedback,
choice list style,
tracking of preliminary inputs using live pages,
based on Nash/Pareto-decomposition (Jessie and Saari, 2019),
block-randomized order,
random ascending/descending presentation of items,
randomized presentation of choice labels,
belief elicitation after round 1,
beliefs paid with binarized scoring rule (based on Wilson and Vespa, 2018),
random incentive scheme,
CONFIGURABLES:
tlimit (integer, soft time limit in minutes),
first_list (0,1,2, first list shown to subjects without belief elicitation)
duration (duration of experiment in minutes for intro page)
author: Stephan Jagau
"""


class Constants(BaseConstants):
    players_per_group = 2
    name_in_url = 'coordination'
    # Each round is a choice list
    num_rounds = 3
    # Game payoffs based on decomposition; constant Nash sum S2=16-S; Parameters K (Kernel), E (A-Externality), S (A-Nash Term)
    K = c(34)
    NSum = c(16)
    #S's for Sequences 1, 2
    S = [c(-1), c(1), c(3), c(5), c(7), c(9), c(11), c(13), c(15), c(17)]
    #E's for Sequences 1, 2
    ES = [c(0),c(16)]
    #E's for sequence 3
    E = [c(-18), c(-14), c(-10), c(-6), c(-2), c(2), c(6), c(10), c(14), c(18)]
    #Game indices use for lists. This is currently 0,...,9 for all lists
    games=[*range(10)]    
    #Belief incentives match optimization premia of games c(32)
    belief_low = c(6)
    belief_high = c(38)
    #Practice game has S=7, E=2, K=12
    practice_game = [c(21), c(1), c(5), c(19)]


class Subsession(BaseSubsession):
    def creating_session(self):
        print('in creating_session', self.round_number)
        for p in self.get_players():
            #randomize item order; saved in participant.vars to be reused later
            it_order=random.randint(0,1)
            ch_order_self=random.randint(0,1)
            ch_order_other=random.randint(0,1)
            p.participant.vars['it_order_'+str(self.round_number)]=it_order
            p.participant.vars['ch_order_self_'+str(self.round_number)]=ch_order_self
            p.participant.vars['ch_order_other_'+str(self.round_number)]=ch_order_other

        if self.round_number==1:        
            #Saving number of lists and belief incentives to pass on to results app
            self.session.vars['rounds_coordination'] = Constants.num_rounds
            self.session.vars['belief_high'] = Constants.belief_high
            self.session.vars['belief_low'] = Constants.belief_low
            #Constructing Dictionary of Games to be used; saved as session var
            games=Constants.games
            game_dict={}
            for k in range(Constants.num_rounds):
                if k<2:
                    #first two lists have constant E=0,16 and variable S
                    if k==0:     
                        a = [Constants.K+Constants.S[i] + Constants.ES[0] for i in games]
                        b = [Constants.K + Constants.S[i] - Constants.NSum - Constants.ES[0] for i in games]
                        c = [Constants.K - Constants.S[i] + Constants.ES[0] for i in games]
                        d = [Constants.K - Constants.S[i] + Constants.NSum - Constants.ES[0] for i in games]
                    elif k==1:
                        a = [Constants.K + Constants.S[i] + Constants.ES[1] for i in games]
                        b = [Constants.K + Constants.S[i] - Constants.NSum - Constants.ES[1] for i in games]
                        c = [Constants.K - Constants.S[i] + Constants.ES[1] for i in games]
                        d = [Constants.K - Constants.S[i] + Constants.NSum - Constants.ES[1] for i in games]
                #third list has constant S=7 and variable E
                elif k==2:
                    a = [Constants.K + Constants.S[4] + Constants.E[i] for i in games]
                    b = [Constants.K + Constants.S[4] - Constants.NSum - Constants.E[i] for i in games]
                    c = [Constants.K - Constants.S[4] + Constants.E[i] for i in games]
                    d = [Constants.K - Constants.S[4] + Constants.NSum - Constants.E[i] for i in games]
                game_dict[k]=[a,b,c,d]                
            self.session.vars['game_dict'] = game_dict
            
            for p in self.get_players():
                # set order of choice lists, first list fixed in session vars (balanced across sessions), otherwise random
                list_sequence=[*range(Constants.num_rounds)]
                first_list=self.session.config['first_list']
                print('first item is', first_list)
                list_sequence.pop(first_list)
                if p.id_in_subsession<=self.session.num_participants/2:
                    list_sequence.reverse()                
                print('order of remainder is', list_sequence)
                list_sequence.insert(0,first_list)
                p.participant.vars['list_sequence'] = list_sequence
                print('set list sequence for player', p.id_in_subsession, 'to', p.participant.vars['list_sequence'])  
                #intro_labels are randomized at player level
                intro_order_self=random.randint(0,1)
                intro_order_other=random.randint(0,1) 
                p.participant.vars['intro_order_self']=intro_order_self
                p.participant.vars['intro_order_other']=intro_order_other    
                print('intro order for player', p.id_in_subsession, ':', p.participant.vars['intro_order_self'],p.participant.vars['intro_order_other'])         
            #Players grouped randomly for round 1
            self.group_randomly()
            print('Players grouped randomly.')
            print('matrix is', self.get_group_matrix())
        else:
            #Round robin matching after round 1
            self.group_like_round(self.round_number-1)
            self.set_group_matrix(self.round_robin(self.get_group_matrix()))
            print('matrix is', self.get_group_matrix())


    def round_robin(self, old_matrix):
        #print('Round robin: Round ', self.round_number)
        #print('old matrix is', old_matrix)
        new_matrix =[]
        for k in range(len(old_matrix)):
            #Setting new p1
            if k == 0:
                p1 = old_matrix[0][0]
            elif k == 1:
                p1 = old_matrix[0][1]
            else:
                p1 = old_matrix[k-1][0]
            #Setting new p2
            if k < len(old_matrix)-1:
                p2 = old_matrix[k+1][1]
            else:
                p2 = old_matrix[k][0]
            new_matrix.append([p1, p2])
        return new_matrix
    
    def set_results(self):
        first_list = self.session.config['first_list']
        for p in self.get_players():
            #Players are randomly paid for 1 choice from first list and 1 choice and 1 bleiefs task from lists 2 and 3
            game_dict=self.session.vars['game_dict']
            results_dict={}
            num_rounds=Constants.num_rounds
            print('first list:',first_list)
            tasks=[0,1]
            random.shuffle(tasks)
            print('randomly fixed tasks:', tasks)
            tasks.insert(first_list,0)
            print('final tasks allocation:', tasks)
            #Determining results round by round
            for k in [*range(num_rounds)]:
                #Selecting a random game from the choice list
                g = random.randint(0,9)
                #Game parameters
                a=game_dict[k][0][g]
                b=game_dict[k][1][g]
                c=game_dict[k][2][g]
                d=game_dict[k][3][g]
                #Other player based on round-robin matching
                other = p.in_round(k+1).get_others_in_group()[0]
                #Retrieving decisions from database
                choice = getattr(p.in_round(k+1), 'choice_' + str(g))
                oth_choice = getattr(other, 'choice_' + str(g))
                #Payoff from decisions
                if tasks[k] == 0:
                    #Constructing payoff matrix
                    points_matrix = {
                        'A':
                        {
                            'A': a,
                            'B': b,
                        },
                        'B':
                        {
                            'A': c,
                            'B': d,
                        },
                    }
                    payoff = (points_matrix[choice][oth_choice])
                    #Saving in dictionary
                    results_dict[k]=[tasks[k], g, [a,b,c,d], [choice, oth_choice], payoff]
                    print('Results player', p.id_in_subsession, 'in round ', k+1, ':', results_dict[k])
                #Payoff from belief
                elif tasks[k]==1:
                    #Retrieving Belief
                    belief = getattr(p.in_round(k+1), 'belief_' + str(g))
                    #Random numbers for BSR
                    rd1=random.uniform(0,100)
                    rd2=random.uniform(0,100)
                    #Payoff from belief, following BSR (implementation from Wilson and Vespa, 2018)
                    if oth_choice=='A' and belief > min(rd1, rd2):
                        payoff = Constants.belief_high
                    elif oth_choice=='B' and 100-belief > min(rd1, rd2):
                        payoff = Constants.belief_high
                    else:
                        payoff = Constants.belief_low
                    #Saving in dictionary
                    results_dict[k]=[tasks[k], g, [a, b, c, d], [belief, oth_choice, rd1, rd2], payoff]
                    print('Results player', p.id_in_subsession, 'in round ', k+1, ':', results_dict[k])
            p.participant.vars['results_dict']=results_dict


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #Start and end times for each choice list (Unix Timestamp)
    choice_start_time = models.LongStringField()
    choice_end_time = models.LongStringField()
    #Navigation log for each decision interface
    nav_dict = models.LongStringField()
    #Preliminary and final input for each choice list, prelim. inputs are gathered as dict, saved as string 
    for j in range(10):
        locals()['choice_' + str(j)] = models.CharField(
        choices=['A', 'B'],
        doc="""This player's choice""",
        )
        locals()['belief_' + str(j)] = models.FloatField(
        doc="""This player's FOB""",
        )
        locals()['input_dict_' + str(j)] = models.LongStringField()
    del j

    #Live input collects nav_dict and input_dict data, dicts are saved as strings in the database
    def live_input(self, data):
        print(data)
        #Preliminary inputs
        if len(data) == 4:
            #Calling in variables governing ch display
            ch_order_self=self.participant.vars['ch_order_self_'+str(self.round_number)]
            ch_order_other=self.participant.vars['ch_order_other_'+str(self.round_number)]
            print('Choice_orders:', ch_order_self, ch_order_other)
            #Loading data and existing input_dict (possibly empty)
            g = data['game']
            old_dict = getattr(self, 'input_dict_' + str(g))
            t = data['type']
            #Unscrambling ch inputs
            if t == 'choice' and ch_order_self == 1:
                if data['value'] == 'A':
                    data['value']='B'
                else:
                    data['value']='A'
            #Unscrambling belief inputs
            if t == 'belief' and ch_order_other == 1:
                data['value']=100-int(data['value'])
            #Converting to string and adding to input_dict
            new_dict = json.dumps(data)
            print('Final Input:', new_dict)
            if isinstance(old_dict, str):
                new_dict = old_dict + new_dict
            setattr(self, 'input_dict_' + str(g), new_dict)
        #Nav log   
        elif len(data) == 3:
            old_dict = getattr(self, 'nav_dict')
            new_dict = json.dumps(data)
            if isinstance(old_dict, str):
                new_dict = old_dict + new_dict
            setattr(self, 'nav_dict', new_dict)
    #This live method for intro-pages collects total time spent as well as time taken to solve each quiz
    def live_intro(self,data):
        print(data)
        self.participant.vars['intro_' + data['type']] = data['time']

    #Reversing choice labels for self and other.
    def permute_parameters(self, label_self, label_other, list):
        a1 = list[0]
        a2 = a1
        b1 = list[1]
        b2 = b1
        c1 = list[2]
        c2 = c1
        d1 = list[3]
        d2 = d1
        if label_self==1:
            print('Reversing labels; self')
            bk_a1 = a1
            bk_b1 = b1
            a1 = c1
            c1 = bk_a1
            b1 = d1
            d1 = bk_b1
            bk_a2 = a2
            bk_c2 = c2
            a2 = b2
            b2 = bk_a2
            c2 = d2
            d2 = bk_c2
        if label_other==1:
            print('Reversing labels; other')
            bk_a1 = a1
            bk_c1 = c1
            a1 = b1
            b1 = bk_a1
            c1 = d1
            d1 = bk_c1
            bk_a2 = a2
            bk_b2 = b2
            a2 = c2
            c2 = bk_a2
            b2 = d2
            d2 = bk_b2
        new_list = [a1, b1, c1, d1, a2, b2, c2, d2]
        print(new_list)       
        return new_list
    #Adjusting input for players that experienced reversed choice labels, runs after each round if conditions are met
    def unscramble_inputs(self, label_self, label_other):
        #Back permuting choice inputs in case self choice labels were switched
        games = Constants.games
        if label_self==1:
            ch_list=[getattr(self, 'choice_' + str(i)) for i in games]
            print('permuted choice input was', ch_list)
            for i in games:
                if ch_list[i]=='A':
                    setattr(self, 'choice_' + str(i), 'B')
                elif ch_list[i]=='B':
                    setattr(self, 'choice_' + str(i), 'A')
            print('unscrambled choice input is', [getattr(self, 'choice_' + str(i)) for i in games])
        #Back permuting belief inputs in case other choice labels were switched         
        if self.round_number > 1 and label_other==1:
            bel_list=[getattr(self, 'belief_' + str(i)) for i in games]
            print('permuted belief input was', bel_list)
            for i in games:
                setattr(self, 'belief_' + str(i), 100-bel_list[i])            
            print('unscrambled belief input is', [getattr(self, 'belief_' + str(i)) for i in games])
    #Reordering lists and tasks according to list_sequences, runs after final round
    def reorder_inputs(self, list_sequence):
            games = Constants.games
            inputs = {}
            print('Reordering inputs according to list_sequence', list_sequence)
            #Retrieving all inputs by active player in chronological order
            for i in range(len(list_sequence)):
                p = self.in_round(i+1)
                choices = [getattr(p, 'choice_' + str(k)) for k in games]
                beliefs = [getattr(p, 'belief_' + str(k)) for k in games]
                input_dicts = [getattr(p, 'input_dict_' + str(k)) for k in games]
                nav_dict = getattr(p, 'nav_dict')
                choice_start_time = getattr(p, 'choice_start_time')
                choice_end_time = getattr(p, 'choice_end_time')
                inputs[p] = [choices, beliefs, input_dicts, nav_dict, choice_start_time, choice_end_time]
            print('Inputs in chronological order:', inputs)
            #Reordering inputs according to list numbering
            for i in range(len(list_sequence)):
                print(i)      
                p_chron = self.in_round(i+1)
                print(list_sequence[i])
                p_list = self.in_round(list_sequence[i]+1)
                for k in games:
                    setattr(p_list, 'choice_' + str(k), inputs[p_chron][0][k])
                    setattr(p_list, 'belief_' + str(k), inputs[p_chron][1][k])
                    setattr(p_list, 'input_dict_' + str(k), inputs[p_chron][2][k])
                    setattr(p_list, 'nav_dict', inputs[p_chron][3])
                    setattr(p_list, 'choice_start_time', inputs[p_chron][4])
                    setattr(p_list, 'choice_end_time', inputs[p_chron][5])
            for i in range(len(list_sequence)):
                p = self.in_round(i+1)
                choices = [getattr(p, 'choice_' + str(k)) for k in games]
                beliefs = [getattr(p, 'belief_' + str(k)) for k in games]
                input_dicts = [getattr(p, 'input_dict_' + str(k)) for k in games]
                nav_dict = getattr(p, 'nav_dict')
                choice_start_time = getattr(p, 'choice_start_time')
                choice_end_time = getattr(p, 'choice_end_time')
                inputs[p] = [choices, beliefs, input_dicts, nav_dict, choice_start_time, choice_end_time]
            print('Inputs in order of list sequence:', inputs)

def custom_export(players):
    # Scrambling data in chronological order
    yield ['session', 'participant_code', 'round_number', 'list', 'it_order', 'labels_self', 'labels_other']
    for p in players:
        yield [
            p.session.code,
            p.participant.code,
            p.round_number,
            p.participant.vars['list_sequence'][p.round_number-1],
            p.participant.vars['it_order_'+str(p.round_number)],
            p.participant.vars['ch_order_self_'+str(p.round_number)],
            p.participant.vars['ch_order_other_'+str(p.round_number)],
        ]




        


