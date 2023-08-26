from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout
from .models import (News, Comment, CustomUser, 
                    TakeAnimalImage, LikesOfPost, 
                    OtclickOfPost, Message, 
                    AnimalImage, OwnAnimal, 
                    CommentForOwnAnimal,LikesOfAnimal,
                    LikesOfTakeAnimalComment)
from .forms import NewsAddModelForm, SignUpForm, NewsChangeModelForm, AnimalAddForm, ProfileChangeModelForm, ChangePasswordForm, AnimalChangeModelForm
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from rest_framework.status import HTTP_200_OK
from .serializers import NewsModelSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import check_password

def get_info_about_new(request, news_id : int):
    if request.method == "GET":
        news = get_object_or_404(News, pk=news_id)
        images = TakeAnimalImage.objects.filter(post_take_animal=news).all()
        comments = Comment.objects.order_by("-created_at").filter(news_id_id = news_id).all()
        return render(request, "news/info_news.html", {"news" : news, "comments" : comments, "images" : images})
    elif request.method == "POST" and request.user.is_authenticated or request.user.has_perm("news.add_comment"):
        user = get_object_or_404(CustomUser,pk=request.user.id)
        news = get_object_or_404(News, pk=news_id)
        content = request.POST.get("content", "")
        comment = Comment(content=content, news_id=news, author_of_comment=user)
        comment.save()
        return redirect(reverse("news:info_news", kwargs={"news_id" : news_id}))

def likes_if_take_animal_comment(request, comment_id : int, author_id : int):
   
    if request.method == "POST":
        comment = Comment.objects.get(pk=comment_id)
        user = CustomUser.objects.get(pk=author_id)
        like, created = LikesOfTakeAnimalComment.objects.get_or_create(author=user, comment=comment)
        if  created:
            comment.likes += 1
            like.bolean = True
            comment.save()
            like.save()
        elif like.bolean:
            comment.likes -= 1
            like.bolean = False
            comment.save()
            like.save()
        else:
            comment.likes += 1
            like.bolean = True
            comment.save()
            like.save()
    return redirect(reverse("news:info_news", args=(comment.news_id.id, )))

# @permission_required("news.add_news", login_url="/login")
@login_required(login_url="/login/")
def add_news(request):
    if request.method == "POST":
        form = NewsAddModelForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_object_or_404(CustomUser,pk=request.user.id)
            # news = News(title = form.cleaned_data['title'], content = form.cleaned_data["content"], author_of_news=user)
            # news.save()
            news = form.save(commit=False)
            news.author_of_news = user
            news.save()
            images = request.FILES.getlist("images")
            
            for image in images:
                TakeAnimalImage.objects.create(post_take_animal=news, image=image)

            return redirect(reverse("news:info_news", kwargs={"news_id": news.id}))
        else:
            return redirect(reverse("news:interface_adding", {"news_add_form" : form}))
    elif request.method == "GET":
        news_add_form = NewsAddModelForm()
        return render(request, "news/add_news.html", {"news_add_form" : news_add_form})
     
def get_all_news(request):
    news = News.objects.order_by("-created_at").all()
    return render(request, "news/get_all_news.html", {"news" : news})

def main_page(request):
    return render(
        request, 
        "news/main_page.html",
    )


class NewsUpdateView(View):
    def get(self, request, news_id : int):
        news = get_object_or_404(News, pk=news_id)
        if request.user == news.author_of_news or request.user.has_perm("news.change_news"): 
            form = NewsChangeModelForm(instance=news)
            return render(request, 'news/change_news.html', {'news_change_form':form, "news_id" : news_id})
        return HttpResponse("Permission denied")

    def post(self, request, news_id : int):
        news = get_object_or_404(News, pk=news_id)
        if request.user == news.author_of_news or request.user.has_perm("news.change_news"):
            form = NewsChangeModelForm(request.POST, request.FILES, instance=news)
            if form.is_valid():
                form.save()
                return redirect(reverse("news:info_news", kwargs={"news_id":news_id}))   
            return render(request, 'news/change_news.html', {'news_change_form':form, "news_id" : news_id})  
        else:
            return HttpResponseRedirect("/error", {"message" : "Error"})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # group = Group.objects.get(name="default")
            # group.customuser.add(user)
            login(request, user)
            return redirect(reverse("news:main"))
        else:
            return render(request, "registration/sign_up.html", {"form": form})
        
    elif request.method == "GET":
        form = SignUpForm()
        return render(
            request,
            "registration/sign_up.html",
            {
                "form" : form
            }
        )
    return render(request, "registration/sign_up.html", {"form": form})
    

def log_out(request):
    logout(request)
    return redirect("/login/")
    
@login_required(login_url="/login/")
def get_profile(request):
    return render(
        request,
        "news/info_user.html"
    )

def comment_delete(request, comment_id : int, news_id : int):
    comment = get_object_or_404(Comment, pk=comment_id)
    news = get_object_or_404(News, pk=news_id)
    if comment.author_of_comment == request.user or request.user.has_perm("news.delete_comment") or news.author_of_news == request.user:
        comment.delete()
    return redirect(reverse("news:info_news", kwargs={"news_id" : news_id}))


