from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User, News, Statement, Cup, ConstructorsCup, Schedule, Posts, Comments, DiscussionTopic, Group, GroupMembership, Tag
from django.db.models import Q
from django.utils import timezone
from .forms import NewsFilterForm
from .models import Meme


def auth(request):
    errorAuth = ''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email = email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect(account)
            else:
                errorAuth = 'Ошибка в пароле'
        except User.DoesNotExist:
            errorAuth = 'Ошибка в почте'
    return render(request, 'auth.html', {'errorAuth': errorAuth})


def newPassword(request):
    error = ''
    if request.method == 'POST':
        email = request.POST['email']
        key = request.POST['key']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email, key=key)
            user.password = password
            user.save(update_fields=['password'])
            return redirect(auth)
        except User.DoesNotExist:
            error = 'Ошибка в почте или ключевом слове!'
    return render(request, 'newPassword.html', {'error':error})
    

def reg(request):
    errorReg = ''
    if request.method == 'POST':
        nickname = request.POST['nickname']
        email = request.POST['email']
        password = request.POST['password']  
        if not User.objects.filter(Q(email=email) | Q(nickname=nickname)).exists():
            if all([nickname, email, password]):
                if (len(password)>7):
                    user = User(nickname=nickname, email=email, password=password)
                    user.save()
                    request.session['user_id'] = user.id
                    return redirect(account)
                else:
                    errorReg = 'Пароль слишком короткий'
            else:
                errorReg = 'Поле или поля пусты'  
        else:
            errorReg = 'Такой пользователь уже существует'
    return render(request, 'auth.html', {'errorReg': errorReg})


def groups(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        query = request.GET.get('q') 
        if query:
            groups = Group.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        else:
            groups = Group.objects.all()
        return render(request, 'groups.html', {'user': user, 'groups': groups})
    return redirect('auth')


@require_POST
def like_meme(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        meme_id = request.POST.get('meme_id')
        meme = Meme.objects.get(pk=meme_id)

        if user in meme.likes.all():
            meme.likes.remove(user)
            liked = False
        else:
            meme.likes.add(user)
            liked = True

        return JsonResponse({'likes_count': meme.likes.count(), 'liked': liked})
    return JsonResponse({'error': 'User not authenticated'}, status=403)


def group(request, group_id):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        group = get_object_or_404(Group, pk=group_id)
        memes = Meme.objects.filter(group=group)
        is_member = GroupMembership.objects.filter(user=user, group=group).exists()

        if request.method == 'POST':
            if 'join_group' in request.POST:
                GroupMembership.objects.create(user=user, group=group)
                return redirect('group', group_id=group.id)
            if 'leave_group' in request.POST:
                GroupMembership.objects.filter(user=user, group=group).delete()
                return redirect('group', group_id=group.id)

        return render(request, 'group.html', {'user': user, 'group': group, 'memes': memes, 'is_member': is_member})
    return redirect('auth')


def group_topics(request, group_id):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        group = get_object_or_404(Group, pk=group_id)
        discussion_topics = DiscussionTopic.objects.filter(group=group)
        is_member = GroupMembership.objects.filter(user=user, group=group).exists()
        if request.method == 'POST':
            if 'join_group' in request.POST:
                GroupMembership.objects.create(user=user, group=group)
                return redirect('group_topics', group_id=group.id)
            elif 'leave_group' in request.POST:
                GroupMembership.objects.filter(user=user, group=group).delete()
                return redirect('group_topics', group_id=group.id)
        return render(request, 'group_topics.html', {'user': user, 'group': group, 'discussion_topics': discussion_topics, 'is_member': is_member})
    return redirect('auth')


def discussionTopic(request, topic_id):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        topic = get_object_or_404(DiscussionTopic, pk=topic_id)
        group = topic.group
        is_member = GroupMembership.objects.filter(user=user, group=group).exists()
        if not is_member:
            return redirect('group', topic_id)
        statements = Statement.objects.filter(discussionTopic=topic)
        if request.method == 'POST':
            full_text = request.POST['full_text']
            image = request.FILES.get('image')
            current_date = timezone.now().date()
            new_statement = Statement(
                full_text=full_text,
                date=current_date,
                discussionTopic=topic,
                user=user,
                image=image
            )
            new_statement.save()

        return render(request, 'discussionTopic.html', {'user': user, 'topic': topic, 'statements': statements})
    return redirect('auth')


def news(request):
    news_list = News.objects.all().order_by('-date')
    query = request.GET.get('q') 
    
    if query:
        news_list = news_list.filter(tags__name__icontains=query)

    filter_form = NewsFilterForm(request.GET)
    if filter_form.is_valid():
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')
        if start_date:
            news_list = news_list.filter(date__gte=start_date)
        if end_date:
            news_list = news_list.filter(date__lte=end_date)

    return render(request, 'news.html', {'news': news_list, 'filter_form': filter_form})


def newsPage(request, news_id):
    news = News.objects.get(pk=news_id)
    return render(request, 'newsPage.html', {'news': news})


def contacts(request):
    return render(request, 'contacts.html')


def standingsPilots(request):
    cup = Cup.objects.all().order_by('-points')
    return render(request, 'standingsPilots.html', {'cup': cup})


def standingsConstructors(request):
    cup = ConstructorsCup.objects.all().order_by('-points')
    return render(request, 'standingsConstructors.html', {'cup': cup})


def schedule(request):
    schedule = Schedule.objects.all()
    return render(request, 'schedule.html', {'schedule':schedule})


def account(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        posts = Posts.objects.filter(user=user)        
        if request.method == 'POST':
            if 'image' in request.FILES:
                user.image = request.FILES['image']
            if 'nickname' in request.POST:
                user.nickname = request.POST['nickname']
            if 'key' in request.POST:
                user.key = request.POST['key']
            if 'is_online' in request.POST:  
                user.is_online = request.POST['is_online'] == 'on'
            user.save()
        statements_count = Statement.objects.filter(user=user).count()
        user_groups = GroupMembership.objects.filter(user=user)
        return render(request, 'account.html', {'user': user, 'statements_count': statements_count, 'posts': posts, 'user_groups': user_groups})
    return redirect('auth')


def addPost(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        if request.method == 'POST':
            name = request.POST['name']
            text = request.POST['text']
            image = request.FILES.get('image')
            date = timezone.now().date()            
            comment_ids = request.POST.getlist('comments')
            post = Posts.objects.create(name=name, text=text, image=image, date=date, user=user)
            comments = Comments.objects.filter(pk__in=comment_ids)
            post.comments.set(comments)
            return redirect(addPost)
        return render(request, 'addPost.html')
    else:
        return redirect(auth)
    


def deletePost(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('account')
    return render(request, 'deletePost.html', {'post': post})


    
def posts(request):
    if 'user_id' in request.session:
        posts = Posts.objects.all()
        return render(request, 'posts.html', {'posts':posts})
    else:
        return redirect(auth)


    
def postPage(request, post_id):
    if 'user_id' in request.session:
        post = Posts.objects.get(pk=post_id)
        comments = Comments.objects.filter(post=post)

        if request.method == 'POST':
            user_id = request.session.get('user_id')
            user = User.objects.get(pk=user_id)
            comment_text = request.POST.get('comment_text')
            Comments.objects.create(text=comment_text, user=user, post=post)
            return redirect('postPage', post_id=post.id)
        return render(request, 'postPage.html', {'post': post, 'comments': comments})
    return redirect('home')
    


def logOut(request):
    logout(request)
    return redirect(news)