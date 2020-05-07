from django.db import models


class Slot(models.Model):
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    position = models.IntegerField()
    taken = models.BooleanField(default=False)

    def __str__(self):
        return f"<Slot shop='{self.shop.name}' taken? {self.taken}>"


class Shop(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slot_amount = models.IntegerField(default=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.slot_set.all():
            for i in range(self.slot_amount):
                Slot(shop=self, position=i).save()

    # def add_slots(self):
    #     for i in range(self.slot_amount):
    #         Slot(shop=self, position=i).save()
    #     return self.slot_set.all()

    def __str__(self):
        return f"<Shop '{self.name}'>"


class Person(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
