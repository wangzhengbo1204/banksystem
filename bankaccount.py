# coding:utf-8
import csv

from pydantic import BaseModel, confloat, PositiveFloat, conint

import bankcommon


class BankAccount:
    def __init__(self, bank_name, initial_balance=None):
        self.bank_name = bank_name
        self.balance = initial_balance

    def get_bank_name(self):
        return self.bank_name

    def set_bank_name(self, bank_name):
        self.bank_name = bank_name

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

    def deposit(self, amount):
        bank_common = bankcommon.BankCommon()
        new_balance = bank_common.update_balance(self.bank_name, amount, 'deposit')
        return new_balance

    def withdraw(self, amount):
        bank_common = bankcommon.BankCommon()
        new_balance = bank_common.update_balance(self.bank_name, amount, 'withdraw')
        return new_balance

    def transfer(self, to_name, amount):
        bank_common = bankcommon.BankCommon()
        new_balance = bank_common.update_transfer_balance(self.bank_name, to_name, amount)
        return new_balance

    def save(self):
        bank_common = bankcommon.BankCommon()
        bank_common.save_account(self)
        return True


class AccountRequest(BaseModel):
    """
    新建银行账户请求类
    """
    bank_name: str
    balance: conint(ge=0)


class DepositRequest(BaseModel):
    """
    存款请求类
    """
    bank_name: str
    amount: PositiveFloat


class WithdrawRequest(BaseModel):
    """
    取款请求类
    """
    bank_name: str
    amount: PositiveFloat


class TransferRequest(BaseModel):
    """
    转账请求类
    """
    from_name: str
    to_name: str
    amount: PositiveFloat
