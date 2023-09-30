from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .form import *
import datetime
from django.db.models import Count


@login_required(login_url='login')
def Index(request):
    smo = []
    for i in Candidate.objects.filter(season=Season.objects.last()):
        if QuizResult.objects.filter(candidate__season=Season.objects.last(), candidate=i):
            pass
        else:
            smo.append(i)
    date = request.GET.get('date')
    if date is None:
        date = datetime.datetime.now().date()
    else:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    today_s = QuizResult.objects.filter(candidate__created_at__year=date.year, candidate__created_at__month=date.month, candidate__created_at__day=date.day).order_by('-percentage')
    total = RegisteredUser.objects.filter(season=Season.objects.last()).count()

    exam_passed_count = QuizResult.objects.filter(candidate__season=Season.objects.last()).count()
    if exam_passed_count != 0 and total != 0:
        exam_passed_percentage = (exam_passed_count / total) * 100
    else:
        exam_passed_percentage = 0

    excellent_candidate = QuizResult.objects.filter(candidate__season=Season.objects.last(), percentage__gte=60).count()
    if excellent_candidate != 0 and total != 0:
        excellent_candidate_percentage = (excellent_candidate / total) * 100
    else:
        excellent_candidate_percentage = 0

    checked_telegram_bot_percentage = 0
    checked_telegram_bot_count = 0
    if CheckedTelegramBot.objects.filter(season=Season.objects.last()).count() != 0 and total != 0:
        checked_telegram_bot_count = CheckedTelegramBot.objects.last().quantity
        checked_telegram_bot_percentage = (CheckedTelegramBot.objects.all().count() / total) * 100

    obj = QuizResult.objects.filter(candidate__season=Season.objects.last(), percentage__gte=60).order_by('-percentage')

    context = {
        "smo": smo,
        "smo_count": len(smo),
        "today_s": PagenatorPage(today_s, 10, request),
        "todays_count": today_s.count(),
        'courselist': Course.objects.all(),
        'total_candidate': total,

        'exam_passed_count': exam_passed_count,
        'exam_passed_percentage': exam_passed_percentage,

        'excellent_candidate_count': excellent_candidate,
        'excellent_candidate_percentage': excellent_candidate_percentage,

        'checked_telegram_bot_count': checked_telegram_bot_count,
        'checked_telegram_bot_percentage': checked_telegram_bot_percentage,

        'percentage_greater_candidate': PagenatorPage(obj, 10, request),
        "date": date.strftime('%Y-%m-%d'),
        'results': PagenatorPage(obj, 10, request),
    }
    return render(request, 'index.html', context)


@login_required(login_url='login')
def CourseView(request):
    context = {
        'courselist': Course.objects.all(),
    }
    return render(request, 'course.html', context)


@login_required(login_url='login')
def SearchView(request):
    search = request.GET.get('search')
    context = {
        'search_result': QuizResult.objects.filter(candidate__name__icontains=search),
    }
    return render(request, 'search.html', context)


@login_required(login_url='login')
def SearchResultView(request, pk):
    context = {
        'candidate': QuizResult.objects.get(id=pk).candidate,
        'quiz_result': QuizResult.objects.get(id=pk),
        'questions': QuestionResponse.objects.filter(quiz_result_id=pk),
    }
    return render(request, 'search_result.html', context)


@login_required(login_url='login')
def UserAnswerCoursePage(request):
    result = QuizResult.objects.filter(candidate__course__status=1).values('candidate__course_id', 'candidate__course__name').annotate(dcount=Count('id')).distinct()
    context = {
        'courselist': result,
    }
    return render(request, 'user-answer.html', context)


@login_required(login_url='login')
def UserAnswerListPage(request, pk):
    context = {
        'quiz': QuizResult.objects.filter(candidate__course_id=pk).order_by('-percentage'),
    }
    return render(request, 'user-answer-list.html', context)


@login_required(login_url='login')
def UserAnswerQuestionViewPage(request, pk):
    context = {
        'candidate': QuizResult.objects.get(id=pk).candidate,
        'questions': QuestionResponse.objects.filter(quiz_result_id=pk),
        'quiz_result': QuizResult.objects.get(id=pk),
        'pk': QuizResult.objects.get(id=pk).candidate.course.id,
    }
    return render(request, 'user-answer-view.html', context)


@login_required(login_url='login')
def QuestionAdd(request, pk):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            course = Course.objects.get(id=pk)
            query = form.cleaned_data['query']
            if Question.objects.filter(query=query).count() > 0:
                messages.success(request, 'bunday savol mavjud')
                return redirect('questionAdd', pk)
            optionA = form.cleaned_data['optionA']
            optionB = form.cleaned_data['optionB']
            optionC = form.cleaned_data['optionC']
            optionD = form.cleaned_data['optionD']
            free_option = form.cleaned_data['free_option']
            correct_answer = form.cleaned_data['correct_answer']
            Question.objects.create(
                course=course,
                query=query,
                optionA=optionA,
                optionB=optionB,
                optionC=optionC,
                optionD=optionD,
                free_option=free_option,
                correct_answer=correct_answer,
            )
            return redirect('questionAdd', pk)
        return redirect('questionAdd', pk)
    context = {
        'form': QuestionForm,
        'pk': pk,
    }
    return render(request, 'question-add.html', context)


@login_required(login_url='login')
def QuestionList(request, pk):
    context = {
        'questionList': Question.objects.filter(course_id=pk),
        'pk': pk,
    }
    return render(request, 'question-list.html', context)


@login_required(login_url='login')
def DeleteQuestion(request, pk: int):
    q = Question.objects.get(id=pk)
    ids = q.course.id
    Question.objects.get(id=pk).delete()
    return redirect('questionList', ids)


@login_required(login_url='login')
def CandidateList(request):
    object = Candidate.objects.all().order_by('-id')
    context = {
        'candidate_list': object
    }
    return render(request, 'candidate-list.html', context)


def PagenatorPage(List, num, request):
    paginator = Paginator(List, num)
    pages = request.GET.get('page')
    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list


def LoginView(request):
    user = request.user
    if not user.is_anonymous:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = User.objects.filter(username=username)
        if users.count() > 0:
            usr = authenticate(username=username, password=password)
            if usr is not None:
                login(request, usr)
                return redirect('index')
            else:
                return redirect('login')
        else:
            return redirect('login')
    return render(request, 'login.html')


def LogoutView(request):
    logout(request)
    return redirect('login')


def studiedView(request):
    context = {
        'studied': Studied.objects.all()
    }
    return render(request, 'studied.html', context)


def registeredView(request):
    season_id = request.GET.get('season')
    if season_id is None:
        season = Season.objects.last()
    else:
        season = Season.objects.get(id=season_id)
    context = {
        'registered': RegisteredUser.objects.filter(season=season),
        'season': Season.objects.all(),
        'current': season,
    }
    return render(request, 'registered.html', context)


def registeredDetailView(request, pk):
    context = {
        "registered": RegisteredUser.objects.get(id=pk)
    }
    return render(request, 'registered-detail.html', context)
