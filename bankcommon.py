# coding: utf-8
import csv
import os
import threading
from decimal import Decimal


class SingletonMeta(type):
    """自定义单例元类"""

    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class BankCommon(metaclass=SingletonMeta):
    # 保存账户数据的csv文档
    account_file = 'accounts.csv'

    file_lock = threading.Lock()

    def __init__(self):
        pass

    def exists_account(self, name):
        """
        判断账户是否已存在
        :param name:
        :return:
        """
        # if not os.path.exists(BankCommon.account_file):
        #     return False

        with open(BankCommon.account_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'] == name:
                    return True

        return False

    def save_account(self, account):
        """
        新建账户保存到csv文件
        :param account:
        :return:
        """
        with BankCommon.file_lock:
            with open(BankCommon.account_file, mode='a', newline='') as file:
                fieldnames = ['name', 'balance']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow({'name': account.bank_name, 'balance': account.balance})

    def read_accounts(self):
        """
        读取已存在的账户数据
        :return:
        """
        with open(BankCommon.account_file, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            data = [row for row in reader]
        return data

    def update_balance(self, name_to_update, amount, type='deposit'):
        """
        存款、取款时，更新balance
        :param name_to_update:
        :param amount:
        :param type:
        :return:
        """
        new_balance = None
        with BankCommon.file_lock:
            data = self.read_accounts()
            for row in data:
                if row['name'] == name_to_update:
                    balance = BankCommon.convert_balance(name_to_update, Decimal(row['balance']))
                    if type == 'deposit':
                        new_balance = balance + Decimal(amount)
                    elif type == 'withdraw':
                        amount = Decimal(amount)
                        if balance > amount:
                            new_balance = balance - amount
                        else:
                            raise Exception(f"{name_to_update} 账户余额：{balance}，不能进行取款：{amount}")
                    else:
                        raise Exception(f"{name_to_update} 账户，不支持的操作：{type}")

                    row['balance'] = new_balance
                    break  # name是唯一的，找到后直接退出循环
            else:
                raise Exception(f"{name_to_update} 账户不存在，操作失败")

            self.write_accounts(data)

        return new_balance

    def update_transfer_balance(self, from_name, to_name, amount):
        """
        转账时，更新balance
        :param name_to_update:
        :param amount:
        :param type:
        :return:
        """
        new_balance = None
        with BankCommon.file_lock:
            data = self.read_accounts()
            update_from_flag = update_to_flag = False
            for row in data:
                if row['name'] == from_name:
                    balance = BankCommon.convert_balance(from_name, Decimal(row['balance']))
                    if balance > amount:
                        new_balance = balance - amount
                    else:
                        raise Exception(f"{from_name} 账户余额：{balance}，不能进行转账：{amount}")

                    row['balance'] = new_balance

                    update_from_flag = True
                elif row['name'] == to_name:
                    balance = BankCommon.convert_balance(from_name, Decimal(row['balance']))
                    new_balance = balance + amount
                    row['balance'] = new_balance

                    update_to_flag = True

                # 若转账双方账户更新完balance，可以退出循环
                if update_from_flag and update_to_flag:
                    break

            if not update_from_flag:
                raise Exception(f"{from_name} 账户不存在，转账失败")

            if not update_to_flag:
                raise Exception(f"{to_name} 账户不存在，转账失败")

            self.write_accounts(data)

        return new_balance

    def write_accounts(self, data):
        """
        保存账户数据到csv文件
        :param data:
        :return:
        """
        with open(BankCommon.account_file, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = data[0].keys()  # 获取列名
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()  # 写入列名
            for row in data:
                writer.writerow(row)

    @staticmethod
    def convert_balance(bank_name, balance):
        """
        账户余额类型转换
        :param bank_name:
        :param balance:
        :return:
        """
        try:
            balance = Decimal(balance)
        except ValueError:
            raise Exception(f"{bank_name} 账户余额转换错误，余额：{balance}")

        return balance
