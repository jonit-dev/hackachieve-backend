import datetime
import time
from datetime import date
from datetime import datetime
# from importlib import reload
from apps.goals.models import Goal
from hackachieve.classes.DateHandler import *
import random
from apps.columns.models import Column

from hackachieve.settings import HOST_NAME

# this is just an accessory class. it wont be executed by cron jobs.
from hackachieve.classes.EmailHandler import EmailHandler


def send_goal_reminder_email(user, goal, goal_name, goal_type, diff, titles, project_url):
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
                                       "goal_diff_days": diff,
                                       "project_url": project_url
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

        print('Evaluating email sending...')

        # do not send notifications to goals that are not just examples (goals created on project creation, just to teach the user how to use hackachieve)

        if goal_type == 'long-term' and goal.is_example:
            print('{} long term - is an example goal... skipping!'.format(goal.name))
            pass
        elif goal_type == 'short-term' and goal.column.is_example:
            print('{} short term - is an example goal... skipping!'.format(goal.name))
            pass
        else:
            try:
                user = goal.user
                members = goal.member.all()

                # calculate days difference between today and deadline date.
                diff = DateHandler.get_date_difference(goal.deadline, today, 'days')

                # set some random titles to avoid gmail spam folder
                random_titles = [

                    'Remember to accomplish "{}" in {} day(s)'.format(getattr(goal, goal_name).capitalize(), diff),
                    '{} deadline in {} day(s)'.format(getattr(goal,
                                                              goal_name).capitalize(),
                                                      diff),
                    '{}, "{}" is due in {} day(s)'.format(user.first_name.capitalize(),
                                                          getattr(goal, goal_name).capitalize(), diff),

                ]
                member_title = []
                for member in members:
                    member_title.append([
                        'Remember to accomplish "{}" in {} day(s)'.format(getattr(goal, goal_name).capitalize(), diff),
                        '{} deadline in {} day(s)'.format(getattr(goal,  goal_name).capitalize(), diff),
                        '{}, "{}" is due in {} day(s)'.format(member.first_name.capitalize(),  getattr(goal, goal_name).capitalize(), diff),
                    ])

                # periods = [2, 14, 7, 1, 0]
                periods = [0, 3, 7]

                project_url = ""

                if diff in periods:
                    print(
                        '*** Sending {} day(s) email for goal {} to {}'.format(diff, getattr(goal, goal_name),
                                                                               user.email))

                    if goal_type == 'long-term':
                        project_url = '{}/project/{}/board'.format(HOST_NAME, goal.board.project.id)
                    elif goal_type == 'short-term':
                        project_url = '{}/project/{}/board'.format(HOST_NAME, goal.column.board.project.id)



                    send_goal_reminder_email(user, goal, getattr(goal, goal_name).capitalize(), goal_type, diff,
                                             random_titles, project_url)

                    # sending email if goal has member
                    for idx, member in enumerate(members):
                        send_goal_reminder_email(member, goal, getattr(goal, goal_name).capitalize(), goal_type, diff, member_title[idx], project_url)
                else:
                    pass


            except Exception as e:
                print('An error has occured while trying to send your e-mail')
                print(e)

    pass
