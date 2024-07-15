from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Program(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'program'

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    SEX_CHOICES = (
        ('female', 'Female'),
        ('male', 'Male'),
    )
    sex = models.CharField(choices=SEX_CHOICES, max_length=6)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subject(models.Model):
    name = models.CharField(max_length=20)
    subject_code = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'subject'

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=2, unique=True)

    class Meta:
        db_table = 'grade'

    def __str__(self):
        return self.name


class Marks(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    class Meta:
        db_table = 'marks'

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks} marks"
