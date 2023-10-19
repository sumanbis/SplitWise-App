from rest_framework import serializers
from . import models

class ExpenseCreateSerializer(serializers.Serializer):
    payer = serializers.PrimaryKeyRelatedField(queryset=models.UserProfile.objects.all())
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=models.UserProfile.objects.all())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    expense_type = serializers.ChoiceField(choices=models.Expense.EXPENSE_TYPES)
    owed_amounts = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=2), required=False)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'name', 'email', 'mobile_number')


class BalanceSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()  # Use UserProfileSerializer for the user field
    owed_to = UserProfileSerializer(source='other_user')  # Use the source parameter to rename the field

    class Meta:
        model = models.Balance
        fields = ('user', 'owed_to', 'amount')
