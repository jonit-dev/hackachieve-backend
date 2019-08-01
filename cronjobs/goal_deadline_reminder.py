import datetime
import time
from datetime import date
from datetime import datetime
# from importlib import reload
from apps.goals.models import Goal
from hackachieve.classes.DateHandler import *

import random
from apps.columns.models import Column

# this is just an accessory class. it wont be executed by cron jobs.
from hackachieve.classes.EmailHandler import EmailHandler


def send_goal_reminder_email(user, goal, goal_name, goal_type, diff, titles):
    # choose  a random email title

    n = random.randint(0, len(titles))
    email_title = titles[n - 1]

    # send email to user
    send = EmailHandler.send_email(email_title, [user.email],
                                   "goals_deadline_reminder",
                                   {
                                       "goal_type": goal_type,
                                       "name": user.first_name.capitalize(),
                                       "goal_name": goal_name.capitalize(),
                                       "goal_description": goal.description.capitalize(),
                                       "goal_deadline": goal.deadline,
                                       "goal_diff_days": diff
                                   })

    time.sleep(2)
    return send


def goal_reminder(goal_type):
    today = date.today()
    goals = None
    goal_name = None
    print('*** Goal type is: {} ***'.format(goal_type))

    if goal_type == 'long-term':
        goals = Column.objects.all()
        goal_name = 'name'
    elif goal_type == 'short-term':
        goals = Goal.objects.all()
        goal_name = 'title'

    for goal in goals:

        try:
            user = goal.user

            # calculate days difference between today and deadline date.
            diff = DateHandler.get_date_difference(goal.deadline, today, 'days')

            # set some random titles to avoid gmail spam folder
            random_titles = [

                'Your deadline to "{}" is in {} day(s)'.format(getattr(goal, goal_name).capitalize(), diff),
                '{} deadline is in {} day(s)'.format(getattr(goal,
                                                             goal_name).capitalize(),
                                                     diff),
                '{} your goal "{}" is due in {} day(s)'.format(user.first_name.capitalize(),
                                                               getattr(goal, goal_name).capitalize(), diff),
            ]

            periods = [2, 14, 7, 1, 0]

            if diff in periods:
                print(
                    '*** Sending {} day(s) email for goal {} to {}'.format(diff, getattr(goal, goal_name), user.email))
                send_goal_reminder_email(user, goal, getattr(goal, goal_name).capitalize(), goal_type, diff,
                                         random_titles)
            else:
                pass


        except Exception as e:
            print('An error has occured while trying to send your e-mail')
            print(e)

    pass
