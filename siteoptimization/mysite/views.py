from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.http import HttpResponse
from .forms import *
from .models import *
from django.template import loader

# Create your views here.

def index(request):
    context = {}
    context['title'] = "Главная страница"
    return render(request, 'mysite/Index.html', context)


def add_values(request):
    if request.method == "POST":
        if "SaveInput" in request.POST:
            form = FormInputData(request.POST)
            form.save()
            return HttpResponseRedirect(reverse('AddValues'))
        elif "SaveOgranic" in request.POST:
            form = FormOgranichenie(request.POST)
            form.save()
            return HttpResponseRedirect(reverse('AddValues'))
        elif "DeleteInput" in request.POST:
            pk = request.POST.get('DeleteInput')
            input = InputData.objects.get(id=pk)
            input.delete()
            return HttpResponseRedirect(reverse('AddValues'))
        elif "DeleteOrganic" in request.POST:
            pk = request.POST.get('DeleteOrganic')
            input = Ogranichenie.objects.get(id=pk)
            input.delete()
            return HttpResponseRedirect(reverse('AddValues'))

    context = {
        'title': "Добавление данных",
        'input': InputData.objects.all(),
        'ogranic': Ogranichenie.objects.all(),
        'last_pk': InputData.objects.last(),
        'count_ogranic': Ogranichenie.objects.count(),
        'count_input': InputData.objects.count(),
        'last_pk_organic': Ogranichenie.objects.last(),
        'formInput': FormInputData(),
        'formOgranic': FormOgranichenie(),
    }

    return render(request, "mysite/InputData.html", context)

def calculate(request):
    context = {
        'title': 'Расчет',
        'input': InputData.objects.all(),
        'ogranic': Ogranichenie.objects.all(),
    }

    if Ogranichenie.objects.count() == 1:
        for x in OutputData.objects.all():
            x.delete()

        if OutputData.objects.google()['coef']:
            google = OutputData.objects.google()
            lst = google.get('coef')
            for i,l in enumerate(lst):
                OutputData.objects.create(NameFactory=f'A{i+1}', CostWorkshopId1=l[0], CostWorkshopId2=l[1], CostWorkshopId3=l[2], CostWorkshopId4=l[3], PowerFactory=l[0]+l[1]+l[2]+l[3])

            context['output'] = OutputData.objects.all()
            context['cost'] = int(google.get('cost'))
        else:
            context['output'] = None
    return render(request, 'mysite/Calculation.html', context)