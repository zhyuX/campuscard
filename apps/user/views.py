from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from datetime import datetime, date, timedelta
from .models import Card, Student
from operation.models import ConsumeRecord
from .forms import LoginForm


# Create your views here.
# 登陆功能
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户名和密码
            account = request.POST.get('account', '')
            pass_word = request.POST.get('password', '')
            result = Card.objects.filter(card_id=account, password=pass_word)
            # 验证成功
            if len(result) > 0:
                request.session['card_id'] = account
                return HttpResponseRedirect("/index/")
            else:
                return render(request, 'login.html', {'msg': '卡号或密码错误'})
        else:
            return render(request, 'login.html', {'msg': '卡号和密码不能为空'})


# 主页
class IndexView(View):
    def get(self, request):
        account = request.session.get('card_id', None)
        # 已登陆
        if account:
            card = Card.objects.get(card_id=account)
            student = Student.objects.get(card_id=account)
            consume_today = ConsumeRecord.objects.filter(card_id=account, time__day=datetime.now().day)
            # 计算今日消费额
            consume_today_sum = 0.0
            for single_consume in consume_today:
                consume_today_sum += single_consume.value
            name = student.name
            college = student.college
            balance = card.balance
            return render(request, 'personal-center.html', {
                'account': account,
                'name': name,
                'college': college,
                'balance': balance,
                'consume_today_sum': consume_today_sum,
            })
        # 未登陆
        else:
            return render(request, 'login.html')


# 消费记录查询
class ConsumeRecordView(View):
    # get方法直接返回页面
    def get(self, request):
        account = request.session.get('card_id', None)
        # 已登陆
        if account:
            monday = date.today() - timedelta(days=date.today().weekday())
            consume = ConsumeRecord.objects.filter(card_id=account, time__gte=monday).order_by('-time')
            consume_today = ConsumeRecord.objects.filter(card_id=account, time__day=datetime.now().day).order_by('-time')
            return render(request, 'consumption-record.html', {
                'consume_today': consume_today,
                'consume': consume,
            })
        else:
            return render(request, 'login.html')


# 消费记录查询
class BorrowInfoView(View):
    def get(self, request):
        account = request.session.get('card_id', None)
        # 已登陆
        if account:
            return render(request, 'borrow-info.html')
        else:
            return render(request, 'login.html')

# 注销
def logout(request):
    request.session.clear()
    return HttpResponseRedirect("/login/")
# def login(request):
#     if request.method == 'POST':
#         account = request.POST.get('account', '')
#         pass_word = request.POST.get('password', '')
#         if account != '' and pass_word != '':
#             result = Card.objects.filter(card_id=account, password=pass_word)
#             # 存在账户
#             if len(result) > 0:
#                 request.session['card_id'] = account
#                 return render(request, 'personal-center.html')
#             else:
#                 return render(request, 'login.html', {'msg': '卡号或密码错误'})
#         else:
#             return render(request, 'login.html', {'msg': '卡号和密码不能为空'})
#     elif request.method == 'GET':
#         return render(request, 'login.html')
