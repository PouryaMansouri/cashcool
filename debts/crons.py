from datetime import datetime

from django_cron import CronJobBase, Schedule

from credit_card.debts.exceptions import ThisDebtPenaltyCreateRepetitive, CalculateDebtPenaltyEverydayErrors
from credit_card.debts.models import Debt, DebtPenalty


class CalculateDebtPenaltyEveryday(CronJobBase):
    RUN_AT_TIME = ['00:00']  # every days

    schedule = Schedule(run_at_times=RUN_AT_TIME)
    code = 'credit_card.debts.crons.calculate_debt_penalty_every_day'  # a unique code

    def do(self):

        all_debt_need_penalty = Debt.objects.filter(repayment_date_time__lt=datetime.utcnow())
        count_success = 0
        count_fails = 0
        errors = []
        for debt in all_debt_need_penalty:
            try:
                DebtPenalty.objects.create(debt=debt)
                count_success = count_success + 1
            except ThisDebtPenaltyCreateRepetitive:
                count_fails = count_fails + 1
                repetitive_debt_penalty = DebtPenalty.objects.filter(debt=debt)
                error = [{'fail_debt': debt}, {'error_message: ': ThisDebtPenaltyCreateRepetitive.default_detail},
                         {'repetitive_debt_penalty:': repetitive_debt_penalty}]
                errors.append(error)

        if errors:
            raise CalculateDebtPenaltyEverydayErrors(errors, count_success, count_fails)
