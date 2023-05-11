dbConf = {
    # 'host': "127.0.0.1",
    # 'port': 3306,
    # 'passwd': "root",
    # 'user': "root",
    'host': "13.213.10.175",
    'port': 8005,
    'user': "root_metatdex",
    'passwd': "b9!45faecbD54ec5c1",
    'charset': "utf8",
    'database': {
        "metatdex_log": "metatdex_log",
        "metatdex": "metatdex",
        "tdex6_saas_polygon": "tdex6_saas_polygon",
        "tdex6_polygon": "tdex6_polygon",
    }
}

RULE_MIN_IPS = 2  # 设备ID关联IP的最大数量
RULE_ADDRESS_ASSOCIATED_OTHER_DEVICE = 2
RULE_MAX_DEVICES_ON_THIS_IP = 5  # 设备ID关联IP的最大数量,在该IP登陆的用户数量阀值(超过就上报)
RULE_UNDER_OTHER_DEVICE = 4
RULE_NEW_ADDRESS = 5
RULE_TOKEN_ASSET_LOW = 5  # 链上资产最少数额（兑USDT）
RULE_NATIVE_COIN_ASSET_LOW = 0.1  # 原生币最少数额
RULE_ASSETS_FROM_MULTIPLE_ADDRESS = 3  # 资金来源，最多几个地址，地址数量

RickConf = {
    "created_duration": 86400,  # 被邀请用户device 出现在identity_login_id 的添加时间，距离现在的时间间隔大于该间隔就判定为老用户
    "max_user_num_within_same_login_ip": 86400,  # 被邀请用户device 出现在identity_login_id 的添加时间，距离现在的时间间隔大于该间隔就判定为老用户
    "chain": {
        "blockchain": [
            {
                # Polygon
                "RPC": "https://cosmopolitan-yolo-diagram.matic.quiknode.pro/a86c7ac86e70c58eb51dc38343d4bb0776464e70/",
                "tokens": [
                    "TT",  # TT
                    "WBTC",  # WBTC
                    "WETH",  # WETH
                    "USDT",  # USDT
                ],
                "contractAddress": {
                    "TT": "0x17a011150e9feb7bec4cfada055c8df436eb730b",  # WBTC
                    "WBTC": "0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6",  # WBTC
                    "WETH": "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619",  # WETH
                    "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",  # USDT
                },
                "chainName": "Polygon",
            }
        ]
    },
    "risk_reason": {
        "RULE_MIN_IPS": "设备ID关联ip数量>={}".format(RULE_MIN_IPS),
        "RULE_ADDRESS_ASSOCIATED_OTHER_DEVICE": "该设备下地址关联了其他设备",
        "RULE_MAX_DEVICES_ON_THIS_IP": "新用户登录相同IP数量达到上限{}".format(
            RULE_MAX_DEVICES_ON_THIS_IP),
        "RULE_UNDER_OTHER_DEVICE": "该设备下地址在其他设备ID下出现",
        "RULE_NEW_ADDRESS": "1天内创建地址",
        "RULE_TOKEN_ASSET_LOW": "代币余额小于{}U".format(RULE_TOKEN_ASSET_LOW),
        "RULE_NATIVE_COIN_ASSET_LOW": "原生币余额小于{}".format(RULE_NATIVE_COIN_ASSET_LOW),
        "RULE_ASSETS_FROM_MULTIPLE_ADDRESS": "资金来源账户数量大于阀值",
    }
}
