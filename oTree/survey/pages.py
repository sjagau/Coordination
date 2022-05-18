from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Survey(Page):
    form_model ='player'
    
    form_fields=[
        'age',
        'gender',
        'birth',
        'language',
        'major',
        'seniority',
        'econ_exp',
        'stats_exp',
        'risk',
        'CRT_1',
        'CRT_2',
        'CRT_3',
        'CRT_4',
        'SVO_1',
        'SVO_2',
        'SVO_3',
        'freeform',
    ]

    def vars_for_template(self):

        return dict(
            likert=[*range(Constants.likert)],
            max=Constants.likert-1,
            num_parts=len(self.session.config['app_sequence'])-1
        )


page_sequence = [
    Survey,
]
