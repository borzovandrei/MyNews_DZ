from django.shortcuts import render, get_object_or_404
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import auth

from News.models import Tutor, Course
from News.forms import SignupForm, SigninForm

from django.http import Http404
from .models import Article, Like, Comment


def home(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, "News/home.html", context)


def about(request):
    return render(request, 'News/about.html')


def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, "News/article.html", {'article': article})






def main(request):
    tutors = Tutor.objects.all()

    return render(request, 'News/main.html', {
        'tutors': tutors
    })


def signup(request):
    redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect(redirect)
    else:
        form = SignupForm()

    return render(request, 'News/signup.html', {
        'form': form
    })


def signin(request):
    redirect = request.GET.get('continue', '/success')
    if request.method == "POST":
        form = SigninForm(request.POST)

        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(redirect)
    else:
        form = SigninForm()
    return render(request, 'News/signin.html', {
        'form': form
    })


@login_required(redirect_field_name='continue')
def login_success(request):
    return render(request, 'News/success.html')


def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)


class TutorView(View):
    def get(self, request, id):
        tutor = Tutor.objects.get(id=int(id))

        print(tutor)
        courses = Course.objects.filter(tutor=tutor).all()

        return render(request, 'News/tutor.html', {
            'tutor': tutor,
            'courses': courses
        })




@login_required
def like(request, post_id):
    try:
        post = Article.objects.get(id=post_id)
        if request.POST.get('delete') == 'True':
            Like.objects.filter(user=request.user, post=post).delete()
        else:
            Like.objects.get_or_create(user=request.user, post=post)
    except Article.DoesNotExist:
        raise Http404

    return HttpResponseRedirect('%s#comment' % reverse('article', args=[post_id]))


@login_required
def add_comment(request, post_id):
    try:
        post = Article.objects.get(id=post_id)
        text = request.POST.get('comment')
        if text:
            Comment.objects.create(user=request.user, text=text, post=post)
        else:
            Like.objects.get_or_create(user=request.user, post=post)
    except Article.DoesNotExist:
        raise Http404

    return HttpResponseRedirect('%s#comment' % reverse('article', args=[post_id]))




class CreatePostForm(forms.ModelForm):


    def __init__(self, user, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Article
        fields = ('image', 'title', 'text')

    def save(self, commit=False):
        instance = super(CreatePostForm, self).save(commit=False)
        instance.user = self.user

        return instance

@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save(True)
            return redirect('home')
    else:
        form = CreatePostForm(request.user)

    return render(request, 'News/create_post.html', {'form': form})
