from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Submission, Choice, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    
    submission = Submission.objects.create(enrollment=enrollment)
    
    # Collect checked choice IDs from request POST data
    selected_ids = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            selected_ids.append(int(value))
            
    for choice_id in selected_ids:
        choice = Choice.objects.get(pk=choice_id)
        submission.choices.add(choice)
        
    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    grade_total = 0
    
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            grade_total += question.grade
            correct_choices = set(question.choice_set.filter(is_correct=True).values_list('id', flat=True))
            user_choices = set(submission.choices.filter(question=question).values_list('id', flat=True))
            if correct_choices == user_choices:
                total_score += question.grade
                
    context = {
        'course': course,
        'submission': submission,
        'total_score': total_score,
        'grade_total': grade_total,
        'passed': total_score >= (grade_total * 0.7) # assuming 70% passing grade
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
