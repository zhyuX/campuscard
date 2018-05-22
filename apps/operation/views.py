from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.context_processors import request
from django.utils.datetime_safe import datetime
from django.views import View

from user.models import Student, Card
from operation.models import Library
from operation.models import ConsumeRecord
from operation.models import AccessRecord


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


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
            Library.objects.create(book_id=bookname, state="未归还", card_id=cardid)
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
        val = float(request.POST['val'])
        plac = request.POST.get('place', False)
        studentList = Student.objects.filter(student_id=studentid)
        for row in studentList:
            cardid = row.card_id
        card = Card.objects.get(card_id = cardid)
        card_balance = card.balance;
        ctx = {}

        student = Student.objects.get(card_id=cardid)
        consume_today = ConsumeRecord.objects.filter(card_id=cardid, time__day=datetime.now().day)
        # 计算今日消费额
        consume_today_sum = 0.0
        for single_consume in consume_today:
            consume_today_sum += single_consume.value
        consume_today_sum += val
        # name = student.name
        # college = student.college
        # balance = card.balance

        if len(studentList) > 0:
            if (card_balance - val) > 0:
                if consume_today_sum < 100:
                    ConsumeRecord.objects.create(value=val, location=plac, card_id=cardid)
                    card.balance = card_balance - val
                    card.save();
                    ctx['rlt'] = "消费成功"
                    return render(request, 'consump.html', ctx)
                else:
                    ctx['rlt'] = "今日消费额度达到上限"
                    return render(request, 'consump.html', ctx)
            else:
                ctx['rlt'] = "余额不足"
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



