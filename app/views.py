from . import models
from . import serializers
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from decimal import Decimal
from django.db.models import F
from django.db.models import Q


class ExpenseCreateView(APIView):
    """
    Add expenses and calculate according to expense type. 
    Save and update in database.
    """
    def post(self, request):
        serializer = serializers.ExpenseCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                payer = serializer.validated_data['payer']
                participants = serializer.validated_data['participants']
                amount = serializer.validated_data['amount']
                expense_type = serializer.validated_data['expense_type']
                owed_amounts = serializer.validated_data.get('owed_amounts', {})

                if expense_type == models.Expense.EQUAL:
                    # Calculate the equal amount for each participant
                    equal_amount = float(amount) / len(participants) 

                    for participant in participants:
                        if participant != payer:
                            # Check if a balance already exists
                            existing_balance = models.Balance.objects.filter(
                                Q(user=participant, other_user=payer) | Q(user=payer, other_user=participant)
                            ).first()

                            if existing_balance:
                                # Update the existing balance
                                existing_balance.amount = F('amount') + equal_amount
                                existing_balance.save()
                            else:
                                # Create a new balance
                                models.Balance.objects.create(user=participant, other_user=payer, amount=equal_amount)
                elif expense_type == models.Expense.EXACT:
                    for participant in participants:
                        if participant != payer:
                            owed_amount = owed_amounts.get(str(participant.id), Decimal('0'))
                            # Check if a balance already exists
                            existing_balance = models.Balance.objects.filter(
                                Q(user=participant, other_user=payer) | Q(user=payer, other_user=participant)
                            ).first()

                            if existing_balance:
                                # Update the existing balance
                                existing_balance.amount = F('amount') + float(owed_amount)
                                existing_balance.save()
                            else:
                                # Create a new balance
                                models.Balance.objects.create(user=participant, other_user=payer, amount=float(owed_amount))
                elif expense_type == models.Expense.PERCENT:
                    percentages = request.data.get('percentages', [])
                    total_percentage = sum(percentages)

                    if total_percentage != 100:
                        return Response("Total percentage should be 100.", status=status.HTTP_400_BAD_REQUEST)

                    # Calculate the amounts based on percentages
                    for i, participant in enumerate(participants):
                        if participant != payer:
                            percentage = percentages[i]
                            owed_amount = round((percentage / 100) * float(amount), 2)
                            # Check if a balance already exists
                            existing_balance = models.Balance.objects.filter(
                                Q(user=participant, other_user=payer) | Q(user=payer, other_user=participant)
                            ).first()

                            if existing_balance:
                                # Update the existing balance
                                existing_balance.amount = F('amount') + owed_amount
                                existing_balance.save()
                            else:
                                # Create a new balance
                                models.Balance.objects.create(user=participant, other_user=payer, amount=owed_amount)

                return Response("Expense recorded and balances updated.", status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BalanceListView(generics.ListAPIView):
    """
    List all the balance of the user
    """
    queryset = models.Balance.objects.all()
    serializer_class = serializers.BalanceSerializer
    