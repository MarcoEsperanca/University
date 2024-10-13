from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
import requests
from django.views.decorators.http import require_POST
from .models import *
from django.contrib import messages
import json
from django.db.models import F
from .models import Comment
from .models import Comment
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.core.files.storage import default_storage
from django.conf import settings
import re
import openai
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import RedditUser, Message
from allauth.socialaccount.models import SocialAccount
import requests
from io import BytesIO
from django.core.files import File


# Create your views here.

openai_api_key = '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'
openai.api_key = openai_api_key

def index(request):

    subreddits = Subreddit.objects.all()

    category_filter = request.GET.get('category_filter')

    if category_filter:
        subreddits = subreddits.filter(Q(category__id=category_filter))

    interest_categories = InterestCategory.objects.all()

    subreddit_search_query = request.GET.get('subreddit_search', '')
    user_search_query = request.GET.get('user_search', '')
    users = []
    following_users = []


    if request.user.is_authenticated:

        if not hasattr(request.user, 'reddituser'):
            country = "PT"
            email = request.user.email
            username = email.split('@')[0]


            google_social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
            profile_picture = google_social_account.get_avatar_url() if google_social_account else 'default.jpeg'
            if profile_picture != 'default.jpeg':
                response = requests.get(profile_picture)
                if response.status_code == 200:
                    image_content = BytesIO(response.content)
                    image_file = File(image_content)

                    fs = FileSystemStorage()
                    profile_picture = fs.save('profile_image.jpeg', image_file)
            reddit_user = RedditUser(user=request.user, country=country,
                                     profile_picture=profile_picture)
            reddit_user.save()

            if not request.user.is_superuser:
                request.user.username = username
                request.user.save()

        following_users = request.user.reddituser.following.all()


    if subreddit_search_query:
        subreddits = subreddits.filter(Q(name__icontains=subreddit_search_query) | Q(description__icontains=subreddit_search_query))
    if user_search_query:
        users = User.objects.filter(Q(username__icontains=user_search_query))
    subreddits_per_page = int(request.GET.get('subreddits_per_page', 10))
    paginator = Paginator(subreddits, subreddits_per_page)
    page_number = request.GET.get('page')

    try:
        subreddits = paginator.page(page_number)
    except PageNotAnInteger:
        subreddits = paginator.page(1)
    except EmptyPage:
        subreddits = paginator.page(paginator.num_pages)
    return render(request, 'subreddit/index.html', {
        'subreddits': subreddits,
        'subreddits_per_page': subreddits_per_page,
        'user_search_query': user_search_query,
        'users': users,
        'following_users': following_users,
        'interest_categories': interest_categories,
        'selected_category_id': int(category_filter) if category_filter else None,
    })


def registo(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        gender = request.POST['gender']
        country = request.POST['country']
        selected_interests = request.POST.getlist('interests')

        if User.objects.filter(username=username).exists():
            return render(request, 'subreddit/registo.html', {
                'error_message': 'O nome de utilizador já está a ser utilizado.'
            })

        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:

            fs = FileSystemStorage()
            profile_picture = fs.save(f"profile_{username}_{profile_picture.name}", profile_picture)
        else:

            profile_picture = 'default.jpeg'

        user = User.objects.create_user(username, email, password)
        reddit_user = RedditUser(user=user, country=country, gender=gender, profile_picture=profile_picture)
        reddit_user.save()

        for interest_name in selected_interests:
            interest, created = InterestCategory.objects.get_or_create(name=interest_name)
            reddit_user.interests.add(interest)

        messages.success(request, 'Registro bem-sucedido! Faça login para continuar.')
        return redirect('subreddit:login')
    else:
        return render(request, 'subreddit/registo.html')




def login_view(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        if recaptcha_response:
            captcha_data = {
                'secret': '6Lf5eYooAAAAALU7LfNVg7Hhm3Jr2lQ_W9Tk3c-F',
                'response': recaptcha_response
            }
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
            result = response.json()
            if result['success']:
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('subreddit:index'))
                else:
                    error_message = 'Dados introduzidos incorretos. Tente novamente.'
                    return render(request, 'subreddit/login.html', {'error_message': error_message})
            else:
                error_message = 'Captcha inválido. Por favor, tente novamente.'
                return render(request, 'subreddit/login.html', {'error_message': error_message})
        else:
            error_message = 'Por favor, prove que não é um robô.'
            return render(request, 'subreddit/login.html', {'error_message': error_message})
    else:
        return render(request, 'subreddit/login.html')


def detalhe_subreddit(request, subreddit_id):
    subreddit = get_object_or_404(Subreddit, pk=subreddit_id)
    posts = Post.objects.filter(subreddit=subreddit)
    posts_per_page = int(request.GET.get('posts_per_page', 10))
    sort_by = request.GET.get('sort_by', 'recent')
    if sort_by == 'recent':
        posts = posts.order_by('-pub_data')
    elif sort_by == 'popular':
        posts = posts.order_by('-likes')
    post_search = request.GET.get('post_search', '')
    if post_search:
        posts = posts.filter(Q(title__icontains=post_search) | Q(content__icontains=post_search))
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'subreddit/detalhe_subreddit.html', {'subreddit': subreddit, 'posts': posts,})


