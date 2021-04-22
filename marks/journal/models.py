from django.db import models
import uuid

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.utils import timezone

# Create your models here.

def validateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

class Term(models.Model):
    """
        Описание модели Семестр
    """
    number = models.AutoField(blank=False, primary_key=True)
    start_date = models.DateField(default=timezone.now, help_text="Выберете дату начала")
    end_date = models.DateField(default=timezone.now, help_text="Выберете дату конца семестра")
    
    isCurrentTerm = models.BooleanField(help_text="Это текущий семестр?")
    
    def __str__(self):
        return "{0}".format(self.number)



class Specialty(models.Model):
    """
        Описание модели Специальность
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для предмета на семестр")
    name = models.TextField()
    
    def __str__(self):
        return self.name



class Group(models.Model):
    """
        Описание модели Группа
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для группы")
    name = models.TextField(blank=False, help_text="Пожалуйста, введите название группы")
    
    first_term = models.IntegerField(help_text="Пожалуйста, выберете первый семестр для группы")
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, help_text="Пожалуйста, выберете специальность группы")
    terms = models.ManyToManyField(Term)
    
    def __str__(self):
        return self.name
        
#Term(models.Model).groups = models.ManyToManyField(Group)

class Student(models.Model):
    """
        Описание модели Студент
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для студента")
    name = models.TextField(blank=False, help_text="Пожалуйста, введите имя студента")
    last_name = models.TextField(blank=False, help_text="Пожалуйста, введите фамилию студента")
    patronymic = models.TextField(null=True, blank=True, help_text="Пожалуйста, введите отчество студента(если есть)")
    
    email = models.EmailField(null=True, blank=True, validators=[validateEmail], help_text="Пожалуйста, введите почту")
    password = models.TextField(null=True, blank=True, help_text="Пожалуйста, введите пароль")
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.last_name+ " " + self.name + " " + self.patronymic



class Subject(models.Model):
    """
        Описание модели Предмет
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для предмета")
    name = models.TextField(blank=False, help_text="Пожалуйста, введите название предмета")
    specialties = models.ManyToManyField(Specialty)
    
    def __str__(self):
        return self.name



class SubjectInstance(models.Model):
    """
        Описание модели Предмет на семестр
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для предмета на семестр")
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    def __str__(self):
        return "{0} сем. {1}".format(self.term.number,self.subject.name)



class Lecturer(models.Model):
    """
        Описание модели Преподаватель
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для преподователя")
    name = models.TextField(blank=False, help_text="Пожалуйста, введите имя студента")
    last_name = models.TextField(blank=False, help_text="Пожалуйста, введите фамилию студента")
    patronymic = models.TextField(null=True, blank=True, help_text="Пожалуйста, введите отчество студента(если есть)")
    
    email = models.EmailField(null=True, blank=True, validators=[validateEmail], help_text="Пожалуйста, введите почту")
    password = models.TextField(null=True, blank=True, help_text="Пожалуйста, введите пароль")
    
    subject_instances = models.ManyToManyField(SubjectInstance,blank=True)
    
    def __str__(self):
        return self.last_name+ " " + self.name + " " + self.patronymic



class Task(models.Model):
    """
        Описание модели Задание
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для семестра")
    name = models.TextField(help_text="Пожалуйста, введите название задания")
    bref = models.TextField(null=True, blank=True, help_text="Пожалуйста, введите краткое описание задания")
    
    worth = models.IntegerField(help_text="Пожалуйста, ввдеите ценность задания")
    b_max = models.IntegerField(help_text="Пожалуйста, введите максимальный балл по заданию")
    
    date_of_issue = models.DateField(help_text="Пожалуйста, выберете дату выдачи задания")
    deadline = models.DateField(help_text="Пожалуйста, выберете крайнюю дату задания")
    
    KINDS = [ 
        ("main", "основная"),
        ("additional", "доаолнительная")
    ]
    
    kind = models.TextField(choices=KINDS, blank=False, help_text="Пожалуйста, выберете тип задания")
    
    def isMainWork(self):
        if(self.type=="main"):
            return true
        else:
            return false
    
    subject_instance = models.ForeignKey(SubjectInstance, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name



class Mark(models.Model):
    """
        Описание модели Баллы
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для оценки студента")
    number = models.IntegerField(help_text="Пожалуйста, введите полученный балл студента за задание")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, help_text="Пожалуйста, выберете студента")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, help_text="Пожалуйста, выберете задание")
    
    def __str__(self):
        return "b: {0}".format(self.number)
        