from __future__ import absolute_import

import os

import pandas as pd
from celery import shared_task
from django.conf import settings

from credit_card.requests.models import ImportUserRequest
from misc.functions import phone_number_correction, is_number
from .constants import IMPORT_USER_REQUEST_CHOICES


@shared_task
# def import_user_request_excel_file_process(object: ImportUserRequest):
def import_user_request_excel_file_process(object_id: int, excel_file_path):
    excel_file_os_path = os.path.join(settings.MEDIA_URL, excel_file_path)

    excel_file = pd.read_excel(excel_file_os_path)
    is_excel_header_correct = ImportUserRequest.is_excel_header_correct(list(excel_file.columns), excel_file)
    obj = ImportUserRequest.objects.get(id=object_id)

    if not is_excel_header_correct:
        obj.status = IMPORT_USER_REQUEST_CHOICES.rejected
        obj.save()

        return False, 'reason: excel header is not correct'
    # TODO refactor for better and cleaner code
    row_explain = []
    row_index = []
    for row in excel_file.iterrows():
        row_dict = row[1]
        row_error = {}
        for key, value in row_dict.items():
            function_name = 'validate_' + key
            if function_name == 'validate_refund_amount' or function_name == 'validate_credit_month_limit':
                if not 'credit' in row_error:
                    result = getattr(FieldValidation, function_name)(value, row_dict['credit'])
                else:
                    row_error[key] = 'not checked, cause of incorrect credit.'
                    result = True
            else:
                result = getattr(FieldValidation, function_name)(value)
            if result:
                continue

            row_error[key] = result

        if row_error:
            row_explain.append(row_error)
            row_index.append(row[0] + 1)
        else:
            # TODO cheange title of excel to credit_amount
            obj.create_all_things_needed_for_credit_card(row_dict['phone_number'], row_dict['first_name'],
                                                         row_dict['last_name'], row_dict['credit'],
                                                         row_dict['refund_period'])

    if row_explain and row_index:
        ImportUserRequest.create_data_frame_for_incorrect_rows(row_index, row_explain, excel_file_os_path)
        obj.status = IMPORT_USER_REQUEST_CHOICES.partial_accepted
        obj.save()

        #
        # phone_number = row['phone_number']
        # first_name = row['first_name']
        # last_name = row['last_name']
        # credit = row['credit']
        # refund_period = row['refund_period']
        # refund_amount = row['refund_amount']
        # credit_month_limit = row['credit_month_limit']

        # TODO create absent user *
        # TODO create regular cwallet for absent user *
        # TODO create credit cwallet *
        # TODO add credit amount to credit cwallet * !
        # TODO send sms to user for inform him/her
        # TODO salavat bar mohammad va ale mohammad


class FieldValidation:
    @staticmethod
    def validate_phone_number(phone_number):
        validate = is_number(phone_number)
        if validate:
            return phone_number_correction(str(phone_number))
        return validate

    @staticmethod
    def validate_credit(credit):
        return is_number(credit)

    @staticmethod
    def validate_refund_period(refund_period):
        validate = is_number(refund_period)
        if validate:
            return 1 <= refund_period <= 12
        return validate

    @staticmethod
    def validate_refund_amount(refund_amount, credit):
        validate = is_number(refund_amount)
        if validate:
            return refund_amount <= credit
        return validate

    @staticmethod
    def validate_credit_month_limit(credit_month_limit, credit):
        validate = is_number(credit_month_limit)
        if validate:
            return credit_month_limit <= credit
        return validate

    # TODO so chert. thin k about it again
    @staticmethod
    def validate_first_name(first_name):
        return first_name

    # TODO so chert. thin k about it again
    @staticmethod
    def validate_last_name(last_name):
        return last_name
