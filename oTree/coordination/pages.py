from ._builtin import Page, WaitPage
from .models import Constants
import random

class Introduction(Page):
    form_model = 'player'
    live_method = 'live_intro'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        intro_order_self=self.participant.vars['intro_order_self']
        intro_order_other=self.participant.vars['intro_order_other']
        print('intro_orders:', intro_order_self, intro_order_other)
        #Permuting labels for intro task
        practice_game=self.player.permute_parameters(intro_order_self, intro_order_other, Constants.practice_game)
        #Changing other_labels page and beliefs_quiz orientation if equilibria are off diagonal
        if intro_order_self+intro_order_other==1:
            other_A="B"
            other_B="A"
        else:
            other_A="A"
            other_B="B"
        #Determining answers to choice-based quiz according to matrix display
        if intro_order_self==1:
            payoff_quiz_1=Constants.practice_game[3]
            payoff_quiz_2=Constants.practice_game[1]
        else:
            payoff_quiz_1=Constants.practice_game[0]
            payoff_quiz_2=Constants.practice_game[2]

        return dict(
            treatment=0,
            tlimit=self.session.config['tlimit'],
            a1=practice_game[0],
            b1=practice_game[1],
            c1=practice_game[2],
            d1=practice_game[3],
            a2=practice_game[4],
            b2=practice_game[5],
            c2=practice_game[6],
            d2=practice_game[7],
            num_games=len(Constants.games),
            participation_fee=self.session.config['participation_fee'],
            real_equivalent=1 / self.session.config['real_world_currency_per_point'],   
            other_A=other_A,
            other_B=other_B,
            payoff_quiz_1=payoff_quiz_1,  
            payoff_quiz_2=payoff_quiz_2,   
            duration=self.session.config['duration']
        )
        
class Introduction_Beliefs(Page):
    form_model = 'player'
    live_method = 'live_intro'

    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self):
        intro_order_self=self.participant.vars['intro_order_self']
        intro_order_other=self.participant.vars['intro_order_other']
        print('intro_orders:', intro_order_self, intro_order_other)
        #Permuting labels for intro task
        practice_game=self.player.permute_parameters(intro_order_self, intro_order_other, Constants.practice_game)
        #Changing other_labels page and beliefs_quiz orientation if equilibria are off diagonal
        if intro_order_self+intro_order_other==1:
            other_A="B"
            other_B="A"
            beliefs_quiz=1
        else:
            other_A="A"
            other_B="B"
            beliefs_quiz=0

        return dict(
            tlimit=self.session.config['tlimit'],
            a1=practice_game[0],
            b1=practice_game[1],
            c1=practice_game[2],
            d1=practice_game[3],
            a2=practice_game[4],
            b2=practice_game[5],
            c2=practice_game[6],
            d2=practice_game[7],
            num_games=len(Constants.games),
            num_tasks=2*len(Constants.games),
            belief_high=Constants.belief_high,
            belief_low=Constants.belief_low,    
            other_A=other_A,
            other_B=other_B,  
            beliefs_quiz=beliefs_quiz,  
        )

class Choice(Page):
    form_model = 'player'
    live_method = 'live_input'
    

    def get_form_fields(self):
        form_fields=[]
        for i in Constants.games:
            form_fields.append('choice_'+str(i))
            if self.round_number>1:
                form_fields.append('belief_'+str(i))
        form_fields.extend(['choice_start_time', 'choice_end_time'])
        return form_fields

    def vars_for_template(self):
        list=self.participant.vars['list_sequence'][self.round_number-1]
        it_order=self.participant.vars['it_order_'+str(self.round_number)]
        ch_order_self=self.participant.vars['ch_order_self_'+str(self.round_number)]
        ch_order_other=self.participant.vars['ch_order_other_'+str(self.round_number)] 
        tlimit=self.session.config['tlimit']
        #Setting up payoffs from corresponding entry of game_dict
        game_dict=self.session.vars['game_dict'][list]
        if it_order==0:
            a = game_dict[0]
            b = game_dict[1]
            c = game_dict[2]
            d = game_dict[3]
            games = Constants.games.copy()
        elif it_order==1:
            print('Reversing order')
            a = game_dict[0][::-1]
            b = game_dict[1][::-1]
            c = game_dict[2][::-1]
            d = game_dict[3][::-1]
            games = Constants.games.copy()[::-1]
        #Permuting choice labels
        perm_dict=self.player.permute_parameters(ch_order_self, ch_order_other, [a, b, c, d])
        a1 = perm_dict[0]
        b1 = perm_dict[1]
        c1 = perm_dict[2]
        d1 = perm_dict[3]
        a2 = perm_dict[4]
        b2 = perm_dict[5]
        c2 = perm_dict[6]
        d2 = perm_dict[7]
        #Changing other_labels page if equilibria are off diagonal
        if ch_order_self+ch_order_other==1:
            other_A="B"
            other_B="A"
        else:
            other_A="A"
            other_B="B"
        #First list has no beliefs, also first list is its own part
        if self.round_number==1:
            beliefs=0
            num_part=1
        else:
            beliefs=1
            num_part=2
        #Round and game counter, adjusted for Parts 1
        if self.round_number == 1:
            max_round = 11
            min_round = 1
        else:
            max_round = (self.round_number-1)*10+1
            min_round = max_round - 10
        next_max = max_round + 10
        next_min = min_round + 10
        rounds = [*range(min_round, max_round)]
        #Zipping page_inputs
        page_input = [*zip(games, rounds, a1, b1, c1, d1, a2, b2, c2, d2)]
        page_indices = [*zip(games, rounds)]

        return dict(
            beliefs=beliefs,
            num_rounds=Constants.num_rounds,
            num_round=self.round_number,
            num_part=num_part,
            input=page_input,
            indices=page_indices,
            min=min_round,
            max=max_round-1,
            next_min=next_min,
            next_max=next_max-1,
            tlimit=tlimit,
            other_A=other_A,
            other_B=other_B,   
        )
    
    def before_next_page(self):
        p=self.player
        ch_order_self=p.participant.vars['ch_order_self_'+str(self.round_number)]
        ch_order_other=p.participant.vars['ch_order_other_'+str(self.round_number)]
        #Putting choices and beliefs into the top-left, down-right orientation
        p.unscramble_inputs(ch_order_self,ch_order_other)        
        #Putting problems into order of list sequence
        if self.round_number == 3:
            list_sequence = self.participant.vars['list_sequence']
            p.reorder_inputs(list_sequence)
            


#After all subjects finish the choice lists, results are set, and subjects are forwarded to the survey.                   
class Next(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    after_all_players_arrive = 'set_results'

    template_name = "coordination/Wait.html"

    wait_for_all_groups = True

    body_text = "Waiting for other participants to finish make their decisions..."


page_sequence = [
    Introduction,
    Introduction_Beliefs,
    Choice,
    Next,
]
