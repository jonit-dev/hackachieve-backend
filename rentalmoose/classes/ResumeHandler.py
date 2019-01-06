import json
import datetime

from django.core.exceptions import ObjectDoesNotExist

from apps.applications.models import Application
from apps.properties.models import Property
from rentalmoose.classes.EmailHandler import *
from rentalmoose.classes.API import API
from rentalmoose.classes.UserHandler import UserHandler
from rentalmoose.settings import HOST_NAME


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

        financial_details = {}

        # Job, employment, etc. =========================== #

        if not resume.currently_working:
            financial_risk += 40
            financial_details["Unemployed Risk"] = 40

        # Past behaviour =========================== #
        if resume.eviction_history:
            financial_risk += 50
            financial_details["Eviction Risk"] = 50

        # Credit score =========================== #

        # we're looking for credit_score over 700

        # if 680 <= resume.credit_score <= 720:
        #     financial_risk += 15
        #     financial_details["Credit Score Risk"] = 15
        # elif 620 <= resume.credit_score < 680:
        #     financial_risk += 25
        #     financial_details["Credit Score Risk"] = 25
        # elif 580 <= resume.credit_score < 620:
        #     financial_risk += 35
        #     financial_details["Credit Score Risk"] = 35
        # elif 500 <= resume.credit_score < 580:
        #     financial_risk += 50
        #     financial_details["Credit Score Risk"] = 50
        # elif resume.credit_score < 500:
        #     financial_risk += 100
        #     financial_details["Credit Score Risk"] = 99.9

        if resume.consent_credit_check is not True:
            financial_risk += 50
            financial_details["Credit Score Risk"] = 50

        # rental vs total household income

        rental_total_income_ratio = (resume.total_household_income / property.rental_value)
        if 2.5 <= rental_total_income_ratio < 3:
            financial_risk += 10
            financial_details["Rental/Total Income Risk"] = 10
        elif 2 <= rental_total_income_ratio < 2.5:
            financial_risk += 18
            financial_details["Rental/Total Income Risk"] = 18
        elif 1.5 <= rental_total_income_ratio < 2:
            financial_risk += 25
            financial_details["Rental/Total Income Risk"] = 25
        elif rental_total_income_ratio < 1.5:
            financial_risk += 50
            financial_details["Rental/Total Income Risk"] = 50

        # rental vs wage ratio =========================== #

        rental_wage_ratio = (resume.current_wage / property.rental_value)

        if 2.5 <= rental_wage_ratio < 3:
            financial_risk += 10
            financial_details["Rental/Wage Risk"] = 10
        elif 2 <= rental_wage_ratio < 2.5:
            financial_risk += 18
            financial_details["Rental/Wage Risk"] = 18
        elif 1.5 <= rental_wage_ratio < 2:
            financial_risk += 25
            financial_details["Rental/Wage Risk"] = 25
        elif rental_wage_ratio < 1.5:
            financial_risk += 50
            financial_details["Rental/Wage Risk"] = 50

        # ================================================================= #
        #                      PROPERTY DAMAGE RISK
        # ================================================================= #

        property_damage_details = {}

        property_damage_risk = 0

        if resume.has_pet is True:
            property_damage_risk += 30
            property_damage_details["Pet Risk"] = 30

        if 1 < resume.total_household_members <= 2:
            property_damage_risk += 20
            property_damage_details["Household Members Qty Risk"] = 20
        elif 2 < resume.total_household_members <= 4:
            property_damage_risk += 30
            property_damage_details["Household Members Qty Risk"] = 30
        elif 4 < resume.total_household_members:
            property_damage_risk += 40
            property_damage_details["Household Members Qty Risk"] = 40

        if resume.consent_criminal_check is not True:
            property_damage_risk = 100
            financial_risk = 100
            property_damage_details["Criminal check refused"] = 99.9

        if resume.current_property_has_infestations is True:
            property_damage_risk += 40
            property_damage_details["Infestations Risk"] = 40

        # ================================================================= #
        #                      EARLY VACATION RISK
        # ================================================================= #

        early_vacancy_risk = 0
        early_vacancy_risk_details = {}

        if resume.expected_tenancy_length < 2:
            early_vacancy_risk += 40
            early_vacancy_risk_details["Low Tenancy Length Risk"] = 40

        if resume.eviction_history is True:
            early_vacancy_risk += 50
            early_vacancy_risk_details["Low Tenancy Length Risk"] = 50

        if rental_wage_ratio < 2:
            early_vacancy_risk += 30
            early_vacancy_risk_details["Low Tenancy Length Risk"] = 30



        # ================================================================= #
        #                      OVERALL RISK CALCULATION
        # ================================================================= #

        # Some validation to avoid overflow values =========================== #
        if financial_risk >= 100:
            financial_risk = 99.9
        elif financial_risk == 0:
            financial_risk = 0.1

        if early_vacancy_risk >= 100:
            early_vacancy_risk = 99.9
        elif early_vacancy_risk == 0:
            early_vacancy_risk = 0.1

        if property_damage_risk >= 100:
            property_damage_risk = 99.9
        elif property_damage_risk == 0:
            property_damage_risk = 0.1

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
            "propertyName": property.title,
            "applicationDate": ResumeHandler.datetime_parse(application.timestamp),
            "rentalWageRatio": round(rental_wage_ratio, 2),
            "rentalTotalIncomeRatio": round(rental_total_income_ratio, 2),
            "email": resume.tenant.email,
            "phone": resume.phone,
            "description": resume.description,
            "financialRisk": round(financial_risk, 2),
            "financialDetails": financial_details,
            "propertyDamageRisk": round(property_damage_risk, 2),
            "propertyDamageDetails": property_damage_details,
            "earlyVacancyRisk": round(early_vacancy_risk, 2),
            "earlyVacancyRiskDetails": early_vacancy_risk_details,
            "overallRisk": overall_risk,
            "overallScore": round(overall_score, 2),
            "expectedTenancyLength": resume.expected_tenancy_length,
            "totalHouseHoldMembers": resume.total_household_members,
            "consentCriminalCheck": resume.consent_criminal_check,
            "evictionHistory": resume.eviction_history,
            "currentPropertyHasInfestations": resume.current_property_has_infestations,
            "hasPet": resume.has_pet,
            "currentlyWorking": resume.currently_working,
            "maximumRentalBudget": resume.maximum_rental_budget,
            "currentWage": resume.current_wage,
            "consentCreditCheck": resume.consent_credit_check,
            "totalHouseHoldIncome": resume.total_household_income,
            "rentalValue": property.rental_value
        }

        if resume.currently_working:
            result['currentOcupation'] = resume.current_ocupation

        return result

    @staticmethod
    def apply_to_property(tenant, property_id):

        if tenant.type != 1:
            return API.json_response({
                "status": "error",
                "message": "Sorry. Only tenants can apply for properties.",
                "type": "danger"
            })

        resume_query = tenant.resume_set.filter(active=True)
        resume = resume_query.first()
        resume_count = resume_query.count()

        if Application.objects.filter(resume=resume.id, property=property_id).count() > 0:
            return API.json_response({
                "status": "error",
                "message": "You already sent a resume for this application",
                "type": "danger"
            })

        # Application =========================== #

        try:
            property = Property.objects.get(pk=property_id)

            if resume_count >= 1:
                Application.apply(resume, property)

                # warn landlord about new application

                tenant_name = UserHandler.capitalize_name(tenant.first_name)
                landlord_name = UserHandler.capitalize_name(property.owner.first_name)

                send = EmailHandler.send_email('New applicant to ' +
                                               property.title, [property.owner.email],
                                               "apply_posting",
                                               {
                                                   "tenant_application_link": "{}/property/check/applicants/{}/{}".format(
                                                       HOST_NAME, property_id, tenant.id),
                                                   "property_title": property.title,
                                                   "tenant_name": tenant_name,
                                                   "landlord_first_name": landlord_name
                                               })

                return API.json_response({
                    "status": "success",
                    "message": "Your tenant's application resume was sent succesfully.",
                    "type": "success"
                })
            else:
                return API.json_response({
                    "status": "error",
                    "message": "You don't have a registered resume to apply.",
                    "type": "danger"
                })




        except ObjectDoesNotExist as e:  # and more generic exception handling on bottom
            return API.json_response({

                "status": "error",
                "message": "The property that you're trying to apply for does not exist.",
                "type": "danger"
            })

