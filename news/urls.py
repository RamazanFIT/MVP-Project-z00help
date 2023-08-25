from django.urls import path, include
from . import views

app_name = 'news'


urlpatterns = [
    path("<int:news_id>/", views.get_info_about_new, name="info_news"),
    path("add_news/", views.add_news, name="interface_adding"),
    path("", views.get_all_news, name="all_news"),
    path("main_page/", views.main_page, name="main"),
    path('<int:news_id>/edit/', views.NewsUpdateView.as_view(), name="change_data_of_news"),
    path("sign_up/", views.signup, name="sign_up"),
    path("logout/", views.log_out, name="logout"),
    path("profile/", views.get_profile, name="profile"),
    path("delete_comment/<int:comment_id>/<int:news_id>/", views.comment_delete, name="delete_comment"),
    path("delete_news/<int:news_id>/<int:user_id>/", views.delete_news, name="delete_news"),
    path("inc_like/<int:news_id>/<int:author_id>/", views.likes_post, name="likes_post"),
    path("inc_otclick/<int:news_id>/<int:author_id>/", views.otclick_post, name="otclick_post"),
    path("direct/<int:sender_id>/<int:receiver_id>/", views.direct.as_view(), name="direct"),
    path("direct/delete_message/<int:sender_id>/<int:receiver_id>/<int:message_id>/", views.delete_message, name="delete_message"),
    path("own_direct/", views.own_direct, name="own_direct"),
    path("send_direct/", views.send_direct, name="send_direct"),
    path("list_of_user/", views.list_of_user, name="list_of_user"),
    path("animals_of_user/<int:user_id>/", views.animals_of_user, name="animals_of_user"),
    path("add_animal/", views.add_animal, name="add_animal"),
    path('get_info_about_animal/<int:animal_id>/', views.get_info_about_animal, name="get_info_about_animal"),
    path("comment_delete_for_animal/<int:comment_id>/<int:animal_id>/", views.comment_delete_for_animal, name="comment_delete_for_animal"),
    path("likes_animal/<int:animal_id>/<int:author_id>/", views.likes_animal, name="likes_animal")
    
]