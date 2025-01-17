import http
from random import choice
import re
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from poll.models import Question, Choice


# 일반 사용자가 투표하는 설문폼
def vote_form(request):
    # question은 전체 질문과 보기를 가지고 있는 객체
    question = Question.objects.all()
    return render(request, "poll/vote_form.html", {"question": question})


# 일반 사용자의 투표 처리
# 투표를 정상적으로 완료하면 감사 페이지로 이동
# 투표가 정상적으로 완료되지 않으면 투표 폼으로 이동
def vote(request):
    # 모든 질문의 pk를 받아오는 객체
    question = request.POST.getlist("question")
    # 1. 각 질문의 choice가 하나라도 비어있을 시 error 메시지와 함께 폼 반환
    # 2. 각 질문의 choice가 전부 채워져있다면 각 질문의 choice의 votes를 1씩 증가
    choices = request.POST.getlist("choice")
    if len(choices) < len(question):
        return render(
            request,
            "poll/vote_form.html",
            {
                "error_msg": "설문이 완료되지 않았습니다.",
                "question": question,
            },
        )
    else:
        for i in range(len(choices)):
            choice = Choice.objects.get(pk=choices[i])
            choice.votes += 1
            choice.save()
        return render(request, "poll/vote_finish.html")


# 로그인한 관리자일 때 투표 결과보기
@login_required
def vote_result(request):
    question = Question.objects.all()
    return render(request, "poll/vote_result.html", {"question": question})
