import os
from blockchain.getPrice import updateTokenPrice
from log import logger
import schedule as schedule
from task.task import riskTask

currPath = os.path.dirname(os.path.abspath(__file__))
logFile = "{}/log/logs.log".format(currPath)
logger.config_log(logFile)

schedule.every(10).minutes.do(riskTask)
schedule.every(1).hour.do(updateTokenPrice)
schedule.run_all()

while True:
    schedule.run_pending()
