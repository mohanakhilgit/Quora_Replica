from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

from question.models import Question, Answer, LikeCount


def home(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'home.html', context)


def add_question(request):
    if not request.user.is_authenticated:
        messages.error(request, "Login first to post question")
        return redirect('login_user')
    
    if request.method == 'POST':
        short_desc = request.POST.get('short_desc')
        long_desc = request.POST.get('long_desc')
        image = request.FILES.get('image')

        question = Question(
            short_desc=short_desc,
            long_desc=long_desc,
            image=image,
            user=request.user,
        )

        question.save()

        messages.success(request, "Question posted successfully")
        return redirect('home')

    return render(request, 'add_question.html')


def add_answer(request, question_id):
    if not request.user.is_authenticated:
        messages.error(request, "Login first to post an answer")
        return redirect('login_user')
    
    try:
        question = Question.objects.get(id=question_id)

    except Question.DoesNotExist:
        messages.error(request, "Question not found!")
        return redirect('home')
    
    
    if request.method == 'POST':
        short_desc = request.POST.get('short_desc')
        long_desc = request.POST.get('long_desc')
        image = request.FILES.get('image')

        question = Answer(
            short_desc=short_desc,
            long_desc=long_desc,
            image=image,
            question=question,
            user=request.user,
        )

        question.save()

        messages.success(request, "Answer posted successfully")
        return redirect('home')

    return render(request, 'add_answer.html', {'question': question})


def like_answer(request, answer_id):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'Login first to like an answer'})
    
    if request.method == 'POST':
        try:
            answer = Answer.objects.get(id=answer_id)

        except Answer.DoesNotExist:
            return JsonResponse({"error": "Answer not found!"})
        
        if not LikeCount.objects.filter(answer=answer, user=user).exists() and answer.user != user:
            LikeCount.objects.create(answer=answer, user=user)
            return JsonResponse({"success": "Liked"})
