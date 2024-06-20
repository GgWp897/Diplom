from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    nickname = models.CharField('Имя', max_length=256)
    email = models.CharField('Email', max_length=256)
    password = models.CharField('Пароль', max_length=256)
    image = models.ImageField('Аватар', upload_to='AvatarImage/')
    key = models.CharField('Ключевое слово', max_length=256)
    is_online = models.BooleanField('В сети', default=False) 
    groups = models.ManyToManyField('Group', through='GroupMembership', related_name='users')

    def __str__(self):
        return self.email
    def save(self, *args, **kwargs):
        is_new_user = self.pk is None
        if is_new_user or 'password' in kwargs.get('update_fields', []):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    @property
    def status(self):
        message_count = self.statements.count()
        if message_count <= 100:
            return "Новичок"
        elif message_count <= 200:
            return "Стажёр"
        elif message_count <= 300:
            return "Опытный"
        elif message_count <= 400:
            return "Профессионал"
        elif message_count <= 500:
            return "Ветеран"
        elif message_count <= 600:
            return "Мастер"
        else:
            return "Легенда"



class Tag(models.Model):
    name = models.CharField('Название тега', max_length=100, unique=True)

    def __str__(self):
        return self.name



class News(models.Model):
    name = models.CharField('Заголовок', max_length=512)
    text = models.TextField('Текст новости')
    date = models.DateField('Дата')
    img = models.ImageField('Изображение', upload_to='news_static/')
    tags = models.ManyToManyField(Tag, verbose_name='Теги', related_name='news')
    video = models.FileField('Видео', upload_to='videos/', blank=True, null=True)

    def has_video(self):
        return self.video is not None and self.video != ''
    def __str__(self):
        return self.name



class Comments(models.Model):
    text = models.TextField('Комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE, related_name='comments_to_post')
    date = models.DateTimeField('Дата комментария', auto_now_add=True)

    def __str__(self):
        return f"комментарий от {self.user} для {self.post.name}"



class Posts(models.Model):
    name = models.CharField('Название', max_length=512)
    text = models.TextField('Текст')
    image = models.ImageField('Изображение', upload_to='PostImage')
    date = models.DateField('Дата')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comments, related_name='posts_commented', blank=True)

    def __str__(self):
        return self.name



class Group(models.Model):
    name = models.CharField('Название группы', max_length=256)
    description = models.TextField('Описание группы', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    imageHead = models.ImageField('Шапка', upload_to='ImageHeader/')
    imageAvatar = models.ImageField('Изображение группы', upload_to='ImageAvatar/')

    def __str__(self):
        return self.name



class GroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    joined_at = models.DateTimeField('Дата вступления', auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} в {self.group.name}'



class DiscussionTopic(models.Model):
    title = models.CharField('Тема обсуждения', max_length=256)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='discussion_topics')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    content = models.TextField('Содержание темы', blank=True)

    def __str__(self):
        return self.title



class Meme(models.Model):
    text = models.TextField('текст мемаса')
    image = models.ImageField('Изображение', blank=True)
    date = models.DateTimeField('Дата')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    likes = models.ManyToManyField('User', related_name='liked_memes', blank=True)

    def __str__(self):
        return self.text



class Statement(models.Model):
    full_text = models.TextField('Полный текст')
    date = models.DateField('Дата')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statements')
    discussionTopic = models.ForeignKey(DiscussionTopic, on_delete=models.CASCADE, related_name='statements')
    image = models.ImageField('Изображение', blank=True, null=True, upload_to='StatementImage/')

    def __str__(self):
        return self.full_text
    


class Cup(models.Model):
    name = models.CharField(max_length=255)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    


class ConstructorsCup(models.Model):
    team = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.team



class Schedule(models.Model):
    stage = models.CharField('Этап', max_length = 256)
    time = models.DateTimeField('Время')

    def __str__(self):
        return self.stage