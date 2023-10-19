from django.db import models

class UserProfile(models.Model):
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(('email_address'), unique=True, max_length = 100)
    name = models.CharField(max_length=100)

class Expense(models.Model):
    EQUAL = 'EQUAL'
    EXACT = 'EXACT'
    PERCENT = 'PERCENT'
    EXPENSE_TYPES = [
        (EQUAL, 'Equal'),
        (EXACT, 'Exact'),
        (PERCENT, 'Percent'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPES)
    participants = models.ManyToManyField(UserProfile, related_name='expenses_participated')
    payer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='expenses_paid')
    date = models.DateField(auto_now_add=True)

class Balance(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='balances')
    other_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='other_user_balances')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

