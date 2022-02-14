from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from .forms import LoginForm
from .models import Profile
from .forms import UserEditForm
from .forms import ProfileEditForm
from .models import Post
from .forms import CommentForm
from .forms import EmailPostForm
from .forms import PostForm
from .forms import AddPostForm
from django.utils.text import slugify
from django.db.models import Count


# обязательна авторизация
@login_required
def edit(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def edit_post(request, author_id, post_id):
    #post = Post.objects.get()
    post = get_object_or_404(Post, author_id=author_id, id=post_id)
    post_form = PostForm(instance=post)
    if request.method == 'POST':
        post_form = PostForm(instance=post,
                                      data=request.POST,
                                      files=request.FILES)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'Profile updated successfully')
            posts = request.user.post.all()
            return render(request, 'account/images.html', {'posts': posts})
        else:
            messages.error(request, 'Error updating your profile')
    return render(request, 'account/edit_image.html', {'post_form': post_form})


@login_required  # авторизован ли польз-ль
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


@login_required
def my_posts(request):
    posts = request.user.post.all()
    return render(request, 'account/images.html', {'posts': posts})


@login_required
def posts(request, author, author_id):
    #author = get_object_or_404(Profile, author_id=author_id)
    posts = Post.objects.all().filter(author_id=author_id)  #get_object_or_404(Post, author_id=author_id) - это только для одного объекта
    return render(request, 'blog/post/posts.html', {'posts': posts, 'author': author})


@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = AddPostForm(data=request.POST, files=request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.slug = slugify(new_post.name, allow_unicode=True)
            new_post.full_clean()
            new_post.save()
            #posts = Post.objects.all().filter(author_id=request.user.id)
            #print(posts)
            posts = request.user.post.all()
            return render(request, 'account/images.html', {'posts': posts})
    else:
        post_form = AddPostForm()
    return render(request, 'blog/post/add_post.html', {'post_form': post_form})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month,
                             publish__day=day)
    comment_form = CommentForm()
    # список активных комменов для статьи
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # взяли коммент но еще не сохранили в БД
            new_comment = comment_form.save(commit=False)
            new_comment.name = request.user.username
            new_comment.email = request.user.email
            # привязка коммента к статье
            new_comment.post = post
            # сохр-е коммента в БД
            new_comment.save()
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'profile': Profile})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')  # получение данных по id
    sent = False
    form = EmailPostForm()

    if request.method == 'POST':  # иначе отображается пустая форма
        form = EmailPostForm(request.POST)  # форма отправлена на сохр-ие методом POST
        if form.is_valid():  # данные формы прошли валидацию
            cd = form.cleaned_data  # получаем введенные данные (если бы форма была не валидна, то сюда прошли бы только корректные данные)
            # отправка по email
            post_url = request.build_absolute_uri(post.get_absolute_url())  # ссылка на статью
            subjects = '{} ({}) recommends your reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments {}'.format(post.title, post_url, cd['name'], cd['comments'])
            #send_mail(subjects, message, 'admin@admin.ru', cd['to'])
            sent = True  # успешная отправка

        else:
            form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})


def people(request):
    people = Profile.objects.all()  #register_people.exclude(id=request.user.profile.id,)  # register_people
    return render(request, 'account/people.html', {'people': people})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])  # сверка с данными в базе на коррект-ь; возврат User пр успешной аутент-ии
            if user is not None:
                if user.is_active:
                    login(request, user)  # авторизация на сайте (сохр-ие в сессии)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login or password!')
        else:
            return HttpResponse('Invalid form')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # создание нового поль-я но без добавдения в БД
            new_user = user_form.save(commit=False)
            # задаем польз-ю зашифрованный пароль
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)

            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})