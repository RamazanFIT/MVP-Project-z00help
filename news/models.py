from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='animals_images/default.png')
    groups = models.ManyToManyField(Group, related_name='customuser')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser')
    phone = models.CharField(max_length=14, null=True)

class News(models.Model):
    STATUS_CHOICES = [
        ('taked', 'Подобран'),
        ('not_taked', 'Не подобран'),
    ]
    VARIANTS_OF_PETS = [
        ("cat", "кошка"),
        ("dog", "собака")
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    address = models.CharField(max_length=100)
    mobile_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    author_of_news = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to='animals_images/', blank=True, null=True, default='animals_images/default.png')
    likes = models.IntegerField(default=0)
    otclick = models.IntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="not_taked")
    type = models.CharField(max_length=15, choices=VARIANTS_OF_PETS, default="cat")

    def has_comment(self):
        if len(self.comment_set.all()) != 0:
            return True
        else:
            return False
    
    def __str__(self):
        return self.title

class TakeAnimalImage(models.Model):
    post_take_animal = models.ForeignKey(News, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='animals_images/', blank=True, null=True, default='animals_images/default.png')

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    news_id = models.ForeignKey(News, on_delete=models.CASCADE)
    author_of_comment = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    def __str__(self):
        return self.content

class LikesOfTakeAnimalComment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    bolean = models.BooleanField(null=True)




class LikesOfPost(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(News, on_delete=models.CASCADE)
    bolean = models.BooleanField(null=True)


class OtclickOfPost(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(News, on_delete=models.CASCADE)
    bolean = models.BooleanField(null=True)

class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} - {self.created_at}"

class OwnAnimal(models.Model):
    VARIANTS_OF_PETS = [
        ("cat", "кошка"),
        ("dog", "собака")
    ]
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_animals')
    likes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='animals_images/', blank=True, null=True, default='animals_images/default.png')
    title = models.CharField(max_length=200)
    content = models.TextField(default="", blank=True)
    type = models.CharField(max_length=15, choices=VARIANTS_OF_PETS, default="cat")
    created_at = models.DateTimeField(auto_now_add=True)

class AnimalImage(models.Model):
    animal = models.ForeignKey(OwnAnimal, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='animals_images/', blank=True, null=True, default='animals_images/default.png')

class CommentForOwnAnimal(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    animal = models.ForeignKey(OwnAnimal, on_delete=models.CASCADE)
    author_of_comment = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content

class LikesOfAnimal(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    animal = models.ForeignKey(OwnAnimal, on_delete=models.CASCADE)
    bolean = models.BooleanField(null=True)
