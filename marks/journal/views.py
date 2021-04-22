from django.shortcuts import render
from .models import SubjectInstance, Lecturer

# Create your views here.


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    current_prepod = Lecturer.objects.get(name = "Татьяна")
    subjects=current_prepod.subject_instances.all()
    name_subjects = list(map(lambda x: x.__str__(), subjects))
    # Доступные книги (статус = 'a')
    #num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    #num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    
    return render(
        request,
        'index.html',
        context={'current_prepod':current_prepod,'subjects':name_subjects, 'range':range(len(name_subjects))},
    )
