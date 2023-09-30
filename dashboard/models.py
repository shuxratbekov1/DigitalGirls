from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class ActiveOr(models.Model):
    active = models.BooleanField(default=True)


class Course(models.Model):
    CHOICE = (
        (1, "Course"),
        (2, 'Logical'),
        (3, 'Digital-City'),
    )
    status = models.SmallIntegerField(choices=CHOICE)
    name = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    course_questions = models.IntegerField(null=True, blank=True)
    logic_questions = models.IntegerField(null=True, blank=True)
    logo = models.ImageField(upload_to='img/course/logo/', null=True, blank=True)
    time = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' -----> ' + self.created_at.strftime('%d-%m')


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    query = RichTextUploadingField(null=True, blank=True)
    optionA = RichTextUploadingField(null=True, blank=True)
    optionB = RichTextUploadingField(null=True, blank=True)
    optionC = RichTextUploadingField(null=True, blank=True)
    optionD = RichTextUploadingField(null=True, blank=True)
    free_option = models.BooleanField(default=False, null=True, blank=True)
    correct_answer = models.CharField(choices=(
        ('a', 'optionA'),
        ('b', 'optionB'),
        ('c', 'optionC'),
        ('d', 'optionD'),
    ), max_length=1, null=True, blank=True)

    def __str__(self):
        return f'{self.course} - > {self.query}'


class QuizResult(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    percentage = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.candidate.name}"


class QuestionResponse(models.Model):
    quiz_result = models.ForeignKey(QuizResult, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = RichTextUploadingField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question} - {self.is_correct}"


class CheckedTelegramBot(models.Model):
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    quantity = models.IntegerField()


class RegisteredUser(models.Model):
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    birth = models.DateField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    information = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    reason = models.TextField()
    hear_from = models.TextField()
    passport = models.ImageField(upload_to='Passports/')
    degree = models.IntegerField(choices=(
        (1, 'bad'),
        (2, 'good'),
        (3, 'best')
    ))
    created_at = models.DateTimeField(auto_now_add=True)
    study_time = models.SmallIntegerField(choices=(
        (1, 'ha'),
        (2, 'yoq')
    ))
    has_certificate = models.BooleanField()
    certificate_file = models.FileField(upload_to='Certificate/', null=True, blank=True)

    def __str__(self):
        return self.name + self.phone


class Studied(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    fathers_name = models.CharField(max_length=155)
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
