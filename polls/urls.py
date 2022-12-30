from django.urls import path

from polls.views import login, account, transfer

urlpatterns = [
    path('', login, name='login'),
    path('account/<str:user>', account, name='home' ),
    path('account/<str:user>/transfer/', transfer, name='transfer'),
    #FLAW2:path('account/', include("django.contrib.auth.urls")) 
]