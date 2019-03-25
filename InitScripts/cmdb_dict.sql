/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.3.33
 Source Server Type    : MySQL
 Source Server Version : 50642
 Source Host           : 192.168.3.33:3306
 Source Schema         : rest_xops

 Target Server Type    : MySQL
 Target Server Version : 50642
 File Encoding         : 65001

 Date: 25/03/2019 15:14:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cmdb_dict
-- ----------------------------
DROP TABLE IF EXISTS `cmdb_dict`;
CREATE TABLE `cmdb_dict`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pid_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `cmdb_dict_pid_id_05bfc652_fk_cmdb_dict_id`(`pid_id`) USING BTREE,
  CONSTRAINT `cmdb_dict_pid_id_05bfc652_fk_cmdb_dict_id` FOREIGN KEY (`pid_id`) REFERENCES `cmdb_dict` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of cmdb_dict
-- ----------------------------
INSERT INTO `cmdb_dict` VALUES (1, 'DEVICE_TYPE', '设备类型', '', NULL);
INSERT INTO `cmdb_dict` VALUES (2, 'VM', '虚拟机', '', 1);
INSERT INTO `cmdb_dict` VALUES (3, 'PHY', '物理机', '', 1);
INSERT INTO `cmdb_dict` VALUES (4, 'SERVICE_TYPE', '服务类型', '', NULL);
INSERT INTO `cmdb_dict` VALUES (5, 'password', 'SSH服务|PWD', '', 4);
INSERT INTO `cmdb_dict` VALUES (6, 'private_key', 'SSH服务|KEY', '', 4);
INSERT INTO `cmdb_dict` VALUES (7, 'mysql', 'MYSQL服务', '', 4);
INSERT INTO `cmdb_dict` VALUES (8, 'ENVIRONMENT_TYPE', '应用环境', '', NULL);
INSERT INTO `cmdb_dict` VALUES (9, 'all', '所有环境', '', 8);
INSERT INTO `cmdb_dict` VALUES (10, 'dev', '开发环境', '', 8);
INSERT INTO `cmdb_dict` VALUES (11, 'test', '测试环境', '', 8);
INSERT INTO `cmdb_dict` VALUES (12, 'prod', '生产环境', '', 8);
INSERT INTO `cmdb_dict` VALUES (13, 'REPO_TYPE', '代码类型', '', NULL);
INSERT INTO `cmdb_dict` VALUES (14, 'tag', 'tag', '', 13);
INSERT INTO `cmdb_dict` VALUES (15, 'branch', 'branch', '', 13);

SET FOREIGN_KEY_CHECKS = 1;
