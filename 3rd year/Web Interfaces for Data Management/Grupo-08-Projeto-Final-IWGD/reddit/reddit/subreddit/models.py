from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter


GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Prefiro não dizer'),
    )

INTEREST_CHOICES = (
        ('AN', '⛩ Anime'),
        ('CINE', '📽️ Cinema'),
        ('DES', '⚽ Desporto'),
        ('EDU', '📖 Educação'),
        ('IT', '🖥️ IT'),
        ('JOG', '🎮 Jogos'),
        ('VIG', '🗺️ Viagens'),
    )


class InterestCategory(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_category_display(self):
        category_choices = {
            'AN': '⛩ Anime',
            'CINE': '📽️ Cinema',
            'DES': '⚽ Desporto',
            'EDU': '📖 Educação',
            'IT': '🖥️ IT',
            'JOG': '🎮 Jogos',
            'VIG': '🗺️ Viagens',
        }
        return category_choices.get(self.name, 'Desconhecido')


class RedditUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    profile_picture = models.ImageField(null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    interests = models.ManyToManyField(InterestCategory, choices=INTEREST_CHOICES,
                                       related_name='users_interested', blank=True)

    def __str__(self):
        return self.user.username

    def get_following_users(self):
        return self.following.all()

    def is_following(self, username):
        user_to_follow = User.objects.get(username=username)
        return self.following.filter(id=user_to_follow.id).exists()

    def get_gender_display(self):
        gender_choices = {
            'M': 'Masculino',
            'F': 'Feminino',
            'O': 'Outro',
            'N': 'Prefiro não dizer',
        }
        return gender_choices.get(self.gender, 'Desconhecido')

    def get_interests_display(self):
        interest_choices = {
            'AN': '⛩ Anime',
            'CINE': '📽️ Cinema',
            'DES': '⚽ Desporto',
            'EDU': '📖 Educação',
            'IT': '🖥️ IT',
            'JOG': '🎮 Jogos',
            'VIG': '🗺️ Viagens',
        }
        interests_list = []
        for interest in self.interests.all():
            interests_list.append(interest_choices.get(interest.name, 'Desconhecido'))
        return interests_list


class Subreddit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.OneToOneField('Chat', on_delete=models.SET_NULL, null=True, blank=True, related_name='subreddit_chat')
    category = models.ForeignKey(InterestCategory, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name

    def get_category_display(self):
        category_choices = {
            'AN': '⛩ Anime',
            'CINE': '📽️ Cinema',
            'DES': '⚽ Desporto',
            'EDU': '📖 Educação',
            'IT': '🖥️ IT',
            'JOG': '🎮 Jogos',
            'VIG': '🗺️ Viagens',
        }

        return category_choices.get(self.category, 'Desconhecido')


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_data = models.DateTimeField('data de publicacao')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    disliked_by = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.content

    def foi_publicada_recentemente(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_data_comentario = models.DateTimeField('data de publicacao_comentario')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    liked_by_comment = models.ManyToManyField(User, related_name='liked_posts_commment', blank=True)
    disliked_by_comment = models.ManyToManyField(User, related_name='disliked_posts_comment', blank=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.content


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, default=None)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.sender.username} - {self.timestamp}'


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    subreddit = models.ForeignKey(Subreddit, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='chat_subreddit')
    messages = models.ManyToManyField(Message, related_name='chat_messages', blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f'{", ".join([str(participant) for participant in self.participants.all()])}'



class CustomGoogleOAuth2Adapter(OAuth2Adapter):
    def complete_login(self, request, app, token, response):
        user = super(CustomGoogleOAuth2Adapter, self).complete_login(
            request, app, token, response)
        if user:

            if 'picture' in response:
                user.reddituser.profile_picture = response['picture']
                user.reddituser.save()
        return user

@receiver(post_save, sender=RedditUser)
def handle_user_creation(sender, instance, created, **kwargs):
    if created and not Message.objects.filter(sender=instance.user).exists():
        sender_user = User.objects.get(id=23)
        mensagem_boas_vindas = """
        Bem-vindo ao Serit.Inc, o seu novo lar digital! 😊

        Estou aqui para tornar a sua experiência inesquecível! Se você tiver alguma pergunta ou precisar de ajuda, é só digitar !gpt {sua pergunta} e eu farei o meu melhor para fornecer uma resposta inteligente e útil.

        Em Serit.Inc, estamos sempre disponíveis para você, 24 horas por dia, 7 dias por semana. Não hesite em explorar nossos recursos, fazer novos amigos na nossa comunidade e mergulhar em discussões interessantes sobre os tópicos que mais ama.

        Lembre-se, este é mais do que um site; é uma comunidade. Estamos todos juntos nisso, então vamos fazer deste lugar um lar acolhedor para todos.

        Se precisar de ajuda ou quiser saber mais sobre o Serit.Inc, estou aqui para ajudar. Divirta-se explorando!

        Atenciosamente,

        Chat GPT
        Inteligência Artificial do Serit.Inc 🚀
        """
        Message.objects.create(sender=sender_user, recipient=instance.user, content=mensagem_boas_vindas)

