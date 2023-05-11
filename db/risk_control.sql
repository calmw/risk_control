/*
 Navicat Premium Data Transfer

 Source Server         : tdex175
 Source Server Type    : MySQL
 Source Server Version : 50733 (5.7.33)
 Source Host           : 13.213.10.175:8005
 Source Schema         : metatdex

 Target Server Type    : MySQL
 Target Server Version : 50733 (5.7.33)
 File Encoding         : 65001

 Date: 27/04/2023 10:18:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for risk
-- ----------------------------
DROP TABLE IF EXISTS `risk`;
CREATE TABLE `risk` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `user_index` bigint(20) unsigned DEFAULT NULL COMMENT '风控用户索引（当前风控执行到那个用户）',
  `status` tinyint(3) unsigned DEFAULT '0' COMMENT '当前程序执行状态，1 进行中 ，0 停止\n',
  `is_enabled` tinyint(3) unsigned DEFAULT '0' COMMENT '0 不开启风控程序\n1 开启风控程序',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='用户风控';

-- ----------------------------
-- Records of risk
-- ----------------------------
BEGIN;
INSERT INTO `risk` (`id`, `user_index`, `status`, `is_enabled`) VALUES (1, 1, 0, 0);
COMMIT;

-- ----------------------------
-- Table structure for risk_token_price
-- ----------------------------
DROP TABLE IF EXISTS `risk_token_price`;
CREATE TABLE `risk_token_price` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `symbol` varchar(20) DEFAULT NULL,
  `price` decimal(30,4) unsigned DEFAULT NULL COMMENT '兑USDT汇率',
  `updated_at` datetime DEFAULT NULL,
  `decimals` tinyint(3) unsigned DEFAULT '18',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of risk_token_price
-- ----------------------------
BEGIN;
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (26, 'LDO', 2.5320, '2023-04-27 10:15:14', 18);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (27, 'AAVE', 82.2642, '2023-04-27 10:15:14', 18);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (28, 'MANA', 0.6243, '2023-04-27 10:15:14', 18);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (29, 'LINK', 7.1395, '2023-04-27 10:15:14', 18);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (30, 'SUSHI', 1.1690, '2023-04-27 10:15:14', 18);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (31, 'WETH', 2091.4900, '2023-04-27 10:15:14', 18);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (32, 'WBTC', 27960.6700, '2023-04-27 10:15:14', 8);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (33, 'CRV', 1.0235, '2023-04-27 10:15:14', 18);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (34, 'SAND', 0.6740, '2023-04-27 10:15:14', 18);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (35, 'UNI', 6.2705, '2023-04-27 10:15:14', 18);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (36, 'TT', 1.4559, '2023-04-27 10:15:13', 18);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (37, 'MATIC', 3.0000, '2023-04-27 10:15:13', 18);
INSERT INTO `risk_token_price` (`id`, `symbol`, `price`, `updated_at`, `decimals`) VALUES (38, 'USDT', 1.0000, '2023-04-27 10:15:15', 6);
COMMIT;

-- ----------------------------
-- Table structure for risked_log
-- ----------------------------
DROP TABLE IF EXISTS `risked_log`;
CREATE TABLE `risked_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `address` varchar(42) DEFAULT NULL COMMENT '被风控的用户钱包地址',
  `reason` varchar(255) DEFAULT '0' COMMENT '被风控的原因',
  `risk_type` tinyint(4) DEFAULT NULL COMMENT '类型， 1 被风控 2 解除风控',
  `ctime` datetime DEFAULT NULL COMMENT '被风控的时间',
  `admin` varchar(100) DEFAULT '0' COMMENT '手工操作的管理员',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2532 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of risked_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for risked_user
-- ----------------------------
DROP TABLE IF EXISTS `risked_user`;
CREATE TABLE `risked_user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `address` varchar(42) DEFAULT '' COMMENT '被风控的用户地址',
  `reason` varchar(255) DEFAULT NULL COMMENT '被风控的原因',
  `ctime` datetime DEFAULT NULL COMMENT '被风控的时间',
  `is_admin` int(10) unsigned DEFAULT '0' COMMENT '1 管理员操作\n0 程序自动风控',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=479 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of risked_user
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
