import django.dispatch

# ___define new signal ____
post_atomic_credit_transaction = django.dispatch.Signal(providing_args=["sender", "instance"])
post_atomic_credit_transaction_for_debt_creation = django.dispatch.Signal(providing_args=["sender", "instance"])
