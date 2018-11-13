import json
import datetime

from rentalmoose.classes.UserHandler import UserHandler


class ResumeHandler:

    @staticmethod
    def datetime_parse(application_datetime):

        def myconverter(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()

        return json.dumps(application_datetime, default=myconverter).replace('\"', "").replace('\"', "")

    @staticmethod
    def calculate_risk(resume, property, application):

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

        # rental vs total household income

        rental_total_income_ratio = (resume.total_household_income / property.rental_value)
        if 2.5 <= rental_total_income_ratio < 3:
            financial_risk += 10
        elif 2 <= rental_total_income_ratio < 2.5:
            financial_risk += 18
        elif 1.5 <= rental_total_income_ratio < 2:
            financial_risk += 25
        elif rental_total_income_ratio < 1.5:
            financial_risk += 50

        # rental vs wage ratio =========================== #

        rental_wage_ratio = (resume.current_wage / property.rental_value)

        if 2.5 <= rental_wage_ratio < 3:
            financial_risk += 10
        elif 2 <= rental_wage_ratio < 2.5:
            financial_risk += 18
        elif 1.5 <= rental_wage_ratio < 2:
            financial_risk += 25
        elif rental_wage_ratio < 1.5:
            financial_risk += 50

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

        early_vacancy_risk = 0

        if resume.expected_tenancy_length < 2:
            early_vacancy_risk += 40

        if resume.eviction_history is True:
            early_vacancy_risk += 50

        if rental_wage_ratio < 2:
            early_vacancy_risk += 30

        if not resume.consent_criminal_check or not resume.consent_credit_check:
            early_vacancy_risk = 100

        # ================================================================= #
        #                      OVERALL RISK CALCULATION
        # ================================================================= #

        # Some validation to avoid overflow values =========================== #
        if financial_risk >= 100:
            financial_risk = 99.9

        if early_vacancy_risk >= 100:
            early_vacancy_risk = 99.9

        if property_damage_risk >= 100:
            property_damage_risk = 99.9

        overall_score = (financial_risk * 70 + property_damage_risk * 20 + early_vacancy_risk * 10) / 100
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
            "id": resume.tenant.id,
            "name": UserHandler.shorten_name("{} {}".format(resume.tenant.first_name, resume.tenant.last_name)),
            # names are shortened due to privacy concerns
            "applicationDate": ResumeHandler.datetime_parse(application.timestamp),
            "rentalWageRatio": round(rental_wage_ratio, 2),
            "rentalTotalIncomeRatio": round(rental_total_income_ratio, 2),
            "email": resume.tenant.email,
            "phone": resume.phone,
            # "address": resume.address,
            "city": resume.city.name,
            # "zipCode": resume.zipcode,
            "description": resume.description,
            "financialRisk": round(financial_risk,2),
            "propertyDamageRisk": round(property_damage_risk,2),
            "earlyVacancyRisk": round(early_vacancy_risk,2),
            "overallRisk": overall_risk,
            "overallScore": round(overall_score,2),
            "expectedTenancyLength": resume.expected_tenancy_length,
            "totalHouseHoldMembers": resume.total_household_members,
            "consentCriminalCheck": resume.consent_criminal_check,
            "evictionHistory": resume.eviction_history,
            "currentPropertyHasInfestations": resume.current_property_has_infestations,
            "hasPet": resume.has_pet,
            "currentlyWorking": resume.currently_working,
            "currentOcupation": resume.current_ocupation,
            "creditScore": resume.credit_score,
            "maximumRentalBudget": resume.maximum_rental_budget,
            "currentWage": resume.current_wage,
            "consentCreditCheck": resume.consent_credit_check,
            "totalHouseHoldIncome": resume.total_household_income
        }

        return result
