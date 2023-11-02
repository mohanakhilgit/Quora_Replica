from django.urls import path

from .views import home, add_question, add_answer, like_answer


urlpatterns = [
    path('', home, name='home'),
    path('add-question/', add_question, name='add_question'),
    path('add-answer/<int:question_id>/', add_answer, name='add_answer'),
    path('like-answer/<int:answer_id>', like_answer, name='like_answer')
]