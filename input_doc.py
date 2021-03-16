import json
from dataclasses import dataclass
from typing import List


@dataclass
class Item:
    name: str = 'towar'
    unit: str = "szt."
    amount: str = "1.0"
    price: str = "9.99"

    def __str__(self):
        return str(self.name) + '\n' + str(self.unit) + '\n' + str(self.amount) + '\n' + str(self.price)


@dataclass
class InputDoc:
    place: str = '<miejce>'
    make_date: str = 'dd-mm-yyyy'
    sell_date: str = 'dd-mm-yyyy'
    sellers_name: str = '<nazwa sprzedawcy>'
    sellers_id: str = '<PESEL: / NIP:>'
    sellers_address: str = '<Adres>'
    sellers_post: str = '<kod pocztowy>'
    sellers_city: str = '<Miasto>'
    buyers_name: str = '<nazwa kupującego>'
    buyers_id: str = 'PESEL: / NIP:>'
    buyers_address: str = '<ulica>'
    buyers_post: str = '<kod pocztowy>'
    buyers_city: str = '<miejscowość>'
    bills_id: str = '0'
    items: List[Item] = list
    worded_total_payment: str = 'zero złotych'
    payment_method: str = 'przelew'
    payment_due_date: str = 'dd-mm-yyyy'
    payment_account: str = '12 1234 1234 1234 1234 1234'
    item_input_name: str = '<wprowadź nazwę>'
    item_input_unit: str = 'j.m.'
    item_input_quantity: str = '1'
    item_input_price: str = '100'
    auto_generate: bool = False

    def calc_total(self) -> float:
        total = 0.0
        for item in self.items:
            total += float(item.price) * float(item.amount)
        return total

    def remove_item(self, index):
        self.items.pop(index)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    # def __str__(self):
    #     out = str(self.place) + '\n' + \
    #         self.make_date + '\n' + \
    #         self.sell_date + '\n' + \
    #         self.sellers_name + '\n' + \
    #         self.sellers_id + '\n' + \
    #         self.sellers_address + '\n' + \
    #         self.sellers_post + '\n' + \
    #         self.sellers_city + '\n' + \
    #         self.buyers_name + '\n' + \
    #         self.buyers_id + '\n' + \
    #         self.buyers_address + '\n' + \
    #         self.buyers_post + '\n' + \
    #         self.buyers_city + '\n' + \
    #         self.bills_id + '\n' + \
    #         self.worded_total_payment + '\n' + \
    #         self.payment_method + '\n' + \
    #         self.payment_due_date + '\n' + \
    #         self.payment_account + '\n' + \
    #         self.item_input_name + '\n' + \
    #         self.item_input_unit + '\n' + \
    #         self.item_input_quantity + '\n' + \
    #         self.item_input_price + '\n' + \
    #         str(self.auto_generate) + '\n'
    #     out += str(len(self.items)) + '\n'
    #     for it in self.items:
    #         out += it.__str__() + '\n'
    #     return out
