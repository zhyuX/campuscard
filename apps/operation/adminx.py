import xadmin
from .models import AccessRecord, ConsumeRecord, Library
from user.models import RechargeRecord


class RechargeRecordAdmin:
    list_display = ['id', 'card_id', 'value', 'time', 'mode']
    search_fields = ['id', 'card_id__card_id', 'value', 'time', 'mode']
    list_filter = ['id', 'card_id__card_id', 'value', 'time', 'mode']


class AccessRecordAdmin:
    list_display = ['id', 'card_id', 'time', 'location']
    search_fields = ['id', 'card_id__card_id', 'time', 'location']
    list_filter = ['id', 'card_id__card_id', 'time', 'location']


class ConsumeRecordAdmin:
    list_display = ['id', 'card_id', 'value', 'time', 'location']
    search_fields = ['id', 'card_id__card_id', 'value', 'time', 'location']
    list_filter = ['id', 'card_id__card_id', 'value', 'time', 'location']


class LibraryAdmin:
    list_display = ['id', 'card_id', 'book_id', 'borrow_time', 'ending_time', 'state']
    search_fields = ['id', 'card_id__card_id', 'book_id', 'borrow_time', 'state']
    list_filter = ['id', 'card_id__card_id', 'book_id', 'borrow_time', 'ending_time', 'state']


xadmin.site.register(RechargeRecord, RechargeRecordAdmin)
xadmin.site.register(ConsumeRecord,ConsumeRecordAdmin)
xadmin.site.register(AccessRecord, AccessRecordAdmin)
xadmin.site.register(Library, LibraryAdmin)