@login_required(login_url="subreddit:login")
def criar_subreddit(request):
    interest_categories = InterestCategory.objects.all()
    formatted_categories = [(category.id, category.get_category_display()) for category in interest_categories]

    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        creator = request.user
        category_id = request.POST.get('category')
        if category_id:
            category = InterestCategory.objects.get(id=category_id)
        else:
            category = None

        new_subreddit = Subreddit(name=name, description=description, creator=creator, category=category)
        new_subreddit.save()
        return redirect('subreddit:index')

    return render(request, 'subreddit/criar_subreddit.html', {'interest_categories': formatted_categories})




@login_required(login_url="subreddit:login")
def apagar_subreddit(request, subreddit_id):
    subreddit = get_object_or_404(Subreddit, pk=subreddit_id)
    if request.user.is_superuser or request.user.id == subreddit.creator.id:
        subreddit.delete()
    return redirect('subreddit:index')


@login_required(login_url="subreddit:login")
def criar_post(request, subreddit_id):
    subreddit = get_object_or_404(Subreddit, pk=subreddit_id)
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']

        if 'image' in request.FILES:
            image = request.FILES['image']

            fs = FileSystemStorage()


            username = request.user.username
            post_image_name = f"post_{username}_{title}_{image.name}"


            image = fs.save(post_image_name, image)
        else:
            image = None

        novo_post = Post(title=title, content=content, subreddit=subreddit, author=request.user,
                         pub_data=timezone.now(), image=image)
        novo_post.save()
        return redirect('subreddit:detalhe_subreddit', subreddit_id=subreddit_id)
    return render(request, 'subreddit/criar_post.html', {'subreddit': subreddit})



