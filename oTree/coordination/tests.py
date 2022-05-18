from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random

class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield Submission(pages.Introduction, check_html=False)
        if self.round_number == 2:
            yield Submission(pages.Introduction_Beliefs, check_html=False)
        inputs={}
        for i in range(10):
            choice = random.choice(['A', 'B'])
            choice_label = 'choice_'+str(i)
            belief = random.randint(0, 100)
            belief_label = 'belief_' + str(i)
            inputs.update({choice_label: choice, belief_label: belief})
        inputs.update({'choice_start_time': random.randint(0,100), 'choice_end_time': random.randint(0,100)})
        yield Submission(pages.Choice, inputs, check_html=False)
