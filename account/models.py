from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import forms


# User 모델
class User(AbstractUser):
    # Field 정의 - table 컬럼
    name = models.CharField(
        verbose_name="이름",
        max_length=50,  # varcha(50)
    )
    gender = models.CharField(
        verbose_name="성별",
        max_length=50,  # varchar(50)
        null=True,
    )
    state = models.CharField(
        verbose_name="지역",
        max_length=50,  # varchar(50)
    )
    birthday = models.DateField(
        verbose_name="생년월일",
    )
    profile_img = models.ImageField(
        verbose_name="프로필 사진",
        default="images/default.jpg",
        upload_to="images/%Y/%m/%d",  # 저장경로
        blank=True,
    )

    def __str__(self):
        return f"username: {self.username}, name: {self.name}"
