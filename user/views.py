from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from .models import User,Pet,Favorite
from main.models import Location
from user.forms import UserForm,PetForm

# json 처리
from django.http import JsonResponse,HttpResponse
from django.core import serializers
import json
# Create your views here.
def user_login(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.POST['password'])
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            print("인증성공")
            login(request, user)
            return redirect('index')
        else:
            print("인증실패")
            return redirect('user:login')
    # return render(request, "user/login.html")
    return render(request,'base.html')

def user_logout(request):
    logout(request)
    # return redirect("user:login")
    return redirect('index')

def user_signup(request):
    # if request.method == "POST":
    #     print(request.POST)
    #     # username = request.POST["username"]
    #     username = request.POST.get('username')
    #     # password = request.POST["password"]
    #     password = request.POST.get('password')
    #     # lastname = request.POST['lastname']
    #     firstname = request.POST.get('firstname')
    #     # email = request.POST['email']
    #     email = request.POST.get('email')
    #
    #     # gender = request.POST.get('gender')
    #
    #     user = User.objects.create_user(username=username, password=password,first_name=firstname,email=email)
    #     # user.gender = gender
    #     # user.last_name = lastname
    #     # user.email = email
    #
    #     user.save()
    #     # return redirect("user:login")
    #     print("user 생성!")
    #     return redirect('index')
    # return render(request, "user/signup.html")
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
        print(form.GENDER_CHOICES)
        print(form.GENDER_CHOICES)

    return render(request, 'user/signup.html', {'form': form})
    # return render(request, 'navbar.html', {'form': form})

def sociallogin(request):
    return render(request,'base.html')

def mypage(request):
    pet_form = PetForm(request=request,user = request.user)
    # pet_form = PetForm()
    return render(request, 'user/mypage.html', {'pet_form': pet_form})

def pet(request):
    # Post 방식 요청
    if request.method == 'POST':
        form = PetForm(request.POST,request=request,user = request.user)
        print(form)
        # form = PetForm(request.POST)
        # form.fields['user'].queryset = Pet.objects.
        # print(form.is_valid())
        if form.is_valid():
            print("form is valid")
            post = form.save(commit=False)
            post.save()
            return redirect('index')
        return redirect('user:petcreate')

    # Get 방식 요청
    else:
        print("익명님???????")
        print(type(User(request.user)))
        pet_form = PetForm(request=request,user = request.user)
        # pet_form = PetForm()
        return render(request, 'user/mypage.html', {'pet_form': pet_form})
#로그인 추가하기
def favorite(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            location_id = request.POST.get('location_id')
            location = Location.objects.get(id=location_id)
            my_favorite = Favorite.objects.get_or_create(user=request.user, location__id=location_id)
            return HttpResponse(status=201)
        else:
            # favorites = Favorite.objects.all()
            favorites = Favorite.objects.filter(user=request.user)
            favorites_json = json.loads(serializers.serialize('json',favorites,ensure_ascii=False))
            # return HttpResponse(favorites_json,content_type="text/json-comment-filtered")
            return JsonResponse({'reload_all': False, 'favorites_json': favorites_json})
    else:
        #401상태코드
        #https://devlog.jwgo.kr/2020/10/17/fancy-messaging-system-in-django/
        #https://han-py.tistory.com/105
        return HttpResponse(status=401)