def delete_news(request, news_id : int, user_id : int):
    news = get_object_or_404(News, pk=news_id)
    if news.author_of_news == request.user or request.user.has_perm("news.delete_news"):
        news.delete()
    return redirect(reverse("news:all_news"))


def likes_post(request, news_id : int, author_id : int):
   
    if request.method == "POST":
        post = News.objects.get(pk=news_id)
        user = CustomUser.objects.get(pk=author_id)
        like, created = LikesOfPost.objects.get_or_create(author=user, post=post)
        if  created:
            post.likes += 1
            like.bolean = True
            post.save()
            like.save()
        elif like.bolean:
            post.likes -= 1
            like.bolean = False
            post.save()
            like.save()
        else:
            post.likes += 1
            like.bolean = True
            post.save()
            like.save()
    return redirect(reverse("news:info_news", args=(news_id, )))

def otclick_post(request, news_id : int, author_id : int):
   
    if request.method == "POST":
        post = News.objects.get(pk=news_id)
        user = CustomUser.objects.get(pk=author_id)
        otclick, created = OtclickOfPost.objects.get_or_create(author=user, post=post)
        if  created:
            post.otclick += 1
            otclick.bolean = True
            post.save()
            otclick.save()
        elif otclick.bolean:
            post.otclick -= 1
            otclick.bolean = False
            post.save()
            otclick.save()
        else:
            post.otclick += 1
            otclick.bolean = True
            post.save()
            otclick.save()
    return redirect(reverse("news:info_news", args=(news_id, )))

# @login_required(login_url="/login/")
class direct(View):
    def get(self, request, sender_id : int, receiver_id : int):
        messages = Message.objects.filter(
                                        Q(sender=sender_id, receiver=receiver_id) |
                                        Q(sender=receiver_id, receiver=sender_id)
                                    ).order_by("created_at").all()

        return render(request, "news/direct.html", {"messages" : messages, "receiver_id" : receiver_id})
    def post(self, request, sender_id : int, receiver_id : int):
        content = request.POST.get("content", "")
        if request.user.id == sender_id:
            sender = CustomUser.objects.get(pk=sender_id)
            receiver = CustomUser.objects.get(pk=receiver_id)
            Message.objects.create(sender=sender, receiver=receiver, content=content)
            return redirect(reverse("news:direct", args=(sender_id, receiver_id)))
        else:
            return HttpResponseRedirect("/error", {"message" : "Error"}, status=401)

# @login_required(login_url="/login/")
def delete_message(request, sender_id : int, receiver_id : int, message_id : int):
    message = get_object_or_404(Message, pk=message_id)
    if message.sender == request.user:
        message.delete()
        return redirect(reverse("news:direct", args=(sender_id, receiver_id)))
    else:
        return HttpResponseRedirect("/error", {"message" : "Error"}, status=401)

@login_required(login_url="/login/")
def own_direct(request):
    list_with_dict_of_user = Message.objects.filter(receiver=request.user.id).values('sender').distinct()
    list_with_id_of_user = []
    for i in list_with_dict_of_user:
        list_with_id_of_user.append(i["sender"])
    receiver_ids = CustomUser.objects.filter(pk__in=list_with_id_of_user)

    return render(request, "news/own_direct_to_me.html", {"receiver_ids" : receiver_ids})

@login_required(login_url="/login/")
def send_direct(request):
    list_with_dict_of_user = Message.objects.filter(sender=request.user.id).values('receiver').distinct()
    
    list_with_id_of_user = []
    for i in list_with_dict_of_user:
        list_with_id_of_user.append(i["receiver"])
    receiver_ids = CustomUser.objects.filter(pk__in=list_with_id_of_user)
    return render(request, "news/own_direct_to_other.html", {"receiver_ids" : receiver_ids})

def list_of_user(request):
    users = CustomUser.objects.filter(is_superuser=0).all()
    return render(request, "news/users.html", {"users" : users})

def animals_of_user(request, user_id : int):
    user = CustomUser.objects.get(pk=user_id)
    animals = user.owned_animals.order_by("-created_at").all()
    return render(request, "news/animal_of_user.html", {"animals" : animals, "user_id" : user_id})


@login_required(login_url="/login/")
def add_animal(request):
    if request.method == "POST":
        form = AnimalAddForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_object_or_404(CustomUser,pk=request.user.id)
            animal = form.save(commit=False)
            animal.owner = user
            animal.save()
            images = request.FILES.getlist("images")
            print(images)
            
            for image in images:
                AnimalImage.objects.create(animal=animal, image=image)

            return redirect(reverse("news:animals_of_user", kwargs={"user_id": request.user.id}))
        else:
            return redirect(reverse("news:add_animal"))
    elif request.method == "GET":
        animal_add_form = AnimalAddForm()
        return render(request, "news/add_animal.html", {"animal_add_form" : animal_add_form})

