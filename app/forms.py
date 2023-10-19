from django import forms
from .models import Expense, UserProfile

class UserProfileChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user_profile):
        return f"Name: {user_profile.name} - Email: {user_profile.email} - Mobile Number: {user_profile.mobile_number}"

class ExpenseForm(forms.ModelForm):
    

    participants = forms.ModelMultipleChoiceField(
        label='Participants',
        queryset=UserProfile.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)

        # Customize the labels for participants
        self.fields['participants'].label_from_instance = lambda obj: f"{obj.name}"

    class Meta:
        model = Expense
        fields = ['amount', 'expense_type', 'participants', 'payer']
