from datetime import timedelta
from django.utils import timezone

column_deadline = timezone.now() - timedelta(days=5)
goal_deadline = timezone.now() - timedelta(days=2)

START_UP_BOARD_LIST = [
    {
        'name': 'Family',
        'description': '',
        'long_term_goal': [
            {
                'name': 'Long term goal title for Family',
                'description': '',
                'deadline': column_deadline,
                'short_term_goal': [
                    {
                        'title': 'Short term goal title for Family board',
                        'description': '',
                        'deadline': goal_deadline
                    }
                ]
            }
        ],

    },
    {
        'name': 'Health',
        'description': '',
        'long_term_goal': [
            {
                'name': 'Long term goal title for Health board',
                'description': '',
                'short_term_goal': [
                    {
                        'title': 'Short term goal title for Health board',
                        'description': ''
                    }
                ]
            }
        ]
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
    {'name': 'Operations', 'description': ''}
]
