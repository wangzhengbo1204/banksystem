# coding: utf-8
from decimal import Decimal

import uvicorn
from fastapi import FastAPI

from bankaccount import DepositRequest, AccountRequest, BankAccount, WithdrawRequest, TransferRequest
from bankcommon import BankCommon

app = FastAPI()  # 这个实例将是创建你所有 API 的主要交互对象。


@app.post("/account", summary='创建账户', description='创建账户，并初始化金额', response_description='返回账户创建信息')
async def account(request: AccountRequest):
    bank_common = BankCommon()
    if bank_common.exists_account(request.bank_name):
        return {"message": f"{request.bank_name} 已经存在. 创建失败"}

    account = BankAccount(request.bank_name, request.balance)
    try:
        account.save()
        return {"message": f"新建 {request.bank_name} 账户成功. 初始资金: {request.balance}"}
    except Exception as ex:
        return {"message": ex.args[0]}


@app.post("/deposit", summary='存款')
async def deposit_money(request: DepositRequest):
    account = BankAccount(request.bank_name)
    try:
        new_balance = account.deposit(Decimal(request.amount))
        return {"message": f"账户{request.bank_name}，存入 {request.amount} ， 最新总资金: {new_balance}"}
    except Exception as ex:
        return {"message": ex.args[0]}


@app.post("/withdraw", summary='取款')
async def withdraw_money(request: WithdrawRequest):
    account = BankAccount(request.bank_name)
    try:
        new_balance = account.withdraw(Decimal(request.amount))
        return {"message": f"账户{request.bank_name}，取款 {request.amount} ， 最新总资金: {new_balance}"}
    except Exception as ex:
        return {"message": ex.args[0]}


@app.post("/transfer", summary='转账')
async def transfer_money(request: TransferRequest):
    account = BankAccount(request.from_name)
    try:
        new_balance = account.transfer(request.to_name, Decimal(request.amount))
        return {"message": f"账户{request.from_name}，转账 {request.amount} 到 {request.to_name}成功， 剩余总资金: {new_balance}"}
    except Exception as ex:
        return {"message": ex.args[0]}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8090, reload=True)
