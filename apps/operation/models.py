from django.db import models
from datetime import datetime
from datetime import timedelta

from user.models import Card


# 门禁信息表
class AccessRecord(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u"编号")
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name=u"卡号")
    time = models.DateTimeField(verbose_name=u"时间", default=datetime.now)
    location = models.CharField(max_length=40, verbose_name=u"地点", default=" ")

    class Meta:
        verbose_name = "门禁记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.card_id)


def get_endtime():
    return datetime.today() + timedelta(days=30)


# 图书馆借阅表
class Library(models.Model):
    GENDER_CHOICES = (
        ('returned', '已归还'),
        ('unreturned', '借阅中')
    )
    id = models.AutoField(primary_key=True, verbose_name=u"编号")
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name=u"卡号")
    book_id = models.CharField(max_length=10, verbose_name=u"书本编号")
    borrow_time = models.DateField(verbose_name=u"借书日期", default=datetime.today)
    ending_time = models.DateField(verbose_name=u"应还时间", default=get_endtime())
    state = models.CharField(max_length=12, verbose_name=u"状态", choices=GENDER_CHOICES)

    class Meta:
        verbose_name = u"图书借阅信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.card_id)


# 消费记录表
class ConsumeRecord(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u"编号")
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name=u"卡号")
    value = models.FloatField(verbose_name=u"消费金额")
    time = models.DateTimeField(verbose_name=u"消费时间", default=datetime.now)
    location = models.CharField(max_length=40, verbose_name=u"消费地点", default=" ")

    class Meta:
        verbose_name = "消费记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.card_id)