@login_required(login_url="subreddit:login")
def criar_comentario(request, subreddit_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        content = request.POST['content']
        author = request.user
        pub_data_comentario = timezone.now()
        if 'image' in request.FILES:
            image = request.FILES['image']

            fs = FileSystemStorage()


            username = request.user.username
            post_image_name = f"comment_{username}_{author}_{image.name}"

            image = fs.save(post_image_name, image)
        else:
            image = None

        if content.startswith('!gpt '):
            command = content[5:]
            response = ask_openai(command)
            new_comment = Comment(content='!gpt ' + command, post=post, author=author, pub_data_comentario=pub_data_comentario, image=image)
            new_comment.save()
            gpt_comment = Comment(content=response, post=post, author=User.objects.get(username='Chat GPT'), pub_data_comentario=pub_data_comentario, image=image)
            gpt_comment.save()
        else:

            new_comment = Comment(content=content, post=post, author=author, pub_data_comentario=pub_data_comentario, image=image)
            new_comment.save()
    return redirect('subreddit:detalhe_post', subreddit_id=subreddit_id, post_id=post_id)



def detalhe_post(request, subreddit_id, post_id):
    try:
        subreddit = get_object_or_404(Subreddit, pk=subreddit_id)
        post = get_object_or_404(Post, pk=post_id)
        comments = Comment.objects.filter(post=post)
        comments_per_page = int(request.GET.get('comments_per_page', 10))
        if comments_per_page not in [10, 25, 50]:
            comments_per_page = 10
        paginator = Paginator(comments, comments_per_page)
        page_number = request.GET.get('page')
        try:
            comments = paginator.page(page_number)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        return render(request, 'subreddit/detalhe_post.html', {
            'subreddit': subreddit,
            'post': post,
            'comments': comments,
            'comments_per_page': comments_per_page,
        })
    except Post.DoesNotExist:
        return HttpResponseRedirect(reverse('subreddit:index'))


@login_required(login_url="subreddit:login")
def vote_post(request, subreddit_id, post_id):
    subreddit = get_object_or_404(Subreddit, pk=subreddit_id)
    post = get_object_or_404(Post, pk=post_id)
    vote_type = request.POST.get('vote_type')
    if vote_type == 'like':
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
            post.likes -= 1
        else:
            post.liked_by.add(request.user)
            post.likes += 1

            if request.user in post.disliked_by.all():
                post.disliked_by.remove(request.user)
                post.dislikes -= 1
    elif vote_type == 'dislike':
        if request.user in post.disliked_by.all():
            post.disliked_by.remove(request.user)
            post.dislikes -= 1
        else:
            post.disliked_by.add(request.user)
            post.dislikes += 1

            if request.user in post.liked_by.all():
                post.liked_by.remove(request.user)
                post.likes -= 1
    post.save()
    referer = request.META.get('HTTP_REFERER')
    if 'ver_detalhe_post' in referer:
        return redirect(f'{referer}#post-{post_id}')
    elif 'ver_detalhe_subreddit' in referer:
        referer = re.sub(r'\?page=\d+', '', referer)
        referer = f"{referer}?page=1#post-{post_id}"
        return redirect(referer)
    else:
        return redirect('subreddit:index')

@login_required(login_url="subreddit:login")
def delete_post(request, subreddit_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.is_superuser or request.user.id == post.author.id:
        if post.image:
            default_storage.delete(post.image.name)
        post.delete()
    return redirect('subreddit:detalhe_subreddit', subreddit_id=subreddit_id)


@login_required(login_url="subreddit:login")
def vote_comment(request, subreddit_id, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        vote_type = request.POST.get('vote_type')
        user = request.user
        if vote_type == 'like':
            if user in comment.liked_by_comment.all():
                comment.liked_by_comment.remove(user)
                comment.likes -= 1
            else:
                comment.liked_by_comment.add(user)
                comment.likes += 1
                if user in comment.disliked_by_comment.all():
                    comment.disliked_by_comment.remove(user)
                    comment.dislikes -= 1
        elif vote_type == 'dislike':
            if user in comment.disliked_by_comment.all():
                comment.disliked_by_comment.remove(user)
                comment.dislikes -= 1
            else:
                comment.disliked_by_comment.add(user)
                comment.dislikes += 1
                if user in comment.liked_by_comment.all():
                    comment.liked_by_comment.remove(user)
                    comment.likes -= 1
        comment.save()
        referer = request.META.get('HTTP_REFERER')
        if 'ver_detalhe_subreddit' in referer:
            return redirect(f'{referer}#comment-{comment_id}')
        elif 'ver_detalhe_post' in referer:
            referer = re.sub(r'\?page=\d+', '', referer)
            referer = f"{referer}?page=1#comment-{comment_id}"
            return redirect(referer)
        else:
            return redirect('subreddit:detalhe_post', subreddit_id=subreddit_id, post_id=post_id)


@login_required(login_url="subreddit:login")
def delete_comment(request, subreddit_id, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user.is_superuser or request.user.id == comment.author.id:
        if comment.image:
            default_storage.delete(comment.image.name)
        comment.delete()
    return redirect('subreddit:detalhe_post', subreddit_id=subreddit_id, post_id=post_id)


def post_filter(request, subreddit_id):
    subreddit = get_object_or_404(Subreddit, pk=subreddit_id)
    posts = Post.objects.filter(subreddit=subreddit)
    sort_option = request.GET.get('sort_by')
    if sort_option == 'popular':
        posts = posts.order_by('-likes', '-dislikes')
    elif sort_option == 'recent':
        posts = posts.order_by('-pub_data')
    posts_per_page = int(request.GET.get('posts_per_page', 10))
    paginator = Paginator(posts, posts_per_page)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'subreddit/detalhe_subreddit.html', {
        'subreddit': subreddit,
        'posts': posts,
        'sort_option': sort_option,
        'posts_per_page': posts_per_page,
    })

def comment_filter(request, subreddit_id, post_id):
    subreddit = get_object_or_404(Subreddit, pk=subreddit_id)
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    sort_form = CommentSortForm(request.GET)
    if sort_form.is_valid():
        sort_option = sort_form.cleaned_data['sort_by']
        if sort_option == 'popular':
            comments = comments.order_by('-likes', 'dislikes')
        elif sort_option == 'recent':
            comments = comments.order_by('-pub_data_comentario')
    return render(request, 'subreddit/detalhe_post.html',
                  {'subreddit': subreddit, 'post': post, 'comments': comments, 'sort_form': sort_form})


def about_me(request):
    return render(request, 'subreddit/about_me.html')

@login_required(login_url="subreddit:login")
def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('subreddit:index'))


@login_required(login_url="subreddit:login")
def perfilview(request, username=None):
    if not username:
        user = request.user
    else:
        user = get_object_or_404(User, username=username)

    user_posts = Post.objects.filter(author=user)
    user_subreddits = Subreddit.objects.filter(creator=user)

    num_seguidores = user.reddituser.followers.count()
    num_seguindo = user.reddituser.following.count()

    is_own_profile = user == request.user

    user_interests = user.reddituser.interests.all()

    return render(request, 'subreddit/perfil.html', {
        'user_posts': user_posts,
        'user_subreddits': user_subreddits,
        'num_seguidores': num_seguidores,
        'num_seguindo': num_seguindo,
        'user': user,
        'is_own_profile': is_own_profile,
        'gender': user.reddituser.gender,
        'user_interests': user_interests,
    })

def list_followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.reddituser.followers.all()

    search_query_followers = request.GET.get('search_query_followers')
    if search_query_followers:
        followers = followers.filter(Q(username__icontains=search_query_followers))
    return render(request, 'subreddit/followers_following.html', {
        'users': followers,
        'title': 'Seguidores de {}'.format(user.username)
    })

def list_following(request, username):
    user = get_object_or_404(User, username=username)
    following_users = user.reddituser.following.all()

    search_query_following = request.GET.get('search_query_following')
    if search_query_following:
        following_users = following_users.filter(Q(username__icontains=search_query_following))
    return render(request, 'subreddit/followers_following.html', {
        'users': following_users,
        'title': 'Seguindo {}'.format(user.username)
    })


@login_required(login_url="subreddit:login")
def chat(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            sender = request.user
            Message.objects.create(sender=sender, content=content)
    messages = Message.objects.all()
    form = MessageForm()
    return render(request, 'subreddit/chat.html', {'messages': messages, 'form': form})



@login_required(login_url="subreddit:login")
def subreddit_chat(request, subreddit_id):
    subreddit = get_object_or_404(Subreddit, id=subreddit_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            sender = request.user
            message = content
            if message.startswith('!gpt '):
                command = message[5:]
                response = ask_openai(command)

                Message.objects.create(sender=sender, content='!gpt ' + command, subreddit=subreddit)
                Message.objects.create(sender=User.objects.get(username='Chat GPT'), recipient=sender, content=response, subreddit=subreddit)
            else:
                Message.objects.create(sender=sender, content=message, subreddit=subreddit)
    query = request.GET.get('q')
    if query:
        messages = Message.objects.filter(subreddit=subreddit).filter(Q(sender__username__icontains=query) | Q(content__icontains=query))
    else:
        messages = Message.objects.filter(subreddit=subreddit)
    form = MessageForm()
    return render(request, 'subreddit/chat.html', {'subreddit': subreddit, 'messages': messages, 'form': form})


@login_required(login_url="subreddit:login")
def follow_friend(request, friend_username):
    friend = get_object_or_404(User, username=friend_username)
    user_profile = RedditUser.objects.get(user=request.user)
    friend_profile = RedditUser.objects.get(user=friend)
    if friend != request.user and not user_profile.following.filter(username=friend_username).exists():
        user_profile.following.add(friend)
        friend_profile.followers.add(request.user)
    return redirect('subreddit:index')


@login_required(login_url="subreddit:login")
def unfollow_friend(request, friend_username):
    friend = get_object_or_404(User, username=friend_username)
    user_profile = RedditUser.objects.get(user=request.user)
    friend_profile = RedditUser.objects.get(user=friend)
    if user_profile.following.filter(username=friend_username).exists():
        user_profile.following.remove(friend)
        friend_profile.followers.remove(request.user)
    return redirect('subreddit:index')


@login_required(login_url="subreddit:login")
def editar_perfil(request):
    reddit_user = RedditUser.objects.get(user=request.user)
    if request.method == 'POST':
        form = RedditUserEditForm(request.POST, request.FILES, instance=reddit_user)
        if form.is_valid():
            form.save()
    else:
        form = RedditUserEditForm(instance=reddit_user)
    return render(request, 'subreddit/editar_perfil.html', {'form': form})

def edit_post(request, subreddit_id, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                new_image = form.cleaned_data.get('image')
                if new_image and new_image != post.image:

                    if post.image:
                        default_storage.delete(post.image.name)
                else:

                    form.cleaned_data['image'] = post.image
                form.save()
                return redirect('subreddit:detalhe_post', subreddit_id=subreddit_id, post_id=post_id)
        else:
            form = PostForm(instance=post)
        return render(request, 'subreddit/edit_post.html', {'form': form, 'post': post})
    else:
        return redirect('subreddit:detalhe_post', subreddit_id=subreddit_id, post_id=post_id)



def edit_comment(request, subreddit_id, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        if request.method == 'POST':
            form = CommentForm(request.POST, request.FILES, instance=comment)
            if form.is_valid():
                new_image = form.cleaned_data.get('image')
                if new_image and new_image != comment.image:

                    if comment.image:
                        default_storage.delete(comment.image.name)
                else:

                    form.cleaned_data['image'] = comment.image
                comment.pub_data_comentario = timezone.now()
                form.save()
                return redirect('subreddit:detalhe_post', subreddit_id=subreddit_id, post_id=post_id)
        else:
            form = CommentForm(instance=comment)
        return render(request, 'subreddit/edit_comment.html', {'form': form, 'comment': comment})
    else:
        return redirect('subreddit:detalhe_post', subreddit_id=subreddit_id, post_id=post_id)



@login_required(login_url="subreddit:login")
def chat_privado(request, username):
    recipient = User.objects.get(username=username)
    chat, created = Chat.objects.get_or_create(subreddit=None, is_private=True)
    chat.participants.add(request.user, recipient)
    form = MessageForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            content = form.cleaned_data['content']
            sender = request.user
            recipient = recipient

            if recipient.username == 'Chat GPT':
                if content.startswith('!gpt '):
                    command = content[5:]
                    response = ask_openai(command)
                    original_message = Message.objects.create(sender=sender, content=content, recipient=recipient,
                                                              subreddit=chat.subreddit)
                    chat.messages.add(original_message)
                    gpt_response_message = Message.objects.create(sender=recipient, content=response, recipient=sender,
                                                                  subreddit=chat.subreddit)
                    chat.messages.add(gpt_response_message)
                else:
                    message = Message.objects.create(sender=sender, content=content, recipient=recipient,
                                                     subreddit=chat.subreddit)
                    chat.messages.add(message)
                form = MessageForm()
            else:
                message = Message.objects.create(sender=sender, content=content, recipient=recipient, subreddit=chat.subreddit)
                chat.messages.add(message)
                form = MessageForm()

    query = request.GET.get('q_privado')
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user))

    if query:
        messages = messages.filter(Q(sender__username__icontains=query) | Q(content__icontains=query))
    messages = messages.order_by('timestamp')
    sender_profile_picture = request.user.reddituser.profile_picture.url
    return render(request, 'subreddit/chat.html', {'messages': messages, 'form': form, 'chat': chat, 'sender_profile_picture': sender_profile_picture, 'recipient': recipient})




@login_required(login_url="subreddit:login")
def listar_chats_privados(request):
    user = request.user
    usuarios_seguindo = user.reddituser.following.all()
    usuarios_com_mensagens = User.objects.filter(
        Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
    ).distinct()
    todos_os_usuarios = list(usuarios_seguindo) + list(usuarios_com_mensagens)
    search_query_participants = request.GET.get('search_query_participants', '')
    usuarios_filtrados = todos_os_usuarios
    if search_query_participants:
        usuarios_filtrados = [usuario for usuario in todos_os_usuarios if search_query_participants.lower() in usuario.username.lower()]

    ultimas_mensagens = {}

    for participant in usuarios_filtrados:
        mensagens = Message.objects.filter(
            Q(sender=user, recipient=participant) | Q(sender=participant, recipient=user)
        ).order_by('-timestamp')
        ultima_mensagem = mensagens.first()
        ultimas_mensagens[participant] = ultima_mensagem

    return render(request, 'subreddit/lista_chats_privados.html',
                  {'usuarios_seguindo': usuarios_filtrados, 'ultimas_mensagens': ultimas_mensagens,
                   'search_query_participants': search_query_participants})


def handler404(request, exception):
    return render(request, 'subreddit/404.html', status=404)

def handler500(request, *args, **kwargs):
    return render(request, 'subreddit/500.html', status=500)


def ask_openai(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.7
    )
    answer = response['choices'][0]['text'].strip()

    if answer.startswith("? "):
        answer = answer[2:]
    last_period_index = answer.rfind(".")
    if last_period_index != -1:
        answer = answer[:last_period_index + 1]

    return answer