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
    return render(request, "poll/vote_form.html", {"question_list": question})


# 일반 사용자의 투표 처리
# 투표를 정상적으로 완료하면 감사 페이지로 이동
# 투표가 정상적으로 완료되지 않으면 투표 폼으로 이동
def vote(request):
    # 모든 질문 조회
    questions = Question.objects.all()
    selected_choices = []

    # 질문별로 선택된 값 확인
    for question in questions:
        choice_key = f"choice_{question.pk}"
        choice_pk = request.POST.get(choice_key)

        # 선택값이 없을 경우 에러 메시지와 함께 폼 반환
        if not choice_pk:
            return render(
                request,
                "poll/vote_form.html",
                {
                    "error_msg": "설문이 완료되지 않았습니다.",
                    "question_list": questions,
                },
            )

        # 선택된 choice 저장
        selected_choices.append(choice_pk)

    # 선택값 처리
    for choice_pk in selected_choices:
        choice = Choice.objects.get(pk=choice_pk)
        choice.votes += 1
        choice.save()

    # 완료 페이지로 이동
    return render(request, "poll/vote_finish.html")


# 로그인한 관리자일 때 투표 결과보기
@login_required
def vote_result(request):
    question = Question.objects.all()
    return render(request, "poll/vote_result.html", {"question_list": question})
