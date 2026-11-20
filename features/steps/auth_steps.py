from behave import given, when, then
from auth import Auth


@given('зарегистрирован пользователь "{user}" с паролем "{password}"')
def step_user(context, user, password):
    context.auth = Auth({user: password})
    context.user, context.password = user, password


@when("пользователь {n:d} раза вводит неверный пароль")
def step_wrong(context, n):
    for _ in range(n):
        context.auth.login(context.user, "wrong")


@then("аккаунт заблокирован")
def step_locked(context):
    assert context.user in context.auth.locked


@then("аккаунт не заблокирован")
def step_not_locked(context):
    assert context.user not in context.auth.locked


@then("вход с верным паролем отклоняется")
def step_login_denied(context):
    assert context.auth.login(context.user, context.password) == "locked"


@then("вход с верным паролем успешен")
def step_login_ok(context):
    assert context.auth.login(context.user, context.password) == "ok"
