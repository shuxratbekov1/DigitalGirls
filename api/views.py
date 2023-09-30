from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
import random


@api_view(['GET'])
def getCourse(request):
    query = Course.objects.filter(status=1)
    ser = CourseSerializer(query, many=True)
    return Response(ser.data)


@api_view(['POST'])
def registerCandidate(request):
    course = request.POST.get('course')
    name = request.POST.get('name')
    phone_number = request.POST.get('phone_number')
    if Candidate.objects.filter(phone_number=phone_number):
        data = {
            "success": False,
        }
    else:
        candidate = Candidate.objects.create(
            course_id=course,
            season=Season.objects.last(),
            name=name,
            phone_number=phone_number,
        )
        data = {
            "success": True,
            'candidate_id': CandidateSerializer(candidate).data
        }
    return Response(data)


@api_view(['GET'])
def getQuestion(request):
    try:
        candidate_id = request.GET.get('candidate_id')
        course = Candidate.objects.get(id=candidate_id).course
        query = Question.objects.filter(course_id=course)

        course_questions = random.sample(list(query), k=course.course_questions)
        query_ser = QuestionSerializer(course_questions, many=True)

        logic_q = Question.objects.filter(course__status=2)
        logic_questions = random.sample(list(logic_q), k=course.logic_questions)
        logic_ser = QuestionSerializer(logic_questions, many=True)

        dc_questions = Question.objects.filter(course__status=3)
        dc_ser = QuestionSerializer(dc_questions, many=True)

        data = {
            "success": True,
            "course": query_ser.data,
            "logic": logic_ser.data,
            'dc': dc_ser.data
        }
    except Exception as err:
        data = {
            "success": False,
            "error": f'{err}'
        }
    return Response(data)


@api_view(['POST'])
def responseUserAnswer(request):
    result = request.data['resultData']
    candidate = request.data['candidate_id']
    q = QuizResult.objects.create(candidate_id=candidate)
    total = 0
    wrong = 0
    correct = 0
    for i in result:
        question = Question.objects.get(id=i['id'])
        if question.free_option:
            QuestionResponse.objects.create(
                quiz_result=q,
                question_id=i['id'],
                answer=i['answer'],
            )
        else:
            if question.correct_answer == i['answer'].lower():
                QuestionResponse.objects.create(
                    quiz_result=q,
                    question_id=i['id'],
                    answer=i['answer'],
                    is_correct=True,
                )
                total += 1
                correct += 1
            else:
                QuestionResponse.objects.create(
                    quiz_result=q,
                    question_id=i['id'],
                    answer=i['answer'],
                    is_correct=False,
                )
                total += 1
                wrong += 1
    q.total = total
    q.wrong = wrong
    q.correct = correct
    percentage = (100/total) * correct
    q.percentage = percentage
    q.save()
    return Response({'success': True})


@api_view(['POST'])
def CheckedTelegramBotView(request):
    if CheckedTelegramBot.objects.filter(season=Season.objects.last()).exists():
        ch = CheckedTelegramBot.objects.last()
        ch.quantity += 1
        ch.save()
    else:
        CheckedTelegramBot.objects.create(quantity=1, season=Season.objects.last())
    ids = request.data.get("id_decimal")
    if ids is None:
        return Response({"success": False, 'balans': 0})
    else:
        return Response({"success": True, "balans": 12000})


@api_view(['GET'])
def active_view(request):
    ac = ActiveOr.objects.last()
    if ac.active:
        data = {
            "success": True
        }
    else:
        data = {
            "success": False
        }
    return Response(data)


@api_view(['GET'])
def check_candidate_view(request):
    try:
        name = request.GET.get('name')
        l_name = request.GET.get('l_name')
        phone = request.GET.get('phone')
        r = RegisteredUser.objects.filter(name__icontains=name, l_name__icontains=l_name, phone=phone)
        if len(r) > 0:
            data = {
                "success": True,
                'data': RegisteredUserSerializer(r[0]).data,
            }
        else:
            data = {
                "success": False
            }
        return Response(data)
    except Exception as err:
        print(f'{err}')
        return Response(" ")


@api_view(['POST'])
def register_user(request):
    try:
        name = request.data['name']
        l_name = request.data['l_name']
        birth = request.data['birth']
        address = request.data['address']
        phone = request.data['phone']
        information = request.data['information']
        course = request.data['course']
        reason = request.data['reason']
        hear_from = request.data['hear_from']
        passport = request.FILES['passport']
        degree = request.data['degree']
        study_time = request.data['time']
        has_certificate = request.data['has_certificate']
        certificate_file = request.FILES.get('certificate_file')
        RegisteredUser.objects.create(
            season=Season.objects.last(),
            name=name,
            l_name=l_name,
            birth=birth,
            address=address,
            phone=phone,
            degree=degree,
            information=information,
            course_id=course,
            reason=reason,
            hear_from=hear_from,
            passport=passport,
            study_time=study_time,
            has_certificate=has_certificate,
            certificate_file=certificate_file if certificate_file else None,
        )
        data = {
            "success": True,
        }
    except Exception as err:
        print(f'{err}')
        data = {
            "success": False,
            'error': f'{err}'
        }
    return Response(data)
