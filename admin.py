from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Enrollment, Submission

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'pub_date']
    search_fields = ['name', 'description']

# Register models with admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Enrollment)
