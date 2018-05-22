from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.context_processors import request
from django.views import View

from user.models import Student
from operation.models import Library
from operation.models import ConsumeRecord
from operation.models import AccessRecord


class borrowingView(View):
     def get(self,request):
        return render(request, "borrowing.html")

     def post(self,request):
         studentid = request.POST['student-ID']
         bookname = request.POST['book-name']
         studentList = Student.objects.filter(student_id = studentid)
         for row in studentList:
             cardid = row.card_id
         ctx ={}
         if len(studentList) > 0:
            Library.objects.create(book_id=bookname, state="unreturned", card_id=cardid)
            ctx['rlt'] = "借书成功"
            return render(request, 'borrowing.html', ctx)
         else:
             ctx['rlt'] = "学号错误"
             return render(request, 'borrowing.html', ctx)


class consumpView(View):
    def get(self,request):
        return render(request, 'consump.html')

    def post(self, request):
        studentid = request.POST['student-ID']
        val = request.POST['val']
        plac = request.POST.get('place', False)
        studentList = Student.objects.filter(student_id=studentid)
        for row in studentList:
            cardid = row.card_id
        ctx = {}
        if len(studentList) > 0:
            ConsumeRecord.objects.create(value=val, location=plac, card_id=cardid)
            ctx['rlt'] = "消费成功"
            return render(request, 'consump.html', ctx)
        else:
            ctx['rlt'] = "学号错误"
            return render(request, 'consump.html', ctx)


class entrance_guardView(View):
     def get(self,request):
        return render(request, 'entrance-guard.html')
     def post(self, request):
        studentid = request.POST['student-ID']
        plac = request.POST.get('loc',False)
        studentList = Student.objects.filter(student_id=studentid)
        for row in studentList:
            cardid = row.card_id
        ctx = {}
        if len(studentList) > 0:
            AccessRecord.objects.create(location=plac, card_id=cardid)
            ctx['rlt'] = "出入成功"
            return render(request, 'entrance-guard.html', ctx)
        else:
            ctx['rlt'] = "学号错误"
            return render(request, 'entrance-guard.html', ctx)



