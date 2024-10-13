from django import forms
from .models import Chat, Message
from django.core.files.storage import default_storage, FileSystemStorage
from .models import Subreddit
from PIL import Image
from .models import *
from io import BytesIO


class PostSortForm(forms.Form):
    SORT_CHOICES = (
        ('recent', 'Mais Recentes'),
        ('popular', 'Mais Populares'),
    )
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)


class CommentSortForm(forms.Form):
    SORT_CHOICES = (
        ('recent', 'Mais Recentes'),
        ('popular', 'Mais Populares'),
    )
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escreva a sua mensagem...'}))

class ChatForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escreva a sua mensagem...'}))

    class Meta:
        model = Chat
        fields = ['participants', 'subreddit']

class ChatSubredditForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escreva a sua mensagem...'}))

    class Meta:
        model = Message
        fields = ['content', 'subreddit']

class RedditUserEditForm(forms.ModelForm):
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

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True,
                               widget=forms.Select(attrs={'class': 'selectpicker'}))
    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'selectpicker'}),
        required=False
    )

    def clean_interests(self):
        selected_interests = self.cleaned_data.get('interests', [])
        interest_objects = []
        for interest_code in selected_interests:
            interest, created = InterestCategory.objects.get_or_create(name=interest_code)
            interest_objects.append(interest)
        return interest_objects



    class Meta:
        model = RedditUser
        fields = ['profile_picture', 'gender', 'interests']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender not in ['M', 'F', 'N', 'O']:
            raise forms.ValidationError('Escolha uma opção válida para o gênero.')
        return gender

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        print(profile_picture)

        user_profile = RedditUser.objects.get(user=self.instance.user)
        old_profile_picture = user_profile.profile_picture

        if profile_picture == 'default.jpeg' or profile_picture == old_profile_picture:
            return old_profile_picture

        elif profile_picture:
            file_name = f"profile{self.instance.user.username}_{profile_picture.name}"
            fs = FileSystemStorage()
            profile_picture = fs.save(file_name, profile_picture)

            if old_profile_picture and old_profile_picture != 'default.jpeg':
                old_file_path = old_profile_picture.path
                default_storage.delete(old_file_path)
        else:
            profile_picture = 'default.jpeg'

        return profile_picture


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Insira o Título'}),
            'content': forms.Textarea(attrs={'placeholder': 'Insira o Novo Comentário'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Insira o Novo Comentário'}),
        }
