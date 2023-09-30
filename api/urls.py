from django.urls import path
from .views import *

urlpatterns = [
    # GET
    path('course/', getCourse),
    path('question/', getQuestion),
    path('active/', active_view),
    path('check-candidate/', check_candidate_view),

    path('register-user/', register_user),

    # POST
    path('registerCandidate/', registerCandidate),
    path('responseUserAnswer/', responseUserAnswer),
    path('checkedTelegramBot/', CheckedTelegramBotView),

]
