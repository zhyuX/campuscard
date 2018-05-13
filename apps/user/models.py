from django.db import models
from datetime import datetime


# 校园卡表
class Card(models.Model):
    GENDER_CHOICES = (
        ('valid', '有效'),
        ('invalid', '无效')
    )
    card_id = models.CharField(max_length=20, primary_key=True, verbose_name=u"卡号")
    balance = models.FloatField(verbose_name=u"余额")
    state = models.CharField(max_length=10, verbose_name=u"状态", choices=GENDER_CHOICES)
    create_time = models.DateTimeField(verbose_name=u"创建时间", default=datetime.now)
    password = models.CharField(max_length=20, verbose_name=u"密码")

    class Meta:
        verbose_name = u"校园卡信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.card_id)


# 学生信息表
class Student(models.Model):
    GENDER_CHOICES = (
        ('female', '女'),
        ('male', '男')
    )
    student_id = models.CharField(max_length=20, primary_key=True, verbose_name=u"学号")
    name = models.CharField(max_length=20, verbose_name=u"姓名")
    college = models.CharField(max_length=40, verbose_name=u"学院")
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name=u"卡号")
    sex = models.CharField(max_length=10, verbose_name=u"性别", choices=GENDER_CHOICES)
    grade = models.CharField(max_length=10, verbose_name=u"年级")
    dormitory = models.CharField(max_length=20, verbose_name=u"寝室")

    class Meta:
        verbose_name = u"学生信息"
        ordering = ["student_id"]
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.student_id


# 充值记录表
class RechargeRecord(models.Model):
    GENDER_CHOICES = (
        ('alipay', '支付宝'),
        ('wechatpay', '微信'),
        ('cash', '现金')
    )
    id = models.AutoField(primary_key=True, verbose_name=u"编号")
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name=u"卡号")
    value = models.FloatField(verbose_name=u"金额")
    time = models.DateTimeField(verbose_name=u"充值时间", default=datetime.now)
    mode = models.CharField(max_length=10, verbose_name=u"充值方式", choices=GENDER_CHOICES)

    class Meta:
        verbose_name = u"充值记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.card_id)

