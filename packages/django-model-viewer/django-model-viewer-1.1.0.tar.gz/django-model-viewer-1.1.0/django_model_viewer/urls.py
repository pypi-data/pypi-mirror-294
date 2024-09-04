from django.urls import path
from .views import ShowModelsAll, ajax_call, ajax_call_get_path, ajax_call_create_model_create_path, save_user_preference
urlpatterns = [
    path('', ShowModelsAll.as_view()),
    path('aqSFrOMAEQgBlduCuYfr', ajax_call, name='aqSFrOMAEQgBlduCuYfr'),
    path('AZVTNbMJfPHKWIorjAIz', ajax_call_get_path, name='AZVTNbMJfPHKWIorjAIz'),
    path('McXordmafUNDsqgjmyIE', ajax_call_create_model_create_path, name='McXordmafUNDsqgjmyIE'),
    path('ImMLywRmaWEhXzjCkaxl', save_user_preference, name='ImMLywRmaWEhXzjCkaxl')
]
