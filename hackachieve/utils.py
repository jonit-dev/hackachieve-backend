from datetime import timedelta
from django.utils import timezone

column_deadline = timezone.now() + timedelta(days=20)
goal_deadline = timezone.now() + timedelta(days=2)

START_UP_BOARD_LIST = [
    {
        'name': 'Family',
        'description': '',
        'long_term_goal': [
            {
                'name': 'Travel to Vancouver (example)',
                'description': 'This is a long term goal sample',
                'deadline': column_deadline,
                'short_term_goal': [
                    {
                        'title': 'Buy air tickets',
                        'description': 'This is a sample short term goal',
                        'deadline': timezone.now() + timedelta(days=7)
                    },
                    {
                        'title': 'Hotel reservation',
                        'description': 'This is a sample short term goal',
                        'deadline': timezone.now() + timedelta(days=10)
                    },
                    {
                        'title': 'Health insurance',
                        'description': 'This is a sample short term goal',
                        'deadline': timezone.now() + timedelta(days=14)
                    }
                ]
            }
        ],

    },
    {
        'name': 'Health',
        'description': '',
        # 'long_term_goal': [
        #     {
        #         'name': 'Long term goal title for Health board',
        #         'description': '',
        #         'short_term_goal': [
        #             {
        #                 'title': 'Short term goal title for Health board',
        #                 'description': ''
        #             }
        #         ]
        #     }
        # ]
    },
    {'name': 'Career', 'description': ''},
    {'name': 'Finances', 'description': ''},
    {'name': 'Personal Development', 'description': ''},
    {'name': 'Learning', 'description': ''},
    {'name': 'Spiritual', 'description': ''},
    {'name': 'Leisure and Fun', 'description': ''},
    {'name': 'Recruitment', 'description': ''},
    {'name': 'Sales', 'description': ''},
    {'name': 'Marketing', 'description': ''},
    {'name': 'Operations', 'description': ''},
    {'name': 'Other', 'description': ''},
]
