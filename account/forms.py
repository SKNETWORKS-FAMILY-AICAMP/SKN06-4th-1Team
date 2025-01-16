# Form 클래스 정의
## 등록폼, 수정폼 두가지 정의

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,  # 사용자 등록폼
    UserChangeForm,  # 사용자 수정폼
)
from .models import User
from datetime import datetime


# 사용자 등록 폼폼
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # form field에 명시할 항목
        fields = [
            "username",
            "password1",
            "password2",
            "name",
            "state",
            "birthday",
            "profile_img",
        ]

        # Input type을 변경.
        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date"}),
        }

    # 이름이 올바르게 입력되었는지 확인 (2자 이상상)
    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 2:
            raise forms.ValidationError("이름은 2글자 이상 입력하세요.")
        return name

    # 나이가 올바르게 입력되었는지 확인 (8 ~ 100세)
    def clean_birthday(self):
        birthday = self.cleaned_data["birthday"]
        this_year = datetime.now().year
        if (this_year - birthday.year < 8) or (this_year - birthday.year > 100):
            raise forms.ValidationError("나이가 범주를 벗어났습니다.")
        return birthday


# 사용자 정보 수정 폼
class CustomUserChangeForm(UserChangeForm):
    password = None  # password 변경링크 미표기

    class Meta:
        model = User
        fields = ["name", "state", "birthday", "profile_img"]

        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date"}),
        }

    # 이름이 올바르게 입력되었는지 확인 (2자 이상상)
    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 2:
            raise forms.ValidationError("이름은 2글자 이상 입력하세요.")
        return name

    # 나이가 올바르게 입력되었는지 확인 (8 ~ 100세)
    def clean_birthday(self):
        birthday = self.cleaned_data["birthday"]
        this_year = datetime.now().year
        if (this_year - birthday.year < 8) or (this_year - birthday.year > 100):
            raise forms.ValidationError("나이가 범주를 벗어났습니다.")
        return birthday
