from django.urls import path
from . import views

app_name = 'subreddit'

urlpatterns = [
    path("", views.index, name='index'),
    path("registo/", views.registo, name='registo'),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logoutview, name="logout"),
    path('about_me/',views.about_me, name="about_me"),
    path('perfil/', views.perfilview, name="perfil"),
    path("perfil/<str:username>/", views.perfilview, name="perfil"),
    path('perfil/seguidores/<str:username>/', views.list_followers, name='list_followers'),
    path('perfil/seguindo/<str:username>/', views.list_following, name='list_following'),
    path("chat_privado/<str:username>/", views.chat_privado, name="chat_privado"),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('listar_chats_privados/', views.listar_chats_privados, name='lista_chats_privados'),
    path("adicionar_amigo/<str:friend_username>/", views.follow_friend, name="seguir_amigo"),
    path("remover_amigo/<str:friend_username>/", views.unfollow_friend, name="unfollow_amigo"),
    path("<int:subreddit_id>/criar_post/", views.criar_post, name="criar_post"),
    path("criar_subreddit/", views.criar_subreddit, name="criar_subreddit"),
    path("<int:subreddit_id>/apagar_subreddit/", views.apagar_subreddit, name="apagar_subreddit"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/", views.detalhe_subreddit, name="detalhe_subreddit"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/filtrar_posts/", views.post_filter, name="filtrar_post"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/chat/", views.subreddit_chat, name="subreddit_chat"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/<str:sort_by>/", views.detalhe_subreddit, name="detalhe_subreddit"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/<str:sort_by>/filtrar_posts/", views.post_filter, name="filtrar_post"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/<int:post_id>/vote_post/", views.vote_post, name="vote_post"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/<int:post_id>/ver_detalhe_post/", views.detalhe_post, name="detalhe_post"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/<int:post_id>/ver_detalhe_post/filtrar_comentarios/", views.comment_filter, name="filtrar_comentario"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/<int:post_id>/delete_post/", views.delete_post, name="delete_post"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/<int:post_id>/criar_comentario/", views.criar_comentario, name="criar_comentario"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/<int:post_id>/editar_post/", views.edit_post, name="edit_post"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/<int:post_id>/editar_comentario/<int:comment_id>/",
         views.edit_comment, name="edit_comment"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/<int:post_id>/ver_detalhe_post/<int:comment_id>/", views.vote_comment, name="vote_comment"),
    path("<int:subreddit_id>/ver_detalhe_subreddit/<int:post_id>/delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("chat/", views.chat, name="chat"),


]