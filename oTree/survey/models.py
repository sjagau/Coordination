from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
post-experiment survey:
demographics,
risk attitude, SVO, CRT,
freeform question about participant motivations,
author: Stephan Jagau
"""


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1
    likert = 11 #Likert precision


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    age = models.IntegerField(
        label='What is your age?',
        )

    gender = models.StringField(
        choices=['Male', 'Female', 'Other'],
        label='What is your gender?',
        widget=widgets.RadioSelectHorizontal)

    birth = models.StringField(
        label='What country were you born in?',
    )

    language = models.StringField(
        choices=['English', 'Other'],
        label='Is English your first language?',
        widget=widgets.RadioSelectHorizontal)

    major = models.StringField(
        label='What is your major or proposed field of study?',
    )

    seniority = models.StringField(
        choices=['Undergraduate', 'Graduate', 'Other'],
        label='Are you a graduate student or an undergraduate student?',
        widget=widgets.RadioSelectHorizontal)

    econ_exp = models.IntegerField(
        label='How many courses have you taken in economics, excluding econometrics and statistics?',
        min=0)

    stats_exp = models.IntegerField(
        label='How many courses have you taken in probability, econometrics, or statistics?',
        min=0)

    risk = models.IntegerField(
        min=0,
        max=Constants.likert-1)

    CRT_1 = models.IntegerField()
    CRT_2 = models.IntegerField()
    #For CRT_3, 1 means profit, 0 break even, -1 loss
    CRT_3 = models.IntegerField()
    CRT_4 = models.IntegerField()


    freeform = models.LongStringField()

    SVO_1 = models.IntegerField(
        min=0,
        max=Constants.likert-1)
    SVO_2 = models.IntegerField(
        min=0,
        max=Constants.likert-1)
    SVO_3 = models.IntegerField(
        min=0,
        max=Constants.likert-1)