# import xlwt
from django.contrib import admin

from credit_card.requests.models import ImportUserRequest
from .tasks import import_user_request_excel_file_process


# from django.http import HttpResponse


class ImportUserRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'sender']
    date_hierarchy = 'created_at'
    change_form_template = 'admin/requests/import_user_list.html'

    def response_change(self, request, obj):
        if request.POST.get('process'):
            #TODO delay baby!
            import_user_request_excel_file_process(obj.id, obj.excel_file.name)
        return super().response_change(request, obj)

    #
    # def cashtag(self, obj):
    #     return obj.cwallet.current_cashtag.cashtag
    #
    # def get_shaba_number(self, obj):
    #     return obj.bank_account.shaba_number
    #
    # def get_agent(self, obj):
    #     return obj.get_agent_display()
    #
    # actions = ['export_excel']
    #
    # def export_excel(self, request, queryset):
    #     # init header
    #     response = HttpResponse(content_type='application/ms-excel')
    #     response['Content-Disposition'] = 'attachment; filename="WithdrawRequests.xls"'
    #     wb = xlwt.Workbook(encoding='utf-8')
    #     ws = wb.add_sheet("sheet1")
    #     font_style = xlwt.XFStyle()
    #
    #     # create columns
    #     columns = ['Destination Iban Number (Variz Be Sheba)', 'Owner Name (Name e Sahebe Seporde)',
    #                'Transfer Amount (Mablagh)', 'Description (Sharh)', 'Factor Number (Shomare Factor)',
    #                'Please do not remove this first row. (Lotfan radife nokhost ra paak nafarmayid.)']
    #     row_num = 0
    #     for col_num in range(len(columns)):
    #         ws.write(row_num, col_num, columns[col_num], font_style)
    #
    #     # put data to cells
    #     font_style = xlwt.XFStyle()
    #     for obj in queryset:
    #         if obj.status in obj.STATUSES_COMMITED:
    #             continue
    #         row_num = row_num + 1
    #         user = obj.cwallet.user
    #         shaba_number = obj.bank_account.shaba_number
    #         ws.write(row_num, 0, shaba_number, font_style)
    #         ws.write(row_num, 1, user.first_name + ' ' + user.last_name, font_style)
    #         ws.write(row_num, 2, obj.amount, font_style)
    #     wb.save(response)
    #     return response
    #
    # export_excel.short_description = 'دریافت خروجی برای بانک سامان'


admin.site.site_header = "CashCool Credit Cart Admin"
admin.site.register(ImportUserRequest, ImportUserRequestAdmin)
