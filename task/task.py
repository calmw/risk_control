from core.risk import Risk
from db import mysql


def riskTask():
    conn = mysql.mysql_db()
    if conn is None:
        exit(1)
    risk = Risk(conn)
    risk.checkRisk()


