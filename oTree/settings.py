from os import environ

SESSION_CONFIGS = []

APPS_v33 = [
    dict(
        name='coordination',
        display_name="Coordination",
        num_demo_participants=6,
        app_sequence=[
            'coordination', 
            'survey',
            'results'
            ],
        real_world_currency_per_point=1/6,
        participation_fee=10.00,
        use_browser_bots=False,
        first_list=2,
        duration=60,
        tlimit=8,
    ),
]


SESSION_CONFIGS.extend(APPS_v33)

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01,
    participation_fee=7.00,
    doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'points'

ROOMS = [
    dict(
        name='ESSL',
        display_name='ESSL',
        participant_label_file='_rooms/ESSL.txt',
    ),
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '6to_h--z)e)-d1%kir*a6wdqjetonwf30bfhywv+k(mzx^ojw9'

INSTALLED_APPS = ['otree']

DEBUG = False
