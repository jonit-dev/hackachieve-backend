import json


class ResumeHandler:

    @staticmethod
    def calculate_risk(resume, property):

        # Validation =========================== #

        # check if user has a resume

        # ================================================================= #
        #                      FINANCIAL RISK
        # ================================================================= #

        financial_risk = 0

        # Job, employment, etc. =========================== #

        if not resume.currently_working:
            financial_risk += 40

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

        if resume.consent_credit_check is not True:
            financial_risk += 100

        # rental vs wage ratio =========================== #

        rental_wage_ratio = (resume.current_wage / property.rental_value)

        if 2.5 <= rental_wage_ratio < 3:
            financial_risk += 20
        elif 2 <= rental_wage_ratio < 2.5:
            financial_risk += 35
        elif 1.5 <= rental_wage_ratio < 2:
            financial_risk += 50
        elif rental_wage_ratio < 1.5:
            financial_risk += 100

        # ================================================================= #
        #                      PROPERTY DAMAGE RISK
        # ================================================================= #

        property_damage_risk = 0

        if resume.has_pet is True:
            property_damage_risk += 30

        if 1 < resume.total_household_members <= 2:
            property_damage_risk += 20
        elif 2 < resume.total_household_members <= 4:
            property_damage_risk += 30
        elif 4 < resume.total_household_members:
            property_damage_risk += 40

        if resume.consent_criminal_check is not True:
            property_damage_risk = 100
            financial_risk = 100

        if resume.current_property_has_infestations is True:
            property_damage_risk += 40

        # ================================================================= #
        #                      EARLY VACATION RISK
        # ================================================================= #

        early_vacation_risk = 0

        if resume.expected_tenancy_length < 2:
            early_vacation_risk += 40

        if resume.eviction_history is True:
            early_vacation_risk += 50

        if rental_wage_ratio < 2:
            early_vacation_risk += 30

        if not resume.consent_criminal_check or not resume.consent_credit_check:
            early_vacation_risk = 100

        # ================================================================= #
        #                      OVERALL RISK CALCULATION
        # ================================================================= #

        # Some validation to avoid overflow values =========================== #
        if financial_risk > 100:
            financial_risk = 100

        if early_vacation_risk > 100:
            early_vacation_risk = 100

        if property_damage_risk > 100:
            property_damage_risk = 100

        overall_score = (financial_risk * 70 + property_damage_risk * 20 + early_vacation_risk * 10) / 100
        overall_risk = ""

        if overall_score >= 60:
            overall_risk = "HIGH"
        elif 40 <= overall_score < 60:
            overall_risk = "MEDIUM"
        elif overall_score < 40:
            overall_risk = "LOW"

        # ================================================================= #
        #                      FINAL JSON ANSWER
        # ================================================================= #

        result = {
            "name": "{} {}".format(resume.tenant.first_name, resume.tenant.last_name),
            "applicationDate": "XXXXX",
            "rental_wage_ratio": rental_wage_ratio,
            "email": resume.tenant.email,
            "phone": resume.phone,
            "address": resume.address,
            "city": resume.city.name,
            "zipcode": resume.zipcode,
            "description": resume.description,
            "finacial_risk": financial_risk,
            "property_damage_risk": property_damage_risk,
            "early_vacation_risk": early_vacation_risk,
            "overrallRisk": overall_risk,
            "overallScore": overall_score
        }


        return result
