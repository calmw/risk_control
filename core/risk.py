import logging
import time
from _decimal import Decimal
from web3 import Web3
from blockchain.blockchain import getNativeCoinBalance, getERC20TokenBalance
from config.config import RULE_MIN_IPS, RickConf, RULE_NATIVE_COIN_ASSET_LOW, RULE_TOKEN_ASSET_LOW, \
    RULE_MAX_DEVICES_ON_THIS_IP


# 查询链上原生币币资产
def stepTwoCheckNativeCoinAssets(userAddress):
    assets = 0
    for bc in RickConf.get("chain").get("blockchain"):
        assets += getNativeCoinBalance(bc["RPC"], userAddress)
    logging.info("{} native coin balance:{}".format(userAddress, assets))
    return assets


class Risk:
    db = {}
    tokenPrice = {}
    riskUserIndex = 0  # 上次执行位置

    # 风控检测
    def checkRisk(self):
        if self.checkRiskStatus() is not True:
            return
        # self.setRiskInfo(1, 0)  # 测试服开启
        self.setRiskInfo(0, 1)  # 正式服开启
        users = self.getRiskUser()
        if users is None:
            return
        user_index = 0
        for u in users:
            user_index = u[0]
            logging.info("～～～～～～～～～～～～～～～ {} ～～～～～～～～～～～～～～～".format(format(u[1])))
            # 1 大使邀请新用户风控
            if self.checkStepOne(u[1]) is False:
                continue
            # 2 大使邀请新用户质量考核
            if self.checkStepTwo(u[1]) is False:
                continue
            logging.info("{}检测通过".format(format(u[1])))

        self.setRiskInfo(user_index, 0)  # 正式服开启
        self.closeDb()
        logging.info("执行完毕。")

    # 更新被风控用户信息（上报风控）
    def reportRisk(self, address, reason):
        try:
            with self.db["connMeta"].cursor() as cursor:
                # 更新风控用户表
                sql = "select count(*) from risked_user where address = '{}'".format(address)
                cursor.execute(sql)
                datas = cursor.fetchone()
                if datas[0] == 0:
                    sql = "insert into risked_user (address,reason,is_admin,ctime) values('{}', '{}', {},'{}')".format(
                        address,
                        reason,
                        0,
                        time.strftime("%Y-%m-%d %X", time.localtime()))
                    cursor.execute(sql)
                else:
                    sql = "update risked_user set reason='{}', ctime='{}' where address='{}'".format(
                        reason,
                        time.strftime("%Y-%m-%d %X", time.localtime()),
                        address
                    )
                    cursor.execute(sql)
                # 插入风控用户日志表
                sql = "insert into risked_log (address,reason,risk_type,admin,ctime) values('{}', '{}', {},'{}','{}')".format(
                    address,
                    reason,
                    1,
                    "",
                    time.strftime("%Y-%m-%d %X", time.localtime()))
                cursor.execute(sql)
                # 更新邀请用户表
                sql = "update user_invite set risk_status={} where owner_='{}'".format(
                    1,
                    address,
                )
                cursor.execute(sql)
                self.db["connMeta"].commit()
                logging.info("上报：{}，原因：{}".format(address, reason))
        except Exception as e:
            logging.error("reportRisk error：\n", e)
            return None

    # 第一步，检查邀请用户基础信息（设备ID、关联IP等信息）
    def checkStepOne(self, userAddress):
        userInfo = self.getUserInfo(userAddress)
        if userInfo is None:  # 根据 address 在神策表获取用户信息失败
            return
        deviceId = userInfo[0][0]

        # 1 邀请用户设备ID是否第一次出现
        if self.stepOneCheckDeviceCreateTime(deviceId, userAddress) is False:  # 老用户(创建时间超过设定阀值)不检查
            return False

        # 2 设备ID关联IP数量是否>设定值
        # ipNum = self.stepOneCheckAssociatedIpsByDevice(deviceId, userAddress)
        # if ipNum >= RULE_MIN_IPS:  # 进入风控拦截，上报风控原因：设备ID关联IP数量超过阀值
        #     self.reportRisk(userAddress, RickConf.get("risk_reason").get("RULE_MIN_IPS"))
        #     return False
        # 3 该设备下地址是否在其他设备ID下出现
        if self.stepOneCheckUserAddressIfAssociatedOtherDeviceId(deviceId, userAddress):
            self.reportRisk(userAddress, RickConf['risk_reason']["RULE_UNDER_OTHER_DEVICE"])
            return False
        # 4 要求：将登录IP相同的用户(设备ID)统一上报（在该IP登陆的用户数量超过阀值）
        if self.stepOneCheckUserLoginSameIP(deviceId, userAddress):
            self.reportRisk(userAddress, RickConf['risk_reason']["RULE_MAX_DEVICES_ON_THIS_IP"])
            return False

    # 第二步，大使邀请用户质量考核（地址创建时间、资产等信息）
    def checkStepTwo(self, address):
        # 1 是否为1天内创建地址
        checkAddressByAddTime = self.stepTwoCheckAddressIfCreatedWithinADay(address)
        if checkAddressByAddTime:
            self.reportRisk(address, RickConf['risk_reason']["RULE_NEW_ADDRESS"])
            return False

        # 2 该设备ID下的地址 - 该链的非主链币的主流币（BTC、ETH、USDT）是否超过10u
        if self.stepTwoCheckERC20Assets(address) < RULE_TOKEN_ASSET_LOW:
            self.reportRisk(address, RickConf['risk_reason']["RULE_TOKEN_ASSET_LOW"])
            return False

        # 3 该设备ID下的地址 - 该地址下的主链币资产是否大于0.001
        if stepTwoCheckNativeCoinAssets(address) < RULE_NATIVE_COIN_ASSET_LOW:
            self.reportRisk(address, RickConf['risk_reason']["RULE_NATIVE_COIN_ASSET_LOW"])
            return False

        # 4 检测资金来源是否密集来源单个或者少量多个地址
        # 目标用户：大使邀请来的新用户；
        # 要求：检测资金来源是否密集来源单个或者少量多个地址；（多个地址x个，支持可配置；需要支持链配置，资金来源需要过滤项目合约地址）
        # 结果：若来源单个地址，进入风控列表，上报风控原因：检测资金来源是密集来源单个或者少量多个地址；
        # 若来源多个地址，则判定为正常用户数据，可进行正常化流程；

    # 检查邀请用户设备ID创建的时间间隔
    def stepOneCheckDeviceCreateTime(self, deviceId, userAddress):
        ts = int(time.mktime(time.localtime(time.time())))
        try:
            with self.db["connMetaLog"].cursor() as cursor:
                sql = "select device,add_time,address from identity_login_id where device = '{}' and address='{}' order by add_time desc".format(
                    str(deviceId), userAddress)
                cursor.execute(sql)
                datas = cursor.fetchone()
                if ts - datas[1] <= RickConf['created_duration']:
                    return True
                logging.info("{}不是新用户（创建时间超过{}秒），跳过".format(userAddress, RickConf['created_duration']))
                return False
        except Exception as e:
            logging.error("checkUserDeviceIdIfIsExist error：\n", e)
            return None

    # 查看用户设备ID关联的IP数量
    def stepOneCheckAssociatedIpsByDevice(self, deviceId, userAddress):
        try:
            with self.db["connMetaLog"].cursor() as cursor:
                sql = "select ip from last_log where device = '{}' group by ip".format(str(deviceId))
                cursor.execute(sql)
                datas = cursor.fetchall()
                return len(datas)
        except Exception as e:
            logging.error("checkUserAssociatedIpNumByDeviceId error：\n", e)
            return None

    # 查看用户地址是否关联在其他设备ID下
    def stepOneCheckUserAddressIfAssociatedOtherDeviceId(self, deviceId, userAddress):
        try:
            with self.db["connMetaLog"].cursor() as cursor:
                sql = "select device from last_log where address = '{}' and device <> '{}' group by device".format(
                    userAddress,
                    str(deviceId))
                cursor.execute(sql)
                datas = cursor.fetchall()
                if len(datas) > 0:
                    return True
                return False
        except Exception as e:
            logging.error("checkUserAddressIfBindOtherDeviceId error：\n", e)
            return None

    # 将登录IP相同的用户统一上报（在该IP登陆的用户数量超过阀值）
    # 当前根据最后一次登陆IP判断
    def stepOneCheckUserLoginSameIP(self, deviceId, address):
        try:
            with self.db["connMetaLog"].cursor() as cursor:
                sql = "select ip from last_log where device='{}' and address='{}' group by address order by add_time limit 1".format(
                    deviceId, address)
                cursor.execute(sql)
                lastLog = cursor.fetchone()
                if lastLog is None:
                    return False

                sql = "select address from last_log where ip='{}' and address <> '{}' group by address".format(
                    lastLog[0], address)
                cursor.execute(sql)
                datas = cursor.fetchall()
                if len(datas) >= RULE_MAX_DEVICES_ON_THIS_IP:
                    return True
                return False
        except Exception as e:
            logging.error("stepOneCheckUserLoginSameIP error：\n", e)
            return None

    # 查询是否是一天内注册的地址
    def stepTwoCheckAddressIfCreatedWithinADay(self, userAddress):
        ts = int(time.mktime(time.localtime(time.time())))
        try:
            with self.db["connMetaLog"].cursor() as cursor:
                sql = "select address from last_log where address='{}' and add_time >= {}".format(userAddress, ts)
                cursor.execute(sql)
                datas = cursor.fetchall()
                if len(datas) > 0:
                    return True
                return False
        except Exception as e:
            logging.error("checkAddressByAddTime error：\n", e)
            return None

    # 查询地址链上ERC20代币资产
    def stepTwoCheckERC20Assets(self, userAddress):
        assets = Decimal(0)
        # 获取代币资产
        for bc in RickConf.get("chain").get("blockchain"):
            RPC = bc["RPC"]
            for t in bc.get("tokens"):
                contractAddress = Web3.to_checksum_address(bc["contractAddress"][t])
                # 获取链上代币资产（兑USDT数量）
                tokenNum = getERC20TokenBalance(RPC, contractAddress, userAddress)
                if tokenNum is None:
                    return assets
                tokenNum = Decimal(tokenNum / (10 ** self.tokenPrice[t]['decimals']))
                tokenPrice = self.tokenPrice[t]['price']
                assets += tokenNum * tokenPrice
                logging.info(
                    "address:{}, Token:{}, Number:{}, Price:{}, Assets->{}U".format(userAddress, t, tokenNum,
                                                                                    tokenPrice, tokenNum * tokenPrice))
        logging.info("address:{}, balance:{} USDT".format(userAddress, assets))
        return assets

    # 获取风控进度信息（上次风控执行截止位置）
    def checkRiskStatus(self):
        try:
            with self.db["connMeta"].cursor() as cursor:
                sql = "select user_index,status,is_enabled from risk where id =1"
                cursor.execute(sql)
                cfg = cursor.fetchone()
                if cfg[2] == 0:
                    logging.info("风控没有开启，暂不执行")
                    return False
                if cfg[1] > 0:
                    logging.info("任务正在进行中，等到下轮执行。")
                    return False
                self.riskUserIndex = cfg[0]
                return True
        except Exception as e:
            logging.error("getRiskInfo error：\n", e)
            return None

    # 更新风控状态
    def setRiskInfo(self, user_index, status):
        try:
            with self.db["connMeta"].cursor() as cursor:
                if int(user_index) > 0:
                    sql = "update risk set user_index={}, status={} where id =1".format(user_index, status)
                else:
                    sql = "update risk set status={} where id =1".format(status)
                cursor.execute(sql)
                self.db["connMeta"].commit()
        except Exception as e:
            logging.error("setRiskInfo error：\n", e)

    # 查询要执行风控的用户钱包地址和设备信息
    def getUserInfo(self, userAddress):
        try:
            with self.db["connMetaLog"].cursor() as cursor:
                sql = "select device,address from identity_login_id where address = '{}'".format(str(userAddress))
                cursor.execute(sql)
                datas = cursor.fetchall()
                if len(datas) > 0:
                    return datas
                else:
                    # logging.info("getUserInfo 获取用户信息失败 \n")
                    return None
        except Exception as e:
            logging.error("getUserInfo error：\n", e)
            return None

    # 查询要执行风控的用户钱包地址
    def getRiskUser(self):
        try:
            with self.db["connMeta"].cursor() as cursor:
                sql = "select number, owner_,super_,time from user_invite where super_ <> '' and number > {}".format(
                    self.riskUserIndex)
                cursor.execute(sql)
                datas = cursor.fetchall()
                return datas
        except Exception as e:
            logging.error("getRiskUser error：\n", e)
            return None

    # 查询要执行风控的用户钱包地址
    def getTokenPrice(self):
        try:
            with self.db["connMeta"].cursor() as cursor:
                sql = "select * from risk_token_price "
                cursor.execute(sql)
                datas = cursor.fetchall()
                if len(datas) > 0:
                    for v in datas:
                        self.tokenPrice[v[1]] = {
                            "price": v[2],
                            "decimals": v[4],
                        }
        except Exception as e:
            logging.error("getRiskUser error：\n", e)
            return None

    # 关掉数据库连接
    def closeDb(self):
        self.db["connMeta"].close()
        self.db["connMetaLog"].close()
        self.db["connTdex6Polygon"].close()
        self.db["connTdex6SaasPolygon"].close()

    def __init__(self, conn):
        self.db = conn
        self.getTokenPrice()
