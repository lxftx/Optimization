from django.db import models
from django.contrib.postgres.fields import ArrayField

from ortools.linear_solver import pywraplp
# Create your models here.

class InputData(models.Model):
    NameFactory = models.CharField(max_length=255, verbose_name="Наименование предприятия")
    CostWorkshopId1 = models.IntegerField(verbose_name="Цена 1-ой мастерской")
    CostWorkshopId2 = models.IntegerField(verbose_name="Цена 2-ой мастерской")
    CostWorkshopId3 = models.IntegerField(verbose_name="Цена 3-ей мастерской")
    CostWorkshopId4 = models.IntegerField(verbose_name="Цена 4-ой мастерской")
    PowerFactory = models.IntegerField(verbose_name="Мощность предприятия")

    def __str__(self):
        return self.NameFactory

class OutputDataQuerySet(models.QuerySet):
    def google(self):
        costs = [[x.CostWorkshopId1, x.CostWorkshopId2, x.CostWorkshopId3, x.CostWorkshopId4] for x in InputData.objects.all()]
        supply = [x.PowerFactory for x in InputData.objects.all()]
        demand = list(map(int, [f'{x.SumWorkshopId1} {x.SumWorkshopId2} {x.SumWorkshopId3} {x.SumWorkshopId4}' for x in Ogranichenie.objects.all()][0].split()))

        # Создаем линейную программу
        solver = pywraplp.Solver.CreateSolver('GLOP')

        # Создаем переменные xij
        num_factories = len(costs)
        num_workshops = len(costs[0])

        x = {}
        for i in range(num_factories):
            for j in range(num_workshops):
                x[i, j] = solver.IntVar(0, solver.infinity(), f'x_{i}_{j}')

        # Задаем целевую функцию для минимизации
        solver.Minimize(solver.Sum(costs[i][j] * x[i, j] for i in range(num_factories) for j in range(num_workshops)))

        # Добавляем ограничение на вывоз всех деталей
        for i in range(num_factories):
            solver.Add(solver.Sum(x[i, j] for j in range(num_workshops)) == supply[i])

        # Добавляем ограничение на удовлетворение спроса
        for j in range(num_workshops):
            solver.Add(solver.Sum(x[i, j] for i in range(num_factories)) == demand[j])

        # Решаем задачу
        status = solver.Solve()
        coef = []

        # Выводим результаты
        if status == pywraplp.Solver.OPTIMAL:
            print('Решение найдено:')
            print('Общая стоимость перевозок:', solver.Objective().Value())
            for i in range(num_factories):
                lst = []
                for j in range(num_workshops):
                    lst.append(x[i, j].solution_value())
                    # print(f'x_{i}_{j} =', x[i, j].solution_value())
                coef.append(lst)
        else:

            print('Решение не найдено.')

        d = {
            'cost': solver.Objective().Value(),
            'coef' : coef,
        }

        return d

class OutputData(models.Model):
    NameFactory = models.TextField(verbose_name="Наименование предприятия")
    CostWorkshopId1 = models.IntegerField(verbose_name="Цена 1-ой мастерской")
    CostWorkshopId2 = models.IntegerField(verbose_name="Цена 2-ой мастерской")
    CostWorkshopId3 = models.IntegerField(verbose_name="Цена 3-ей мастерской")
    CostWorkshopId4 = models.IntegerField(verbose_name="Цена 4-ой мастерской")
    PowerFactory = models.IntegerField(verbose_name="Мощность предприятия")

    objects = OutputDataQuerySet.as_manager()

    def __str__(self):
        return self.NameFactory


class Ogranichenie(models.Model):
    SumWorkshopId1 = models.IntegerField(verbose_name='Сумма 1-ой мастерской')
    SumWorkshopId2 = models.IntegerField(verbose_name='Сумма 2-ой мастерской')
    SumWorkshopId3 = models.IntegerField(verbose_name='Сумма 3-ей мастерской')
    SumWorkshopId4 = models.IntegerField(verbose_name='Сумма 4-ой мастерской')