from time import sleep

from apps.resumes.models import Resume
from hackachieve.classes.PropertyHandler import *


def check_resume_matches():
    # fetch all resumes


    # resumes = Resume.objects.filter(pk=1) #dev test
    # resumes = Resume.objects.filter(pk=58) #prod test
    resumes = Resume.objects.all()

    for resume in resumes:
        resume_cities = resume.resume_city_set.all()
        resume_neighborhoods = resume.resume_neighborhood_set.all()

        matches = PropertyHandler.check_matches(resume, resume_cities, resume_neighborhoods)

        print(matches)

        sleep(60 * 5)
