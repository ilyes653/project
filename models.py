from django.db import models
from onlinecourse.models import Lesson, Enrollment

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return f"Question: {self.question_text}"

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).values_list('id', flat=True)
        return set(all_answers) == set(selected_ids)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice: {self.choice_text} (Correct: {self.is_correct})"

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
