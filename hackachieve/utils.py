from datetime import timedelta
from django.utils import timezone

column_deadline = timezone.now() + timedelta(days=20)
goal_deadline = timezone.now() + timedelta(days=2)

START_UP_BOARD_LIST = [
    {
        'name': 'Family',
        'description': ''
    },
    {
        'name': 'Health',
        'description': '',
    },
    {'name': 'Career', 'description': ''},
    {'name': 'Finances', 'description': ''},
    {'name': 'Personal Development', 'description': ''},
    {'name': 'Learning', 'description': ''},
    {'name': 'Spiritual', 'description': ''},
    {'name': 'Leisure and Fun', 'description': ''},
    {'name': 'Recruitment', 'description': ''},
    {
        'name': 'Marketing',
        'description': '',
        'long_term_goal': [
            {
                'name': 'Get 20 leads/week (example)',
                'description': 'This is a long term goal sample',
                'deadline': column_deadline,
                'short_term_goal': [
                    {
                        'title': 'Setup google ads campaign (example)',
                        'description': 'This is a sample short term goal.',
                        'deadline': timezone.now() + timedelta(days=7)
                    },
                    {
                        'title': 'Track conversions in google analytics (example)',
                        'description': 'This is a sample short term goal',
                        'deadline': timezone.now() + timedelta(days=7)
                    },
                    {
                        'title': 'Hire PPC expert freelancer (example)',
                        'description': 'This is a sample short term goal',
                        'deadline': timezone.now() + timedelta(days=10)
                    },
                    {
                        'title': 'Setup mailchimp automation flow',
                        'description': 'This is a sample short term goal',
                        'deadline': timezone.now() + timedelta(days=14)
                    }
                ]
            }
        ],
    },
    {'name': 'Sales', 'description': ''},
    {'name': 'Operations', 'description': ''},
    {'name': 'Other', 'description': ''},
]
