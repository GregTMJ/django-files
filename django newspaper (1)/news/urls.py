from django.urls import path
from .views import Postlist, PostDetail # импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', Postlist.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    ]
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view