def get_info_about_animal(request, animal_id : int):
    if request.method == "GET":
        animal = get_object_or_404(OwnAnimal, pk=animal_id)
        images = AnimalImage.objects.filter(animal=animal).all()
        comments = CommentForOwnAnimal.objects.order_by("-created_at").filter(animal = animal).all()

        return render(request, "news/detail_of_animal.html", {"animal" : animal, "comments" : comments, "images" : images})
    elif request.method == "POST" and request.user.is_authenticated or request.user.has_perm("news.add_comment"):
        user = get_object_or_404(CustomUser,pk=request.user.id)
        animal = get_object_or_404(OwnAnimal, pk=animal_id)
        content = request.POST.get("content", "")
        comment = CommentForOwnAnimal(content=content, animal = animal, author_of_comment=user)
        comment.save()
        return redirect(reverse("news:get_info_about_animal", kwargs={"animal_id" : animal_id}))

def comment_delete_for_animal(request, comment_id : int, animal_id : int):
    comment = get_object_or_404(CommentForOwnAnimal, pk=comment_id)
    animal = get_object_or_404(OwnAnimal, pk=animal_id)
    if comment.author_of_comment == request.user or request.user.has_perm("news.delete_comment") or animal.owner == request.user:
        comment.delete()
    return redirect(reverse("news:get_info_about_animal", kwargs={"animal_id" : animal_id}))

def likes_animal(request, animal_id : int, author_id : int):
   
    if request.method == "POST":
        animal = OwnAnimal.objects.get(pk=animal_id)
        user = CustomUser.objects.get(pk=author_id)
        like, created = LikesOfAnimal.objects.get_or_create(author=user, animal=animal)
        if  created:
            animal.likes += 1
            like.bolean = True
            animal.save()
            like.save()
        elif like.bolean:
            animal.likes -= 1
            like.bolean = False
            animal.save()
            like.save()
        else:
            animal.likes += 1
            like.bolean = True
            animal.save()
            like.save()
    return redirect(reverse("news:get_info_about_animal", kwargs={"animal_id" : animal_id}))

# add_permissions
class EditProfile(View):
    def get(self, request):
        user = get_object_or_404(CustomUser, pk=request.user.id)
        if  request.user.has_perm("news.change_news") or user: 
            form = ProfileChangeModelForm(instance=user)
            return render(request, 'news/user_data_change_form.html', {'form':form})
        return HttpResponse("Permission denied")

    def post(self, request):
        user = get_object_or_404(CustomUser, pk=request.user.id)
        if user or request.user.has_perm("news.change_news"):
            form = ProfileChangeModelForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect(reverse("news:profile"))   
            return redirect(reverse("news:change_data_of_news", kwargs={"form" : form}))     
        else:
            return HttpResponseRedirect("/error", {"message" : "Error"})

class ChangePasswordOfUser(View):
    def get(self, request):
        user = get_object_or_404(CustomUser, pk=request.user.id)
        if  request.user.has_perm("news.change_news") or user: 
            form = ChangePasswordForm()
            return render(request, 'news/password_change_form.html', {'form':form})
        return HttpResponse("Permission denied")

    def post(self, request):
        user = get_object_or_404(CustomUser, pk=request.user.id)
        if user or request.user.has_perm("news.change_news"):
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                if check_password(form.cleaned_data.get("current_password"), user.password):
                    if form.cleaned_data.get("password1") == form.cleaned_data.get("password2"):
                        user.set_password(form.cleaned_data.get("password1"))
                        user.save()
                        login(request, user)
                        return redirect(reverse("news:profile")) 
                    else:
                        form.add_error("password1", "Пароли не совпадают друг с другом")
                        return render(request, 'news/password_change_form.html', {'form':form})
                else:
                    form.add_error("current_password", "Старый пароль пользователя введен некорректно")
                    return render(request, 'news/password_change_form.html', {'form':form})
            return render(request, 'news/password_change_form.html', {'form':form})
        else:
            return HttpResponseRedirect("/error", {"message" : "Error"})

class AnimalUpdateView(View):
    def get(self, request, animal_id : int):
        animal = OwnAnimal.objects.get(pk=animal_id)
        if request.user == animal.owner or request.user.has_perm("news.change_news"): 
            form = AnimalChangeModelForm(instance=animal)
            return render(request, 'news/animal_data_change.html', {'form':form, "animal_id" : animal_id})
        return HttpResponse("Permission denied")

    def post(self, request, animal_id : int):
        animal = OwnAnimal.objects.get(pk=animal_id)
        if request.user == animal.owner or request.user.has_perm("news.change_news"):
            form = AnimalChangeModelForm(request.POST, request.FILES, instance=animal)
            if form.is_valid():
                form.save()
                return redirect(reverse("news:get_info_about_animal", kwargs={"animal_id":animal_id}))    
            return render(request, 'news/animal_data_change.html', {'form':form, "animal_id" : animal_id})
        else:
            return HttpResponseRedirect("/error", {"message" : "Error"})
