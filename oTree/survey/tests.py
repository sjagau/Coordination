from otree.api import Currency as c, currency_range

from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random

class PlayerBot(Bot):

    def play_round(self):
        inputs = {
            'age': random.randint(0, 100),
            'gender': random.choice(['Male', 'Female', 'Other']),
            'birth': 'US',
            'language': random.choice(['English', 'Other']),
            'major': 'Econ',
            'seniority': random.choice(['Undergraduate', 'Graduate', 'Other']),
            'econ_exp': random.randint(0, 100),
            'stats_exp': random.randint(0, 100),
            'risk': random.randint(0, 10),
            'CRT_1': random.randint(0, 100),
            'CRT_2': random.randint(0, 100),
            'CRT_3': random.choice([-1, 0, 1]),
            'CRT_4': random.randint(0, 100),
            'SVO_1': random.randint(0, 10),
            'SVO_2': random.randint(0, 10),
            'SVO_3': random.randint(0, 10),
            'freeform': 'Bla, bla, bla...',
        }

        yield Submission(pages.Survey, inputs, check_html=False)

