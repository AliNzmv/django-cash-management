from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import BuildCredit, ListCredits, MakeTransaction, TransactionLog, ChangeTransaction


urlpatterns = [
    path('build/', BuildCredit.as_view()),
    path('list/', ListCredits.as_view()),
    path('transaction/', MakeTransaction.as_view()),
    path('transactionreport/<str:choice>/<int:credit_id>/', TransactionLog.as_view()),
    path('changetransaction/<int:transaction_id>/', ChangeTransaction.as_view()),
]
