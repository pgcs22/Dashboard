import datetime as dt

def rendimento(saldo_atual, deposito, retiradas, saldo_anterior=0):
    if saldo_anterior == 0:
        rend = (saldo_atual + retiradas)/deposito
        return rend
    else:
        rend = (saldo_atual + (retiradas-deposito))/saldo_anterior
        return rend


def lucro(saldo_atual, deposito, retiradas, saldo_anterior=0):
    if saldo_anterior == 0:
        ganho = saldo_atual + retiradas - deposito
        return ganho
    else:
        ganho = saldo_atual + retiradas - deposito - saldo_anterior
        return ganho

def mes_anterior (data):
    if data.month == 1:
        nova_data = data - dt.timedelta(days=31)
    else:
        nova_data = data.replace(month=data.month-1)
        format(nova_data, "%m/%y")
    return nova_data
