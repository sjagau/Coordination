from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

from django.utils import translation

doc = """
Results for coordination experiment,
presented across three tabs,
reusing the decision interface,
author: Stephan Jagau
"""


class Constants(BaseConstants):
    name_in_url = 'results'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payoff_1 = models.CurrencyField()
    payoff_2 = models.CurrencyField()
    payoff_3 = models.CurrencyField()

    # Reversing choice labels for self and other.
    def permute_results(self, results, label_self, label_other):
        task = results[0]
        a1 = results[2][0]
        a2 = a1
        b1 = results[2][1]
        b2 = b1
        c1 = results[2][2]
        c2 = c1
        d1 = results[2][3]
        d2 = d1
        input_self = results[3][0]
        input_other = results[3][1]
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
            # Switching choice_labels; this happens for self and other because display is symmetric
            if input_self == 'A':
                input_self='B'
            elif input_self == 'B':
                input_self='A'
            if input_other == 'A':
                input_other='B'
            elif input_other == 'B':
                input_other='A'
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
            # Adjusting belief_input; this happens because slider is right-oriented if other-labels are reversed
            if task == 1:
                input_self = 100-int(results[3][0])
        # This will indicate whether the Partner's labels in the HTML need to be reversed
        if label_other+label_self==1:
            other_labels_reversed=1
        else:
            other_labels_reversed=0
        new_list = [[a1, b1, c1, d1, a2, b2, c2, d2], input_self, input_other, other_labels_reversed]
        print(new_list)       
        return new_list

