from rest_framework import serializers
from .models import Credit, Transaction
import datetime

class BuildCreditSerializer(serializers.ModelSerializer):
    date_created = datetime.date.today()

    class Meta:
        model = Credit
        fields = ('balance', 'date_created')

    def validate_price(self, value):
        if value<0:
            raise serializers.ValidationError('Minimum balance must be positive')
        return value

class MakeTransactionSerializer(serializers.Serializer):
    from_credit = serializers.IntegerField()
    to_credit = serializers.IntegerField()
    money = serializers.IntegerField()
    category = serializers.CharField(max_length=2)

    def validate_category(self, value):
        if value == 'g' or value == 'u':
            return value
        raise serializers.ValidationError("Invalid category! Choices are (g,u)!")

    def validate_to_credit(self, value):
        if value < 1:
            raise serializers.ValidationError("Invalid credit id!")
        return value

    def validate_from_credit(self, value):
        if value < 1:
            raise serializers.ValidationError("Invalid credit id!")
        return value

    def validate_money(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount of money must be more than 0 !")
        return value

    def create(self, validated_data):
        transaction = Transaction()
        transaction.save()
        transaction.init_credit = validated_data.get('from_credit')
        transaction.credits.add(Credit.objects.get(id=validated_data.get('from_credit')))
        transaction.credits.add(Credit.objects.get(id=validated_data.get('to_credit')))
        credit1 = Credit.objects.get(id=validated_data.get('from_credit'))
        credit1.balance = credit1.balance - validated_data.get('money')
        credit1.save(update_fields=['balance'])
        credit2 = Credit.objects.get(id=validated_data.get('to_credit'))
        credit2.balance = credit2.balance + validated_data.get('money')
        credit2.save(update_fields=['balance'])
        transaction.money = validated_data.get('money')
        transaction.save()
        return transaction




