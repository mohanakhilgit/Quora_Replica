from django.db import models

from django.contrib.auth.models import User


def save_question_image(instance, filename):
    return f"images/questions/{instance.short_desc}"+filename


def save_answer_image(instance, filename):
    return f"images/answers/{instance.question.id}/{instance.short_desc}"+filename


class Question(models.Model):
    short_desc = models.CharField(max_length=500, null=True)
    long_desc = models.TextField(null=True)
    image = models.ImageField(upload_to=save_question_image, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, null=True)


    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.user.username
        super(Question, self).save(*args, **kwargs)

    
class Answer(models.Model):
    short_desc = models.CharField(max_length=500, null=True)
    long_desc = models.TextField(null=True)
    image = models.ImageField(upload_to=save_answer_image, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, null=True)


    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.user.username
        super(Answer, self).save(*args, **kwargs)


class LikeCount(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)



