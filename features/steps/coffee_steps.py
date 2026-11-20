from behave import given, when, then
from coffee_machine import CoffeeMachine, NotEnoughMilk


@given("в кофемашине {milk:d} мл молока")
def step_milk(context, milk):
    context.machine = CoffeeMachine(milk)


@when("я заказываю капучино")
def step_order(context):
    context.error = context.drink = None
    try:
        context.drink = context.machine.make_cappuccino()
    except NotEnoughMilk as e:
        context.error = str(e)


@then('кофемашина сообщает "{msg}"')
def step_error(context, msg):
    assert context.error == msg, context.error


@then("я получаю капучино")
def step_drink(context):
    assert context.drink == "cappuccino"


@then("в кофемашине остается {milk:d} мл молока")
def step_left(context, milk):
    assert context.machine.milk == milk, context.machine.milk
