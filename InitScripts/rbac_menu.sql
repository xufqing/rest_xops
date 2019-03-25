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

 Date: 25/03/2019 15:15:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for rbac_menu
-- ----------------------------
DROP TABLE IF EXISTS `rbac_menu`;
CREATE TABLE `rbac_menu`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `icon` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `path` varchar(158) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_frame` tinyint(1) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `sort` int(11) NULL DEFAULT NULL,
  `component` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pid_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `rbac_menu_pid_id_a43b3c84_fk_rbac_menu_id`(`pid_id`) USING BTREE,
  CONSTRAINT `rbac_menu_pid_id_a43b3c84_fk_rbac_menu_id` FOREIGN KEY (`pid_id`) REFERENCES `rbac_menu` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
