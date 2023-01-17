from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from datetime import datetime
from .models import Test, Input, Lesson, Lecture, Linkage
import json as json
import importlib.util
from .testGeneration.base import Literal
from django.http import JsonResponse
    
def demo(request, name, id):
    if request.method == 'GET':
        test = Test.objects.get(id = id)

        title = test.title
        descr = test.description

        return render(request, 'adauga_cod.html', {'name': title, 'descr': descr, 'data': id})

def get_output(request, id):
    test = Test.objects.get(id = id)
    inputs = Input.objects.filter(test_id = id)
    jsonData = {
        'testCases': []
    }
    spec = importlib.util.spec_from_file_location(test.output_generator, 'sources/' + test.title + '.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for i in range(test.no_test_cases):
        inputData = {}
        for item in inputs:
            generator = Literal(item.name, item.data_type, item.values)
            inputData[item.name] = generator.getValue()
        jsonData['testCases'].append(
            {
                'input': inputData,
                'output': module.solve(inputData)
            }
        )
    
    return JsonResponse(jsonData)

def welcome(request, name):
    if request.method == 'GET':
        if name == "Oana":
            return render(request, 'welcome-prof.html', {'name': name})

        tests = Test.objects.filter(homework=0, exercise=0)
        return render(request, 'welcome.html', {'name': name, 'tests': [i+1 for i in range(len(tests))]})

def view_course(request, name):
    id = request.GET['id']
    lesson = Lesson.objects.get(id=id)

    noEx = 0
    noHw = 0

    for item in Linkage.objects.filter(lesson=lesson):
        if item.test.exercise == 1:
            noEx += 1
        else:
            noHw += 1

    context =  {}
    context["lessons"] = range(1, len(Lecture.objects.filter(lesson = lesson))+1)
    context["exercises"] = range(1,noEx+1)
    context["homeworks"] = range(1,noHw+1)

    return render(request, 'vizualizare_extinsa_curs.html', context)

def show_courses(request, name):
    usr = User.objects.get(last_name=name)

    if name == 'Oana':
        lessons = Lesson.objects.filter(teacher=usr)
    else:
        lessons = Lesson.objects.all()

    context = {}
    context['lessons'] = []
    for lesson in lessons:
        context['lessons'].append(
            {
                'id': lesson.id,
                'title': lesson.name,
                'descr': lesson.description,
                't_name': lesson.teacher.last_name
            }
        )
    context['name'] = name

    return render(request, 'view_courses.html', context)

def add_course(request, name):
    if name != "Oana":
        return render(request, 'error.html', {'err': 401}, content_type="text/html", status=401)
    context = {}
    context["name"] = name

    if len(request.GET) == 0:
        context["page_data"] = json.dumps({
            "name": name,
            "title": "",
            "descr": "",
            "img": "",
            "lessons": 0,
            "exercises": 0,
            "homeworks": 0,
            "lessonsData": [],
            "exercisesData": [],
            "homeworksData": [],
        })
        context["title"] = ""
        context["descr"] = ""
    else:
        jsonD = json.loads(request.GET["context"])
        context["page_data"] = request.GET["context"]
        context["title"] = jsonD["title"]
        context["descr"] = jsonD["descr"]
        context["lessons"] = range(jsonD["lessons"])
        context["exercises"] = range(jsonD["exercises"])
        context["homeworks"] = range(jsonD["homeworks"])
        context["context"] = request.GET["context"]
    
    if request.method == 'POST':
        lesson = Lesson(
            name = request.POST['title'],
            description = request.POST['descr'],
            teacher = User.objects.get(last_name=name)
        )

        lesson.save()

        if not request.POST['context']:
            return redirect('/main/' + name)

        contextJSON = json.loads(request.POST['context'])
        for i in range(contextJSON['lessons']):
            jsonObj = json.loads(contextJSON['lessonsData'][i])
            l = Lecture(
                title = jsonObj['title'],
                description = jsonObj['descr'],
                lesson = lesson
            )
            l.save()

        for i in range(contextJSON['exercises']):
            jsonObj = json.loads(contextJSON['exercisesData'][i])
            l = Test(
                title = jsonObj['title'],
                description = jsonObj['descr'],
                output_generator = jsonObj['output'],
                no_test_cases = 6,
                save_sources = 0,
                homework = 0,
                exercise = 1,
                due_date = datetime.now(),
                start_date = datetime.now(),
            )
            with open("sources/" + l.title + ".py", "x") as f:
                f.write(l.output_generator)

            l.save()

            for item in jsonObj['input'].split('\n'):
                arr = item.split(' ')
                val = ""

                for i in range(2, len(arr)):
                    if arr[i][-1] == '\n' or arr[i][-1] == '\r':
                        arr[i] = arr[i][:-1]
                    val += arr[i]

                inputD = Input(
                    data_type = arr[0],
                    name = arr[1],
                    test = l,
                    values = val
                )

                inputD.save()
            lnk = Linkage(
                lesson = lesson,
                test = l
            )
            lnk.save()

        for i in range(contextJSON['homeworks']):
            jsonObj = json.loads(contextJSON['homeworksData'][i])
            l = Test(
                title = jsonObj['title'],
                description = jsonObj['descr'],
                output_generator = jsonObj['output'],
                no_test_cases = 6,
                save_sources = 0,
                homework = 1,
                exercise = 0,
                due_date = jsonObj['date'],
                start_date = datetime.now(),
            )
            with open("sources/" + l.title + ".py", "x") as f:
                f.write(l.output_generator)

            l.save()

            for item in jsonObj['input'].split('\n'):
                arr = item.split(' ')
                val = ""

                for i in range(2, len(arr)):
                    if arr[i][-1] == '\n' or arr[i][-1] == '\r':
                        arr[i] = arr[i][:-1]
                    val += arr[i]

                inputD = Input(
                    data_type = arr[0],
                    name = arr[1],
                    test = l,
                    values = val
                )

                inputD.save()
            lnk = Linkage(
                lesson = lesson,
                test = l
            )
            lnk.save()
        return redirect('/main/' + name)
    return render(request, 'adauga_curs.html', context)

def add_lesson(request, name):
    if name != "Oana":
        return render(request, 'error.html', {'err': 401}, content_type="text/html", status=401)

    if 'edit' in request.GET:
        jsonObj = json.loads(json.loads(request.GET['context'])['lessonsData'][int(request.GET['edit'])])
        print(jsonObj)
        return render(request, 'add_lesson.html', {'context': request.GET['context'], 'name': name, 
            'titleEdit': jsonObj["title"],
            'descrEdit': jsonObj["descr"],
            'idEdit': jsonObj["id"]})
    else:
        return render(request, 'add_lesson.html', {'context': request.GET['context'], 'name': name})

def add_lesson2(request, name):
    if request.method == 'POST':
        if request.POST['idEdit']:
            context = request.POST['context']
            jsonD = json.loads(context)
            obj = json.loads(jsonD["lessonsData"][int(request.POST['idEdit'])])
            obj['title'] = request.POST['title']
            obj['descr'] = request.POST['descr']
            jsonD["lessonsData"][int(request.POST['idEdit'])] = json.dumps(obj)
        else:
            context = request.POST['context']
            jsonD = json.loads(context)
            jsonD["lessons"] += 1
            jsonD["lessonsData"].append(json.dumps({
                    "id": jsonD["lessons"] - 1,
                    "title": request.POST["title"],
                    "descr": request.POST["descr"]
                })
            )

        return redirect('/main/' + name + '/courses/add?context=' + json.dumps(jsonD))


def add_ex(request, name):
    if name != "Oana":
        return render(request, 'error.html', {'err': 401}, content_type="text/html", status=401)

    if 'edit' in request.GET:
        jsonObj = json.loads(json.loads(request.GET['context'])['exercisesData'][int(request.GET['edit'])])
        print(jsonObj)
        return render(request, 'add_ex.html', {'context': request.GET['context'], 'name': name, 
            'title': jsonObj["title"],
            'descr': jsonObj["descr"],
            'idEdit': jsonObj["id"],
            'input': jsonObj["input"],
            'output': jsonObj["output"]})
    else:
        return render(request, 'add_ex.html', {'context': request.GET['context'], 'name': name})

def add_ex2(request, name):
    if request.method == 'POST':
        if request.POST['idEdit']:
            context = request.POST['context']
            jsonD = json.loads(context)
            obj = json.loads(jsonD["exercisesData"][int(request.POST['idEdit'])])
            obj['title'] = request.POST['title']
            obj['descr'] = request.POST['descr']
            obj['input'] = request.POST['input']
            obj['output'] = request.POST['output']
            jsonD["exercisesData"][int(request.POST['idEdit'])] = json.dumps(obj)
        else:
            context = request.POST['context']
            jsonD = json.loads(context)
            jsonD["exercises"] += 1
            jsonD["exercisesData"].append(json.dumps({
                    "id": jsonD["exercises"] - 1,
                    "title": request.POST["title"],
                    "descr": request.POST["descr"],
                    "input": request.POST["input"],
                    "output": request.POST["output"]
                })
            )

        return redirect('/main/' + name + '/courses/add?context=' + json.dumps(jsonD))

def add_hw2(request, name):
    if request.method == 'POST':
        if request.POST['idEdit']:
            context = request.POST['context']
            jsonD = json.loads(context)
            obj = json.loads(jsonD["homeworksData"][int(request.POST['idEdit'])])
            obj['title'] = request.POST['title']
            obj['descr'] = request.POST['descr']
            obj['input'] = request.POST['input']
            obj['output'] = request.POST['output']
            obj['date'] = request.POST['date']
            jsonD["homeworksData"][int(request.POST['idEdit'])] = json.dumps(obj)
        else:
            context = request.POST['context']
            jsonD = json.loads(context)
            jsonD["homeworks"] += 1
            jsonD["homeworksData"].append(json.dumps({
                    "id": jsonD["homeworks"] - 1,
                    "title": request.POST["title"],
                    "descr": request.POST["descr"],
                    "input": request.POST["input"],
                    "output": request.POST["output"],
                    "date": request.POST["date"]
                })
            )

        return redirect('/main/' + name + '/courses/add?context=' + json.dumps(jsonD))

def add_hw(request, name):
    if name != "Oana":
        return render(request, 'error.html', {'err': 401}, content_type="text/html", status=401)

    if 'edit' in request.GET:
        jsonObj = json.loads(json.loads(request.GET['context'])['homeworksData'][int(request.GET['edit'])])
        print(jsonObj)
        return render(request, 'add_hw.html', {'context': request.GET['context'], 'name': name, 
            'title': jsonObj["title"],
            'descr': jsonObj["descr"],
            'idEdit': jsonObj["id"],
            'input': jsonObj["input"],
            'output': jsonObj["output"],
            'date': jsonObj['date']})
    else:
        return render(request, 'add_hw.html', {'context': request.GET['context'], 'name': name})

def show_tests(request, name):
    if name != "Oana":
        return render(request, 'error.html', {'err': 401}, content_type="text/html", status=401)

def add_test(request, name):
    if request.method == 'GET':
        if name != "Oana":
            return render(request, 'error.html', {'err': 401}, content_type="text/html", status=401)
        return render(request, 'add_test.html')
    
    try:
        Test.objects.get(title=request.POST['title'])
    except Test.DoesNotExist:
        start_str = request.POST['startDate'] + " " + request.POST['startHr']
        stop_str = request.POST['stopDate'] + " " + request.POST['stopHr']

        test = Test(
            title = request.POST['title'],
            description = request.POST['Description'],
            output_generator = request.POST['OutputScript'],
            no_test_cases = 6,
            save_sources = 0,
            exercise = 0,
            homework = 0,
            start_date = datetime.strptime(start_str, '%Y-%m-%d %H:%M'),
            due_date = datetime.strptime(stop_str, '%Y-%m-%d %H:%M'),
        )

        with open("sources/" + test.title + ".py", "x") as f:
            f.write(test.output_generator)

        test.save()

        for item in request.POST['InputData'].split('\n'):
            arr = item.split(' ')
            val = ""

            for i in range(2, len(arr)):
                if arr[i][-1] == '\n' or arr[i][-1] == '\r':
                    arr[i] = arr[i][:-1]
                val += arr[i]

            inputD = Input(
                data_type = arr[0],
                name = arr[1],
                test = test,
                values = val
            )

            inputD.save()
    return redirect("/main/" + name)

def browse_courses(request, name):
    pass