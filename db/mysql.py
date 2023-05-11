import pymysql
import logging
import config.config


# mysql 连接
def mysql_db():
    try:
        connMeta = pymysql.connect(
            host=config.config.dbConf.get('host'),
            port=config.config.dbConf.get('port'),
            database=config.config.dbConf.get('database').get("metatdex"),
            charset=config.config.dbConf.get('charset'),
            user=config.config.dbConf.get('user'),
            passwd=config.config.dbConf.get('passwd'),
        )
        connMetaLog = pymysql.connect(
            host=config.config.dbConf.get('host'),
            port=config.config.dbConf.get('port'),
            database=config.config.dbConf.get('database').get("metatdex_log"),
            charset=config.config.dbConf.get('charset'),
            user=config.config.dbConf.get('user'),
            passwd=config.config.dbConf.get('passwd'),
        )
        connTdex6Polygon = pymysql.connect(
            host=config.config.dbConf.get('host'),
            port=config.config.dbConf.get('port'),
            database=config.config.dbConf.get('database').get("tdex6_polygon"),
            charset=config.config.dbConf.get('charset'),
            user=config.config.dbConf.get('user'),
            passwd=config.config.dbConf.get('passwd'),
        )
        connTdex6SaasPolygon = pymysql.connect(
            host=config.config.dbConf.get('host'),
            port=config.config.dbConf.get('port'),
            database=config.config.dbConf.get('database').get("tdex6_saas_polygon"),
            charset=config.config.dbConf.get('charset'),
            user=config.config.dbConf.get('user'),
            passwd=config.config.dbConf.get('passwd'),
        )
        return {
            "connMeta": connMeta,
            "connMetaLog": connMetaLog,
            "connTdex6Polygon": connTdex6Polygon,
            "connTdex6SaasPolygon": connTdex6SaasPolygon,
        }
    except Exception as e:
        logging.error("数据库连接失败：\n", e)
        return None
