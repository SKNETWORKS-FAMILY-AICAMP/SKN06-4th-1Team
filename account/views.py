import http
import re
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


# 용어들(변경필요)
# 첫 화면 : chat


# 사용자 가입
def create(request):
    if request.method == "GET":
        return render(
            request, "account/create.html", {"form": CustomUserCreationForm()}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("chat"))
        else:
            return render(request, "account/create.html", {"form": form})


# 사용자 로그인
def login(request):
    if request.method == "GET":
        return render(request, "account/login.html", {"form": AuthenticationForm()})
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            else:
                return redirect(reverse("chat"))
        else:
            return render(
                request,
                "account/login.html",
                {
                    "form": AuthenticationForm(),
                    "error_msg": "아이디나 비밀번호를 다시 확인해주세요.",
                },
            )


# 사용자 로그아웃
@login_required
def logout(request):
    logout(request)
    return redirect(reverse("chat"))


# 사용자 정보 조회
@login_required
def detail(request):
    object = User.objects.get(pk=request.user.pk)
    return render(request, "account/detail.html", {"user": object})


# 사용자 비밀번호 변경
@login_required
def pwd_change(request):
    http_method = request.method
    if http_method == "GET":
        form = PasswordChangeForm(user=request.user)
        return render(request, "account/pwd_change.html", {"form": form})
    elif http_method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse("account:detail"))
        else:
            return render(
                request,
                "account/pwd_change.html",
                {"form": form, "error_msg": "유효하지 않은 비밀번호입니다."},
            )


# 사용자 정보 수정
@login_required
def update(request):
    if request.method == "GET":
        object = User.objects.get(pk=request.user.pk)
        form = CustomUserChangeForm(instance=object)
        return render(request, "account/update.html", {"form": form})
    elif request.method == "POST":
        object = User.objects.get(pk=request.user.pk)
        form = CustomUserChangeForm(request.POST, request.FILES, instance=object)
        if form.is_valid():
            form.save()
            return redirect(reverse("account:detail"))
        else:
            return render(request, "account/update.html", {"form": form})


# 사용자 탈퇴
@login_required
def delete(request):
    request.user.delete()
    logout(request)
    return redirect(reverse("chat"))
