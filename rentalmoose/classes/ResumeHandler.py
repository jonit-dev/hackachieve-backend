import json


class ResumeHandler:

    @staticmethod
    def calculate_risk(resume, property):

        # Validation =========================== #

        # check if user has a resume

        if not resume:
            return False
        else:

            # ================================================================= #
            #                      FINANCIAL RISK
            # ================================================================= #

            financial_risk = 0

            # Job, employment, etc. =========================== #

            if not resume.currently_working:
                financial_risk += 30

            # Past behaviour =========================== #
            if resume.eviction_history:
                financial_risk += 50

            # Credit score =========================== #

            # we're looking for credit_score over 700

            if 680 <= resume.credit_score <= 720:
                financial_risk += 15
            elif 620 <= resume.credit_score < 680:
                financial_risk += 25
            elif 580 <= resume.credit_score < 620:
                financial_risk += 35
            elif 500 <= resume.credit_score < 580:
                financial_risk += 50
            elif resume.credit_score < 500:
                financial_risk += 100

            if financial_risk > 100:
                financial_risk = 100


        # ================================================================= #
        #                      PROPERTY DAMAGE RISK
        # ================================================================= #






        result = {
            "name" : "{} {}".format(resume.tenant.first_name, resume.tenant.last_name),
            "applicationDate": "XXXXX",
            "email": resume.tenant.email,
            "phone": resume.phone,
            "address": resume.address,
            "city": resume.city.name,
            "zipcode": resume.zipcode,
            "description": resume.description,
            "user": resume.tenant.id,
            "finacial_risk": financial_risk,
            "property_damage_risk": "XXX",
            "early_vacation_risk": "XXX",
            "overrallRisk":"XXX",
            "overallScore": "XXX"
        }

        print(result)

        return result
