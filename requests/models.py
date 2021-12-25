import os
from datetime import datetime

import pandas as pd
from django.db import models, transaction as db_transaction

from credit_card.credit_cwallets.internal_app_requests import create_credit_cwallet_from_another_app
from credit_card.credit_cwallets.models import CreditCwallet
from credit_card.credit_marketers.models import CreditMarketer
from credit_card.requests.constants import IMPORT_USER_REQUEST_CHOICES, CORRECT_IMPORT_USER_REQUEST_EXCEL_HEADER
from cwallets.internal_app_requests import create_cwallet_from_another_app
from cwallets.models import CWallet
from misc.functions import append_data_frame_to_excel, correct_phone_number_structure
from users.internal_app_requests import create_user_from_another_app
from users.models import Users




class Request(models.Model):
    sender = models.ForeignKey('CreditMarketer', on_delete=models.CASCADE)
    receiver = models.ForeignKey('CreditMarketer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImportUserRequest(Request):

    def excel_file_upload_path(instance, filename):
        date_now_str = str(datetime.utcnow())
        return os.path.join('credit_card',
                            instance.sender.marketer_cwallet.current_cashtag.cashtag,
                            'excel_file', date_now_str + '__' + filename)

    # TODO : call CreditMarketer in ""
    sender = models.ForeignKey(CreditMarketer, on_delete=models.CASCADE, related_name='marketer')
    receiver = models.ForeignKey("cwallets.CWalletRegular", on_delete=models.CASCADE, related_name='admin')

    excel_file = models.FileField(upload_to=excel_file_upload_path, max_length=200)

    status = models.IntegerField(choices=IMPORT_USER_REQUEST_CHOICES, default=IMPORT_USER_REQUEST_CHOICES.pending)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sender.marketer_cwallet.current_cashtag.cashtag + " | " + self.sender.organization.name

    class Meta:
        db_table = "import_user_requests"

    @staticmethod
    def is_excel_header_correct(excel_header: list, excel_file):
        field_with_errors = []
        correct_fielld = []
        for i in range(len(CORRECT_IMPORT_USER_REQUEST_EXCEL_HEADER)):
            if CORRECT_IMPORT_USER_REQUEST_EXCEL_HEADER[i] != excel_header[i]:
                correct_fielld.append(str(CORRECT_IMPORT_USER_REQUEST_EXCEL_HEADER[i]))
                field_with_errors.append(str(excel_header[i]))

        if field_with_errors:
            error_text = "This header is wrong. it has to be completely same as template."

            data_frame = pd.DataFrame({'Error_text': [error_text, ]})
            append_data_frame_to_excel(excel_file, data_frame, sheet_name="Errors")

            data_frame2 = pd.DataFrame({'header with problem': field_with_errors, 'coorect': correct_fielld})
            append_data_frame_to_excel(excel_file, data_frame2, sheet_name="Missed Header")

            return False
        return True

    @staticmethod
    def create_data_frame_for_incorrect_rows(row_index: list, row_explain: list, excel_file):
        data_frame = pd.DataFrame({'index': row_index, 'Error Explanation': row_explain})

        append_data_frame_to_excel(excel_file, data_frame, sheet_name="Incorrect Rows")

        return True

    def create_all_things_needed_for_credit_card(self, phone_number, first_name, last_name, credit_amount,
                                                 checkout_period_month):
        with db_transaction.atomic():
            phone_number = correct_phone_number_structure(str(phone_number))
            user = create_user_from_another_app(phone_number=phone_number, first_name=first_name, last_name=last_name)

            cwallet = create_cwallet_from_another_app(phone_number=phone_number)

            credit_cwallet = create_credit_cwallet_from_another_app(cwallet=cwallet, credit_marketer=self.sender,
                                                                    credit_amount=credit_amount,
                                                                    checkout_period_month=checkout_period_month)
        return user
