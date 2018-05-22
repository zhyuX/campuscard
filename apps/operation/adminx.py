import xadmin
from .models import AccessRecord, ConsumeRecord, Library
from user.models import RechargeRecord, Card


class RechargeRecordAdmin:
    list_display = ['id', 'card_id', 'value', 'time', 'mode']
    search_fields = ['id', 'card_id__card_id', 'value', 'time', 'mode']
    list_filter = ['id', 'card_id__card_id', 'value', 'time', 'mode']
    model_icon = 'fa fa-jpy'

    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.card_id is not None:
            id = obj.card_id
            card = Card.objects.get(card_id=id)
            card.balance += obj.value
            card.save()

class AccessRecordAdmin:
    list_display = ['id', 'card_id', 'time', 'location']
    search_fields = ['id', 'card_id__card_id', 'time', 'location']
    list_filter = ['id', 'card_id__card_id', 'time', 'location']
    model_icon = 'fa fa-unlock'


class ConsumeRecordAdmin:
    list_display = ['id', 'card_id', 'value', 'time', 'location']
    search_fields = ['id', 'card_id__card_id', 'value', 'time', 'location']
    list_filter = ['id', 'card_id__card_id', 'value', 'time', 'location']
    model_icon = 'fa fa-cart-arrow-down'

    def save_models(self):
        obj = self.new_obj
        if obj.card_id is not None:
            id = obj.card_id
            card = Card.objects.get(card_id=id)
            if card.balance >= obj.value:
                card.balance -= obj.value
                card.save()
                obj.save()


class LibraryAdmin:
    list_display = ['id', 'card_id', 'book_id', 'borrow_time', 'ending_time', 'state']
    search_fields = ['id', 'card_id__card_id', 'book_id', 'borrow_time', 'state']
    list_filter = ['id', 'card_id__card_id', 'book_id', 'borrow_time', 'ending_time', 'state']
    list_editable = ['state']
    model_icon = 'fa fa-book'


xadmin.site.register(RechargeRecord, RechargeRecordAdmin)
xadmin.site.register(ConsumeRecord,ConsumeRecordAdmin)
xadmin.site.register(AccessRecord, AccessRecordAdmin)
xadmin.site.register(Library, LibraryAdmin)