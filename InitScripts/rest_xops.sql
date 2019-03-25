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

 Date: 25/03/2019 15:23:54
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 73 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add permission', 1, 'add_permission');
INSERT INTO `auth_permission` VALUES (2, 'Can change permission', 1, 'change_permission');
INSERT INTO `auth_permission` VALUES (3, 'Can delete permission', 1, 'delete_permission');
INSERT INTO `auth_permission` VALUES (4, 'Can view permission', 1, 'view_permission');
INSERT INTO `auth_permission` VALUES (5, 'Can add group', 2, 'add_group');
INSERT INTO `auth_permission` VALUES (6, 'Can change group', 2, 'change_group');
INSERT INTO `auth_permission` VALUES (7, 'Can delete group', 2, 'delete_group');
INSERT INTO `auth_permission` VALUES (8, 'Can view group', 2, 'view_group');
INSERT INTO `auth_permission` VALUES (9, 'Can add content type', 3, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (10, 'Can change content type', 3, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (11, 'Can delete content type', 3, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (12, 'Can view content type', 3, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (13, 'Can add session', 4, 'add_session');
INSERT INTO `auth_permission` VALUES (14, 'Can change session', 4, 'change_session');
INSERT INTO `auth_permission` VALUES (15, 'Can delete session', 4, 'delete_session');
INSERT INTO `auth_permission` VALUES (16, 'Can view session', 4, 'view_session');
INSERT INTO `auth_permission` VALUES (17, 'Can add 用户信息', 5, 'add_userprofile');
INSERT INTO `auth_permission` VALUES (18, 'Can change 用户信息', 5, 'change_userprofile');
INSERT INTO `auth_permission` VALUES (19, 'Can delete 用户信息', 5, 'delete_userprofile');
INSERT INTO `auth_permission` VALUES (20, 'Can view 用户信息', 5, 'view_userprofile');
INSERT INTO `auth_permission` VALUES (21, 'Can add 菜单', 6, 'add_menu');
INSERT INTO `auth_permission` VALUES (22, 'Can change 菜单', 6, 'change_menu');
INSERT INTO `auth_permission` VALUES (23, 'Can delete 菜单', 6, 'delete_menu');
INSERT INTO `auth_permission` VALUES (24, 'Can view 菜单', 6, 'view_menu');
INSERT INTO `auth_permission` VALUES (25, 'Can add 组织架构', 7, 'add_organization');
INSERT INTO `auth_permission` VALUES (26, 'Can change 组织架构', 7, 'change_organization');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 组织架构', 7, 'delete_organization');
INSERT INTO `auth_permission` VALUES (28, 'Can view 组织架构', 7, 'view_organization');
INSERT INTO `auth_permission` VALUES (29, 'Can add 权限', 8, 'add_permission');
INSERT INTO `auth_permission` VALUES (30, 'Can change 权限', 8, 'change_permission');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 权限', 8, 'delete_permission');
INSERT INTO `auth_permission` VALUES (32, 'Can view 权限', 8, 'view_permission');
INSERT INTO `auth_permission` VALUES (33, 'Can add role', 9, 'add_role');
INSERT INTO `auth_permission` VALUES (34, 'Can change role', 9, 'change_role');
INSERT INTO `auth_permission` VALUES (35, 'Can delete role', 9, 'delete_role');
INSERT INTO `auth_permission` VALUES (36, 'Can view role', 9, 'view_role');
INSERT INTO `auth_permission` VALUES (37, 'Can add 业务', 10, 'add_business');
INSERT INTO `auth_permission` VALUES (38, 'Can change 业务', 10, 'change_business');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 业务', 10, 'delete_business');
INSERT INTO `auth_permission` VALUES (40, 'Can view 业务', 10, 'view_business');
INSERT INTO `auth_permission` VALUES (41, 'Can add 连接信息', 11, 'add_connectioninfo');
INSERT INTO `auth_permission` VALUES (42, 'Can change 连接信息', 11, 'change_connectioninfo');
INSERT INTO `auth_permission` VALUES (43, 'Can delete 连接信息', 11, 'delete_connectioninfo');
INSERT INTO `auth_permission` VALUES (44, 'Can view 连接信息', 11, 'view_connectioninfo');
INSERT INTO `auth_permission` VALUES (45, 'Can add device file', 12, 'add_devicefile');
INSERT INTO `auth_permission` VALUES (46, 'Can change device file', 12, 'change_devicefile');
INSERT INTO `auth_permission` VALUES (47, 'Can delete device file', 12, 'delete_devicefile');
INSERT INTO `auth_permission` VALUES (48, 'Can view device file', 12, 'view_devicefile');
INSERT INTO `auth_permission` VALUES (49, 'Can add 设备信息', 13, 'add_deviceinfo');
INSERT INTO `auth_permission` VALUES (50, 'Can change 设备信息', 13, 'change_deviceinfo');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 设备信息', 13, 'delete_deviceinfo');
INSERT INTO `auth_permission` VALUES (52, 'Can view 设备信息', 13, 'view_deviceinfo');
INSERT INTO `auth_permission` VALUES (53, 'Can add 扫描信息', 14, 'add_devicescaninfo');
INSERT INTO `auth_permission` VALUES (54, 'Can change 扫描信息', 14, 'change_devicescaninfo');
INSERT INTO `auth_permission` VALUES (55, 'Can delete 扫描信息', 14, 'delete_devicescaninfo');
INSERT INTO `auth_permission` VALUES (56, 'Can view 扫描信息', 14, 'view_devicescaninfo');
INSERT INTO `auth_permission` VALUES (57, 'Can add 字典', 15, 'add_dict');
INSERT INTO `auth_permission` VALUES (58, 'Can change 字典', 15, 'change_dict');
INSERT INTO `auth_permission` VALUES (59, 'Can delete 字典', 15, 'delete_dict');
INSERT INTO `auth_permission` VALUES (60, 'Can view 字典', 15, 'view_dict');
INSERT INTO `auth_permission` VALUES (61, 'Can add historical 设备信息', 16, 'add_historicaldeviceinfo');
INSERT INTO `auth_permission` VALUES (62, 'Can change historical 设备信息', 16, 'change_historicaldeviceinfo');
INSERT INTO `auth_permission` VALUES (63, 'Can delete historical 设备信息', 16, 'delete_historicaldeviceinfo');
INSERT INTO `auth_permission` VALUES (64, 'Can view historical 设备信息', 16, 'view_historicaldeviceinfo');
INSERT INTO `auth_permission` VALUES (65, 'Can add 部署记录', 17, 'add_deployrecord');
INSERT INTO `auth_permission` VALUES (66, 'Can change 部署记录', 17, 'change_deployrecord');
INSERT INTO `auth_permission` VALUES (67, 'Can delete 部署记录', 17, 'delete_deployrecord');
INSERT INTO `auth_permission` VALUES (68, 'Can view 部署记录', 17, 'view_deployrecord');
INSERT INTO `auth_permission` VALUES (69, 'Can add 项目配置', 18, 'add_project');
INSERT INTO `auth_permission` VALUES (70, 'Can change 项目配置', 18, 'change_project');
INSERT INTO `auth_permission` VALUES (71, 'Can delete 项目配置', 18, 'delete_project');
INSERT INTO `auth_permission` VALUES (72, 'Can view 项目配置', 18, 'view_project');

-- ----------------------------
-- Table structure for cmdb_business
-- ----------------------------
DROP TABLE IF EXISTS `cmdb_business`;
CREATE TABLE `cmdb_business`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime(6) NOT NULL,
  `modify_time` datetime(6) NOT NULL,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pid_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `cmdb_business_pid_id_b43034ad_fk_cmdb_business_id`(`pid_id`) USING BTREE,
  CONSTRAINT `cmdb_business_pid_id_b43034ad_fk_cmdb_business_id` FOREIGN KEY (`pid_id`) REFERENCES `cmdb_business` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for cmdb_connectioninfo
-- ----------------------------
DROP TABLE IF EXISTS `cmdb_connectioninfo`;
CREATE TABLE `cmdb_connectioninfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime(6) NOT NULL,
  `modify_time` datetime(6) NOT NULL,
  `hostname` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `auth_type` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `port` int(11) NULL DEFAULT NULL,
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `desc` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of cmdb_connectioninfo
-- ----------------------------
INSERT INTO `cmdb_connectioninfo` VALUES (1, '2019-03-23 15:09:43.813048', '2019-03-23 15:09:43.813083', '192.168.3.33', 'password', 22, 'root', 'anson0418', NULL);

-- ----------------------------
-- Table structure for cmdb_devicefile
-- ----------------------------
DROP TABLE IF EXISTS `cmdb_devicefile`;
CREATE TABLE `cmdb_devicefile`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime(6) NOT NULL,
  `modify_time` datetime(6) NOT NULL,
  `file_content` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `upload_user` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `device_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `cmdb_devicefile_device_id_1222de4d_fk_cmdb_deviceinfo_id`(`device_id`) USING BTREE,
  CONSTRAINT `cmdb_devicefile_device_id_1222de4d_fk_cmdb_deviceinfo_id` FOREIGN KEY (`device_id`) REFERENCES `cmdb_deviceinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for cmdb_deviceinfo
-- ----------------------------
DROP TABLE IF EXISTS `cmdb_deviceinfo`;
CREATE TABLE `cmdb_deviceinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime(6) NOT NULL,
  `modify_time` datetime(6) NOT NULL,
  `status` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sys_hostname` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mac_address` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sn_number` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `os_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `os_version` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `device_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `device_model` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `auth_type` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `hostname` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `network_type` int(11) NULL DEFAULT NULL,
  `business_type` int(11) NULL DEFAULT NULL,
  `leader` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `buy_date` date NOT NULL,
  `warranty_date` date NOT NULL,
  `desc` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `changed_by_id` int(11) NULL DEFAULT NULL,
  `pid_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `cmdb_deviceinfo_changed_by_id_1a864b67_fk_rbac_userprofile_id`(`changed_by_id`) USING BTREE,
  INDEX `cmdb_deviceinfo_pid_id_617c7690_fk_cmdb_deviceinfo_id`(`pid_id`) USING BTREE,
  CONSTRAINT `cmdb_deviceinfo_changed_by_id_1a864b67_fk_rbac_userprofile_id` FOREIGN KEY (`changed_by_id`) REFERENCES `rbac_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `cmdb_deviceinfo_pid_id_617c7690_fk_cmdb_deviceinfo_id` FOREIGN KEY (`pid_id`) REFERENCES `cmdb_deviceinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of cmdb_deviceinfo
-- ----------------------------
INSERT INTO `cmdb_deviceinfo` VALUES (1, '2019-03-23 15:09:43.798408', '2019-03-23 15:09:43.798448', 'online', 'xops\r\n', '00:0c:29:55:56:eb\r\n', 'VMware-56 4d c8 fb b0 d9 3c 2b-62 7c bb 44 fe 55 56 eb\r\n', 'Linux', 'CentOS Linux release 7.5.1804 (Core) \r\n', '', '', 'password', '192.168.3.33', NULL, NULL, NULL, '2019-03-23', '2019-03-23', '', 1, NULL);

-- ----------------------------
-- Table structure for cmdb_deviceinfo_businesses
-- ----------------------------
DROP TABLE IF EXISTS `cmdb_deviceinfo_businesses`;
CREATE TABLE `cmdb_deviceinfo_businesses`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deviceinfo_id` int(11) NOT NULL,
  `business_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `cmdb_deviceinfo_business_deviceinfo_id_business_i_ba3f302c_uniq`(`deviceinfo_id`, `business_id`) USING BTREE,
  INDEX `cmdb_deviceinfo_busi_business_id_18409b77_fk_cmdb_busi`(`business_id`) USING BTREE,
  CONSTRAINT `cmdb_deviceinfo_busi_business_id_18409b77_fk_cmdb_busi` FOREIGN KEY (`business_id`) REFERENCES `cmdb_business` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `cmdb_deviceinfo_busi_deviceinfo_id_2b68f4f0_fk_cmdb_devi` FOREIGN KEY (`deviceinfo_id`) REFERENCES `cmdb_deviceinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for cmdb_devicescaninfo
-- ----------------------------
DROP TABLE IF EXISTS `cmdb_devicescaninfo`;
CREATE TABLE `cmdb_devicescaninfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime(6) NOT NULL,
  `modify_time` datetime(6) NOT NULL,
  `status` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sys_hostname` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mac_address` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sn_number` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `os_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `os_version` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `device_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `device_model` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `hostname` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `auth_type` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `port` int(11) NULL DEFAULT NULL,
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `error_message` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of cmdb_devicescaninfo
-- ----------------------------
INSERT INTO `cmdb_devicescaninfo` VALUES (2, '2019-03-23 16:11:32.253081', '2019-03-23 16:12:03.263809', 'Succeed', 'xops\r\n', '00:0c:29:55:56:eb\r\n', 'VMware-56 4d c8 fb b0 d9 3c 2b-62 7c bb 44 fe 55 56 eb\r\n', 'Linux', 'CentOS Linux release 7.5.1804 (Core) \r\n', '', '', '192.168.3.33', 'password', 22, 'root', 'anson0418', '');

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

-- ----------------------------
-- Table structure for cmdb_historicaldeviceinfo
-- ----------------------------
DROP TABLE IF EXISTS `cmdb_historicaldeviceinfo`;
CREATE TABLE `cmdb_historicaldeviceinfo`  (
  `id` int(11) NOT NULL,
  `status` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sys_hostname` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mac_address` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sn_number` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `os_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `os_version` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `device_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `device_model` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `auth_type` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `hostname` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `network_type` int(11) NULL DEFAULT NULL,
  `business_type` int(11) NULL DEFAULT NULL,
  `leader` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `buy_date` date NOT NULL,
  `warranty_date` date NOT NULL,
  `desc` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `history_id` int(11) NOT NULL AUTO_INCREMENT,
  `history_date` datetime(6) NOT NULL,
  `history_change_reason` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `history_type` varchar(1) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `changed_by_id` int(11) NULL DEFAULT NULL,
  `history_user_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`history_id`) USING BTREE,
  INDEX `cmdb_historicaldevic_history_user_id_fc7deca8_fk_rbac_user`(`history_user_id`) USING BTREE,
  INDEX `cmdb_historicaldeviceinfo_id_3be8b451`(`id`) USING BTREE,
  INDEX `cmdb_historicaldeviceinfo_changed_by_id_34b3603c`(`changed_by_id`) USING BTREE,
  CONSTRAINT `cmdb_historicaldevic_history_user_id_fc7deca8_fk_rbac_user` FOREIGN KEY (`history_user_id`) REFERENCES `rbac_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of cmdb_historicaldeviceinfo
-- ----------------------------
INSERT INTO `cmdb_historicaldeviceinfo` VALUES (1, 'online', 'xops\r\n', '00:0c:29:55:56:eb\r\n', 'VMware-56 4d c8 fb b0 d9 3c 2b-62 7c bb 44 fe 55 56 eb\r\n', 'Linux', 'CentOS Linux release 7.5.1804 (Core) \r\n', '', '', 'password', '192.168.3.33', NULL, NULL, NULL, '2019-03-23', '2019-03-23', '', 1, '2019-03-23 15:09:43.799458', NULL, '+', 1, 1);

-- ----------------------------
-- Table structure for deployment_deployrecord
-- ----------------------------
DROP TABLE IF EXISTS `deployment_deployrecord`;
CREATE TABLE `deployment_deployrecord`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime(6) NOT NULL,
  `modify_time` datetime(6) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `record_id` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `alias` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `project_id` int(11) NULL DEFAULT NULL,
  `server_ids` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `target_root` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `target_releases` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `prev_record` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_rollback` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for deployment_project
-- ----------------------------
DROP TABLE IF EXISTS `deployment_project`;
CREATE TABLE `deployment_project`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime(6) NOT NULL,
  `modify_time` datetime(6) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `alias` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `environment` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `excludes` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `is_include` tinyint(1) NOT NULL,
  `target_root` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `target_releases` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `task_envs` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `prev_deploy` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `post_deploy` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `prev_release` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `post_release` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `version_num` int(11) NULL DEFAULT NULL,
  `repo_url` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `repo_mode` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `server_ids` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `last_task_status` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `app_start` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `app_stop` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `app_log_file` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of deployment_project
-- ----------------------------
INSERT INTO `deployment_project` VALUES (1, '2019-03-23 15:17:58.353902', '2019-03-25 15:23:31.851606', '12348账套', 'ledger', 'dev', NULL, 'README.md', 0, '/home/test/xops', '/home/test/release', 'nihao=/home/nihao\ndede=/home/dede', 'echo \'这是部署前的任务，如代码编译\'\necho \'显示自定义变量\'\necho {nihao}\necho {dede}', 'echo \'这是部署后置任务，即上传代码至目标服务器之前的任务\'', 'echo \'这是发布前置任务，即上传代码至目标服务器后，准备发布前的任务，如停止服务\'', 'echo \'这是完成后的任务，如启动服务\'', 5, 'asdasd', 'branch', '1', '', '/home/test/start.sh', '/home/test/stop.sh', '/var/log/messages');

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (2, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (1, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (10, 'cmdb', 'business');
INSERT INTO `django_content_type` VALUES (11, 'cmdb', 'connectioninfo');
INSERT INTO `django_content_type` VALUES (12, 'cmdb', 'devicefile');
INSERT INTO `django_content_type` VALUES (13, 'cmdb', 'deviceinfo');
INSERT INTO `django_content_type` VALUES (14, 'cmdb', 'devicescaninfo');
INSERT INTO `django_content_type` VALUES (15, 'cmdb', 'dict');
INSERT INTO `django_content_type` VALUES (16, 'cmdb', 'historicaldeviceinfo');
INSERT INTO `django_content_type` VALUES (3, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (17, 'deployment', 'deployrecord');
INSERT INTO `django_content_type` VALUES (18, 'deployment', 'project');
INSERT INTO `django_content_type` VALUES (6, 'rbac', 'menu');
INSERT INTO `django_content_type` VALUES (7, 'rbac', 'organization');
INSERT INTO `django_content_type` VALUES (8, 'rbac', 'permission');
INSERT INTO `django_content_type` VALUES (9, 'rbac', 'role');
INSERT INTO `django_content_type` VALUES (5, 'rbac', 'userprofile');
INSERT INTO `django_content_type` VALUES (4, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2019-03-23 14:00:01.554949');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2019-03-23 14:00:01.592232');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2019-03-23 14:00:01.681293');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2019-03-23 14:00:01.698774');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2019-03-23 14:00:01.710296');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2019-03-23 14:00:01.718645');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2019-03-23 14:00:01.729591');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2019-03-23 14:00:01.731390');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2019-03-23 14:00:01.739359');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2019-03-23 14:00:01.750177');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2019-03-23 14:00:01.757334');
INSERT INTO `django_migrations` VALUES (12, 'rbac', '0001_initial', '2019-03-23 14:00:02.374572');
INSERT INTO `django_migrations` VALUES (13, 'cmdb', '0001_initial', '2019-03-23 14:00:02.665535');
INSERT INTO `django_migrations` VALUES (14, 'deployment', '0001_initial', '2019-03-23 14:00:02.719533');
INSERT INTO `django_migrations` VALUES (15, 'sessions', '0001_initial', '2019-03-23 14:00:02.735608');
INSERT INTO `django_migrations` VALUES (16, 'deployment', '0002_auto_20190325_1516', '2019-03-25 15:16:57.650824');
INSERT INTO `django_migrations` VALUES (17, 'deployment', '0003_auto_20190325_1523', '2019-03-25 15:23:29.094700');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

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

-- ----------------------------
-- Records of rbac_menu
-- ----------------------------
INSERT INTO `rbac_menu` VALUES (1, '系统管理', 'system', 'system', 0, 1, 0, NULL, NULL);
INSERT INTO `rbac_menu` VALUES (2, '用户管理', 'user', 'users', 0, 1, 11, 'system/user/index', 1);
INSERT INTO `rbac_menu` VALUES (3, '菜单管理', 'menu', 'menus', 0, 1, 12, 'system/menu/index', 1);
INSERT INTO `rbac_menu` VALUES (4, '角色管理', 'role', 'roles', 0, 1, 14, 'system/role/index', 1);
INSERT INTO `rbac_menu` VALUES (5, '权限管理', 'permission', 'permissions', 0, 1, 13, 'system/permission/index', 1);
INSERT INTO `rbac_menu` VALUES (6, '组织架构', 'peoples', 'organizations', 0, 1, 15, 'system/organization/index', 1);
INSERT INTO `rbac_menu` VALUES (7, '配置中心', 'github', 'cmdb', 0, 1, 1, '', NULL);
INSERT INTO `rbac_menu` VALUES (8, '数据字典', 'tools', 'dicts', 0, 1, 11, 'cmdb/dict/index', 7);
INSERT INTO `rbac_menu` VALUES (9, '资产管理', 'lock', 'asset', 0, 1, 13, 'cmdb/asset/index', 7);
INSERT INTO `rbac_menu` VALUES (10, '设备扫描', 'develop', 'scan', 0, 1, 111, 'cmdb/asset/scan/index', 9);
INSERT INTO `rbac_menu` VALUES (11, '设备管理', 'error', 'devices', 0, 1, 112, 'cmdb/asset/device/index', 9);
INSERT INTO `rbac_menu` VALUES (12, '扫描详情', 'add', 'scan/detail', 0, 0, 999, 'cmdb/asset/scan/detail/index', 9);
INSERT INTO `rbac_menu` VALUES (13, '密码管理', 'icon', 'connections', 0, 1, 12, 'cmdb/passwd/index', 7);
INSERT INTO `rbac_menu` VALUES (15, '设备详情', '', 'devices/detail', 0, 0, 999, 'cmdb/asset/device/detail/index', 9);
INSERT INTO `rbac_menu` VALUES (16, '业务管理', 'monitor', 'businesses', 0, 1, 14, 'cmdb/business/index', 7);
INSERT INTO `rbac_menu` VALUES (17, '持续构建', 'add', 'deploy', 0, 1, 3, 'deployment/index', NULL);
INSERT INTO `rbac_menu` VALUES (18, '项目配置', 'tools', 'projects', 0, 1, 11, 'deployment/project/index', 17);
INSERT INTO `rbac_menu` VALUES (19, '新建项目', '', 'projects/create', 0, 0, 999, 'deployment/project/form.vue', 17);
INSERT INTO `rbac_menu` VALUES (20, '项目详情', '', 'projects/detail', 0, 0, 999, 'deployment/project/form.vue', 17);
INSERT INTO `rbac_menu` VALUES (21, '部署管理', 'github', 'tasks', 0, 1, 12, 'deployment/task/index', 17);
INSERT INTO `rbac_menu` VALUES (22, '部署发布', '', 'tasks/publish', 0, 0, 999, 'deployment/task/publish', 17);
INSERT INTO `rbac_menu` VALUES (23, '控制台', '', 'tasks/console', 0, 0, 999, 'deployment/task/console', 17);
INSERT INTO `rbac_menu` VALUES (24, '工具箱', '', 'tasks/tools', 0, 0, 999, 'deployment/task/tools_tabs', 17);

-- ----------------------------
-- Table structure for rbac_organization
-- ----------------------------
DROP TABLE IF EXISTS `rbac_organization`;
CREATE TABLE `rbac_organization`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `pid_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `rbac_organization_pid_id_0cf751aa_fk_rbac_organization_id`(`pid_id`) USING BTREE,
  CONSTRAINT `rbac_organization_pid_id_0cf751aa_fk_rbac_organization_id` FOREIGN KEY (`pid_id`) REFERENCES `rbac_organization` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for rbac_permission
-- ----------------------------
DROP TABLE IF EXISTS `rbac_permission`;
CREATE TABLE `rbac_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `method` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pid_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `rbac_permission_pid_id_6939354d_fk_rbac_permission_id`(`pid_id`) USING BTREE,
  CONSTRAINT `rbac_permission_pid_id_6939354d_fk_rbac_permission_id` FOREIGN KEY (`pid_id`) REFERENCES `rbac_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 55 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of rbac_permission
-- ----------------------------
INSERT INTO `rbac_permission` VALUES (1, '系统管理员', 'admin', NULL);
INSERT INTO `rbac_permission` VALUES (2, '用户管理', 'user_all', NULL);
INSERT INTO `rbac_permission` VALUES (3, '用户列表', 'user_list', 2);
INSERT INTO `rbac_permission` VALUES (4, '用户创建', 'user_create', 2);
INSERT INTO `rbac_permission` VALUES (5, '用户编辑', 'user_edit', 2);
INSERT INTO `rbac_permission` VALUES (6, '用户删除', 'user_delete', 2);
INSERT INTO `rbac_permission` VALUES (7, '菜单管理', 'menu_all', NULL);
INSERT INTO `rbac_permission` VALUES (8, '菜单列表', 'menu_list', 7);
INSERT INTO `rbac_permission` VALUES (9, '菜单创建', 'menu_create', 7);
INSERT INTO `rbac_permission` VALUES (10, '菜单编辑', 'menu_edit', 7);
INSERT INTO `rbac_permission` VALUES (11, '菜单删除', 'menu_delete', 7);
INSERT INTO `rbac_permission` VALUES (12, '角色管理', 'role_all', NULL);
INSERT INTO `rbac_permission` VALUES (13, '角色列表', 'role_list', 12);
INSERT INTO `rbac_permission` VALUES (14, '角色创建', 'role_create', 12);
INSERT INTO `rbac_permission` VALUES (15, '角色编辑', 'role_edit', 12);
INSERT INTO `rbac_permission` VALUES (16, '角色删除', 'role_delete', 12);
INSERT INTO `rbac_permission` VALUES (17, '权限管理', 'permission_all', NULL);
INSERT INTO `rbac_permission` VALUES (18, '权限列表', 'permission_list', 17);
INSERT INTO `rbac_permission` VALUES (19, '权限创建', 'permission_create', 17);
INSERT INTO `rbac_permission` VALUES (20, '权限编辑', 'permission_edit', 17);
INSERT INTO `rbac_permission` VALUES (21, '权限删除', 'permission_delete', 17);
INSERT INTO `rbac_permission` VALUES (22, '组织管理', 'organization_all', NULL);
INSERT INTO `rbac_permission` VALUES (23, '组织列表', 'organization_list', 22);
INSERT INTO `rbac_permission` VALUES (24, '组织创建', 'organization_create', 22);
INSERT INTO `rbac_permission` VALUES (25, '组织编辑', 'organization_edit', 22);
INSERT INTO `rbac_permission` VALUES (26, '组织删除', 'organization_delete', 22);
INSERT INTO `rbac_permission` VALUES (27, '字典管理', 'dict_all', NULL);
INSERT INTO `rbac_permission` VALUES (28, '字典列表', 'dict_list', 27);
INSERT INTO `rbac_permission` VALUES (29, '字典创建', 'dict_create', 27);
INSERT INTO `rbac_permission` VALUES (30, '字典修改', 'dict_edit', 27);
INSERT INTO `rbac_permission` VALUES (31, '字典删除', 'dict_delete', 27);
INSERT INTO `rbac_permission` VALUES (32, '设备管理', 'device_all', NULL);
INSERT INTO `rbac_permission` VALUES (33, '设备列表', 'device_list', 32);
INSERT INTO `rbac_permission` VALUES (34, '设备创建', '设备_create', 32);
INSERT INTO `rbac_permission` VALUES (35, '设备编辑', 'device_edit', 32);
INSERT INTO `rbac_permission` VALUES (36, '设备删除', 'device_delete', 32);
INSERT INTO `rbac_permission` VALUES (37, '设备扫描', 'scan_all', NULL);
INSERT INTO `rbac_permission` VALUES (38, '密码管理', 'connection_all', NULL);
INSERT INTO `rbac_permission` VALUES (39, '密码列表', 'connection_list', 38);
INSERT INTO `rbac_permission` VALUES (40, '密码创建', 'connection_create', 38);
INSERT INTO `rbac_permission` VALUES (41, '密码编辑', 'connection_edit', 38);
INSERT INTO `rbac_permission` VALUES (42, '密码删除', 'connection_delete', 38);
INSERT INTO `rbac_permission` VALUES (43, '业务管理', 'business_all', NULL);
INSERT INTO `rbac_permission` VALUES (44, '业务列表', 'business_list', 43);
INSERT INTO `rbac_permission` VALUES (45, '业务新建', 'business_create', 43);
INSERT INTO `rbac_permission` VALUES (46, '业务编辑', 'business_edit', 43);
INSERT INTO `rbac_permission` VALUES (47, '业务删除', 'business_delete', 43);
INSERT INTO `rbac_permission` VALUES (48, '项目管理', 'project_all', NULL);
INSERT INTO `rbac_permission` VALUES (49, '项目列表', 'project_list', 48);
INSERT INTO `rbac_permission` VALUES (50, '项目创建', 'project_create', 48);
INSERT INTO `rbac_permission` VALUES (51, '项目编辑', 'project_edit', 48);
INSERT INTO `rbac_permission` VALUES (52, '项目删除', 'project_delete', 48);
INSERT INTO `rbac_permission` VALUES (53, '部署管理', 'deploy_all', NULL);
INSERT INTO `rbac_permission` VALUES (54, '部署执行', 'deploy_excu', 53);

-- ----------------------------
-- Table structure for rbac_role
-- ----------------------------
DROP TABLE IF EXISTS `rbac_role`;
CREATE TABLE `rbac_role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `desc` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of rbac_role
-- ----------------------------
INSERT INTO `rbac_role` VALUES (1, '系统管理员', '系统默认管理员');
INSERT INTO `rbac_role` VALUES (2, '开发攻城狮', '');

-- ----------------------------
-- Table structure for rbac_role_menus
-- ----------------------------
DROP TABLE IF EXISTS `rbac_role_menus`;
CREATE TABLE `rbac_role_menus`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `rbac_role_menus_role_id_menu_id_579f5861_uniq`(`role_id`, `menu_id`) USING BTREE,
  INDEX `rbac_role_menus_menu_id_180f4f9a_fk_rbac_menu_id`(`menu_id`) USING BTREE,
  CONSTRAINT `rbac_role_menus_menu_id_180f4f9a_fk_rbac_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `rbac_menu` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `rbac_role_menus_role_id_323259a4_fk_rbac_role_id` FOREIGN KEY (`role_id`) REFERENCES `rbac_role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of rbac_role_menus
-- ----------------------------
INSERT INTO `rbac_role_menus` VALUES (11, 2, 7);
INSERT INTO `rbac_role_menus` VALUES (8, 2, 9);
INSERT INTO `rbac_role_menus` VALUES (9, 2, 11);
INSERT INTO `rbac_role_menus` VALUES (10, 2, 15);
INSERT INTO `rbac_role_menus` VALUES (1, 2, 17);
INSERT INTO `rbac_role_menus` VALUES (2, 2, 18);
INSERT INTO `rbac_role_menus` VALUES (3, 2, 20);
INSERT INTO `rbac_role_menus` VALUES (4, 2, 21);
INSERT INTO `rbac_role_menus` VALUES (5, 2, 22);
INSERT INTO `rbac_role_menus` VALUES (6, 2, 23);
INSERT INTO `rbac_role_menus` VALUES (7, 2, 24);

-- ----------------------------
-- Table structure for rbac_role_permissions
-- ----------------------------
DROP TABLE IF EXISTS `rbac_role_permissions`;
CREATE TABLE `rbac_role_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `rbac_role_permissions_role_id_permission_id_d01303da_uniq`(`role_id`, `permission_id`) USING BTREE,
  INDEX `rbac_role_permission_permission_id_f5e1e866_fk_rbac_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `rbac_role_permission_permission_id_f5e1e866_fk_rbac_perm` FOREIGN KEY (`permission_id`) REFERENCES `rbac_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `rbac_role_permissions_role_id_d10416cb_fk_rbac_role_id` FOREIGN KEY (`role_id`) REFERENCES `rbac_role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of rbac_role_permissions
-- ----------------------------
INSERT INTO `rbac_role_permissions` VALUES (1, 1, 1);
INSERT INTO `rbac_role_permissions` VALUES (4, 2, 28);
INSERT INTO `rbac_role_permissions` VALUES (5, 2, 33);
INSERT INTO `rbac_role_permissions` VALUES (6, 2, 37);
INSERT INTO `rbac_role_permissions` VALUES (3, 2, 49);
INSERT INTO `rbac_role_permissions` VALUES (2, 2, 53);

-- ----------------------------
-- Table structure for rbac_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `rbac_userprofile`;
CREATE TABLE `rbac_userprofile`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mobile` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `image` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `position` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `department_id` int(11) NULL DEFAULT NULL,
  `superior_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  INDEX `rbac_userprofile_department_id_d0f32bd9_fk_rbac_organization_id`(`department_id`) USING BTREE,
  INDEX `rbac_userprofile_superior_id_5d0a3780_fk_rbac_userprofile_id`(`superior_id`) USING BTREE,
  CONSTRAINT `rbac_userprofile_department_id_d0f32bd9_fk_rbac_organization_id` FOREIGN KEY (`department_id`) REFERENCES `rbac_organization` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `rbac_userprofile_superior_id_5d0a3780_fk_rbac_userprofile_id` FOREIGN KEY (`superior_id`) REFERENCES `rbac_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of rbac_userprofile
-- ----------------------------
INSERT INTO `rbac_userprofile` VALUES (1, 'pbkdf2_sha256$120000$x1BJWT08v5wv$XvBakLaY4INeWqgeIPKvbl3vLVepG56iUmahSE9I8iE=', NULL, 1, 'admin', '', '', 1, 1, '2019-03-23 14:01:30.868481', '管理员', '', 'admin@admin.com', 'image/default.png', NULL, NULL, NULL);
INSERT INTO `rbac_userprofile` VALUES (2, 'pbkdf2_sha256$120000$ydbt6ieD48rX$dk2jIXjAxG9prsYnbvlZQcQCD2EhuGEmcgmQbKr6/QI=', NULL, 0, 'dev', '', '', 0, 1, '2019-03-23 14:22:30.504902', '开发人员', '13710945544', 'dev@test.com', 'image/default.png', '', NULL, NULL);

-- ----------------------------
-- Table structure for rbac_userprofile_groups
-- ----------------------------
DROP TABLE IF EXISTS `rbac_userprofile_groups`;
CREATE TABLE `rbac_userprofile_groups`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `rbac_userprofile_groups_userprofile_id_group_id_4d710b30_uniq`(`userprofile_id`, `group_id`) USING BTREE,
  INDEX `rbac_userprofile_groups_group_id_2c47610b_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `rbac_userprofile_gro_userprofile_id_9cacde37_fk_rbac_user` FOREIGN KEY (`userprofile_id`) REFERENCES `rbac_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `rbac_userprofile_groups_group_id_2c47610b_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for rbac_userprofile_roles
-- ----------------------------
DROP TABLE IF EXISTS `rbac_userprofile_roles`;
CREATE TABLE `rbac_userprofile_roles`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `rbac_userprofile_roles_userprofile_id_role_id_ba9254c5_uniq`(`userprofile_id`, `role_id`) USING BTREE,
  INDEX `rbac_userprofile_roles_role_id_ddc12d7e_fk_rbac_role_id`(`role_id`) USING BTREE,
  CONSTRAINT `rbac_userprofile_rol_userprofile_id_3a7afbe9_fk_rbac_user` FOREIGN KEY (`userprofile_id`) REFERENCES `rbac_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `rbac_userprofile_roles_role_id_ddc12d7e_fk_rbac_role_id` FOREIGN KEY (`role_id`) REFERENCES `rbac_role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of rbac_userprofile_roles
-- ----------------------------
INSERT INTO `rbac_userprofile_roles` VALUES (1, 1, 1);
INSERT INTO `rbac_userprofile_roles` VALUES (2, 2, 2);

-- ----------------------------
-- Table structure for rbac_userprofile_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `rbac_userprofile_user_permissions`;
CREATE TABLE `rbac_userprofile_user_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `rbac_userprofile_user_pe_userprofile_id_permissio_16bbd20f_uniq`(`userprofile_id`, `permission_id`) USING BTREE,
  INDEX `rbac_userprofile_use_permission_id_740ad67c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `rbac_userprofile_use_permission_id_740ad67c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `rbac_userprofile_use_userprofile_id_38afd71d_fk_rbac_user` FOREIGN KEY (`userprofile_id`) REFERENCES `rbac_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
