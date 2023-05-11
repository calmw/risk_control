import time
from _decimal import Decimal
from db import mysql


def updateTokenPrice():
    conn = mysql.mysql_db()
    if conn is None:
        exit(1)
    try:
        with conn["connMeta"].cursor() as MateCursor:
            with conn["connTdex6Polygon"].cursor() as cursor:
                sql = "select symbol,decimals,price from token_price"
                cursor.execute(sql)
                data = cursor.fetchall()
                for d in data:
                    sql = "update risk_token_price set price={},decimals={},updated_at='{}' where symbol ='{}'".format(
                        Decimal(
                            d[2]) / 10 ** 18,  # 该库数据价格精度为18
                        d[1],
                        time.strftime("%Y-%m-%d %X", time.localtime()),
                        d[0],
                    )
                    MateCursor.execute(sql)
            with conn["connTdex6SaasPolygon"].cursor() as cursor:
                sql = "select symbol,decimals,price from token_price"
                cursor.execute(sql)
                data = cursor.fetchall()
                for d in data:
                    if d[0] == "MATIC":  # 从上个库获取
                        continue
                    elif d[0] == "USDT":  # 兑USDT汇率固定为1
                        sql = "update risk_token_price set price={},decimals={},updated_at='{}' where symbol ='{}'".format(
                            Decimal(1),
                            d[1],
                            time.strftime("%Y-%m-%d %X", time.localtime()),
                            d[0],
                        )
                    else:
                        sql = "update risk_token_price set price={},decimals={},updated_at='{}' where symbol ='{}'".format(
                            Decimal(
                                d[2]) / 10 ** 6,  # 该库数据价格精度为6
                            d[1],
                            time.strftime("%Y-%m-%d %X", time.localtime()),
                            d[0],
                        )
                    MateCursor.execute(sql)
        conn["connMeta"].commit()

    except Exception as e:
        print(e)
