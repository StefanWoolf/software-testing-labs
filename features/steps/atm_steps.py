from behave import given, when, then
from atm import ATM, InsufficientFunds


@given("на счету {balance:d} рублей")
def step_balance(context, balance):
    context.atm = ATM(balance)


@when("я пытаюсь снять {amount:d} рублей")
def step_withdraw(context, amount):
    context.error = context.cash = None
    try:
        context.cash = context.atm.withdraw(amount)
    except InsufficientFunds as e:
        context.error = str(e)


@then('банкомат отказывает с сообщением "{msg}"')
def step_refuse(context, msg):
    assert context.error == msg, context.error


@then("банкомат выдает {amount:d} рублей")
def step_cash(context, amount):
    assert context.cash == amount, context.cash


@then("баланс остается {balance:d} рублей")
def step_check_balance(context, balance):
    assert context.atm.balance == balance, context.atm.balance
