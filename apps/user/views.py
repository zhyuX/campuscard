from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from datetime import datetime, date, timedelta
from .models import Card, Student, RechargeRecord
from operation.models import ConsumeRecord, Library
from .forms import LoginForm, UpdatePasswordForm


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
            # 计算借阅数量
            books = Library.objects.filter(card_id=account, state='unreturned').order_by('-borrow_time')
            books_over_time = books.filter(ending_time__lt=date.today())
            books_num = len(books)
            books_over_time_num = len(books_over_time)
            return render(request, 'personal-center.html', {
                'account': account,
                'name': name,
                'college': college,
                'balance': balance,
                'consume_today_sum': consume_today_sum,
                'books_num': books_num,
                'books_over_time_num': books_over_time_num,
            })
        # 未登陆
        else:
            return HttpResponseRedirect("/login/")


# 消费记录查询
class ConsumeRecordView(View):
    @staticmethod
    def processdate(records):
        for record in records:
            record.time = record.time.strftime('%H:%M %p')
        return records

    # get方法直接返回页面
    def get(self, request):
        account = request.session.get('card_id', None)
        # 已登陆
        if account:
            monday = date.today() - timedelta(days=date.today().weekday())
            consume = ConsumeRecord.objects.filter(card_id=account, time__gte=monday).order_by('-time')
            consume_today = ConsumeRecord.objects.filter(card_id=account, time__day=datetime.now().day).order_by('-time')
            consume_today = ConsumeRecordView.processdate(consume_today)
            return render(request, 'consumption-record.html', {
                'consume_today': consume_today,
                'consume': consume,
            })
        else:
            return HttpResponseRedirect("/login/")


# 借阅记录查询
class BorrowInfoView(View):
    @staticmethod
    def processdate(records):
        for record in records:
            record.borrow_time = record.borrow_time.strftime('%Y-%m-%d')
            record.ending_time = record.ending_time.strftime('%Y-%m-%d')
        return records

    def get(self, request):
        account = request.session.get('card_id', None)
        # 已登陆
        if account:
            books = Library.objects.filter(card_id=account, state='unreturned').order_by('-borrow_time')
            books_over_time = books.filter(ending_time__lt=date.today())
            books_num = len(books)
            books_over_time_num = len(books_over_time)
            books = BorrowInfoView.processdate(books)
            return render(request, 'borrow-info.html', {
                'books': books,
                'books_num': books_num,
                'books_over_time_num': books_over_time_num,
            })
        else:
            return HttpResponseRedirect("/login/")


# 充值 ing
class RechargeView(View):
    def get(self, request):
        account = request.session.get('card_id', None)
        if account:
            card = Card.objects.get(card_id=account)
            student = Student.objects.get(card_id=account)
            name = student.name
            balance = card.balance
            return render(request, 'recharge.html', {
                'name': name,
                'balance': balance,
                'id': account
            })
        else:
            return HttpResponseRedirect("/login/")

    def post(self, request):
        # 获取用户名和密码
        account = request.session.get('card_id', None)
        card = Card.objects.get(card_id=account)
        re_id = card.card_id
        re_value = request.POST.get('recharge_value', '')
        pay_mode = request.POST.get('radio', '')
        # 插入记录
        re_value = eval(re_value)
        if re_value > 0:
            obj = RechargeRecord(card_id=card, value=re_value, mode=pay_mode)
            card.balance += re_value
            card.save()
            obj.save()
            return render(request, 'recharge_success.html', {'re_value': re_value})

# 卡券信息
class TicketView(View):
    def get(self, request):
        account = request.session.get('card_id', None)
        if account:
            card = Card.objects.get(card_id=account)
            return render(request, 'card-packet.html')
        else:
            return HttpResponseRedirect("/login/")


# 设置
class SettingView(View):
    def get(self, request):
        account = request.session.get('card_id', None)
        if account:
            card = Card.objects.get(card_id=account)
            student = Student.objects.get(card_id=account)
            return render_to_response('about-me.html', locals())
        else:
            return HttpResponseRedirect("/login/")


# 付款码
class PayCodeView(View):
    def get(self, request):
        account = request.session.get('card_id', None)
        if account:
            card = Card.objects.get(card_id=account)
            return render_to_response('qr-code.html', locals())
        else:
            return HttpResponseRedirect("/login/")


# 更改登陆密码
class UpdatePasswordView(View):
    def get(self, request):
        return render(request, 'login-pssword.html')

    def post(self, request):
        account = request.session.get('card_id', None)
        if account:
            update_form = UpdatePasswordForm(request.POST)
            if update_form.is_valid():
                # 获取表单内容
                old_password = request.POST.get('old_password', '')
                new_password = request.POST.get('new_password', '')
                confirm_password = request.POST.get('confirm_password', '')
                card = Card.objects.get(card_id=account)
                # 符合修改条件
                if old_password == card.password and new_password == confirm_password:
                    card.password = confirm_password
                    card.save()
                    return render_to_response('change-password_successfully.html', locals())
                else:
                    return render(request, 'change-password-failed.html', {'msg': '原密码错误或两次新密码不同'})
            else:
                return render(request, 'change-password-failed.html', {'msg': '请填写原密码'})
        else:
            return HttpResponseRedirect("/login/")


# 支付方式设置
class PaymentSetView(View):
    def get(self, request):
        account = request.session.get('card_id', None)
        if account:
            card = Card.objects.get(card_id=account)
            return render(request, 'payment-set.html')
        else:
            return HttpResponseRedirect("/login/")


# 支付验证设置
class PayAuthSetView(View):
    def get(self, request):
        account = request.session.get('card_id', None)
        if account:
            card = Card.objects.get(card_id=account)
            return render(request, 'pay-auth-set.html')
        else:
            return HttpResponseRedirect("/login/")


# 注销
def logout(request):
    request.session.clear()
    return HttpResponseRedirect("/login/")

