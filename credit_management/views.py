import datetime
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import BuildCreditSerializer, MakeTransactionSerializer
from .models import Credit, Transaction
from rest_framework.generics import get_object_or_404

class BuildCredit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        credit_serializer = BuildCreditSerializer(data=request.data)
        if credit_serializer.is_valid():
            credit_serializer.save(user=request.user)
            return Response(data={
                'massage': 'Credit has added successfully!'
            }, status=201)
        return Response(data=credit_serializer.errors)

class ListCredits(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuildCreditSerializer

    def get_queryset(self):
        return Credit.objects.filter(user=self.request.user)


class MakeTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MakeTransactionSerializer(data=request.data)
        if serializer.is_valid():
            from_credit = get_object_or_404(Credit, id=serializer.validated_data.get('from_credit'))
            get_object_or_404(Credit, id=serializer.validated_data.get('to_credit'))
            transaction = serializer.save()
            if from_credit.user == request.user:
                transaction.date = datetime.date.today()
                transaction.status = 'S'
                transaction.save(update_fields=['status', 'date'])
                return Response(data={"message": "Done!"}, status=201)
            transaction.status = 'F'
            transaction.save(update_fields=['status'])
            return Response(data={"message": "This credit doesn't belong to you!"}, status=400)
        return Response(data=serializer.errors)


class TransactionLog(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, choice,credit_id):
        credit = get_object_or_404(Credit, id=credit_id)
        if credit.user == request.user:
            all_transactions = credit.transaction_set.all()
            if choice == 'm':
                transactions = all_transactions.filter(date__gte=(datetime.date.today() - datetime.timedelta(days=30)))
            elif choice == 'w':
                transactions = all_transactions.filter(date__gte=datetime.date.today() - datetime.timedelta(days=7))
            else:
                return Response(data={'message': 'Invalid input!, Valid choices:(m, w)!'}, status=404)
            transaction_string = str()
            counter = 1
            for transaction in transactions:
                if transaction.init_credit == credit_id:
                    transaction_type = 'Expense'
                else:
                    transaction_type = 'Income'
                transaction_string += f"({counter}): ID= {transaction.id} | {transaction_type} | Category: {transaction.category}  |  from credit id : {transaction.credits.all()[0].id} to credit id: {transaction.credits.all()[1].id} | Money = {transaction.money} ==> {transaction.status}"
                transaction_string += '<br/>'
                counter += 1
            return Response(data={"detail": f"<br/>{transaction_string}"}, status=201)
        return Response(data={"message": "This credit doesn't belong to you!"}, status=400)


class ChangeTransaction(APIView):
    permission_classes = [IsAuthenticated]

    #only the user who had built transaction can change field and only categry can changed.
    def put(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        if Credit.objects.get(id=transaction.init_credit) in request.user.credit_set.all():
            data = request.data
            category = data.get('category')
            if not (category == 'g' or category == 'u'):
                return Response(data={'message': "Invalid category! Choices are (g,u)!"}, status=400)
            transaction.category = category
            transaction.save(update_fields=['category'])
            return Response(data={'message': "Transaction updated successfully!"}, status=201)
        else:
            return Response(data={"message": "This credit doesn't belong to you!"}, status=400)

    # only the user who had built transaction can delete field.
    def delete(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        if Credit.objects.get(id=transaction.init_credit) in request.user.credit_set.all():
            transaction.delete()
            return Response(data={'message': 'Transaction deleted successfully!'}, status=201)
        else:
            return Response(data={"message": "This credit doesn't belong to you!"}, status=400)
