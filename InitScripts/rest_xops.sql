/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50642
 Source Host           : localhost:3306
 Source Schema         : rest_xops

 Target Server Type    : MySQL
 Target Server Version : 50642
 File Encoding         : 65001

 Date: 11/02/2019 11:07:31
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
) ENGINE = InnoDB AUTO_INCREMENT = 37 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

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
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (2, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (1, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (3, 'contenttypes', 'contenttype');
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
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2019-02-10 22:17:27.346000');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2019-02-10 22:17:27.475000');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2019-02-10 22:17:27.850000');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2019-02-10 22:17:27.928000');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2019-02-10 22:17:27.946000');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2019-02-10 22:17:27.962000');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2019-02-10 22:17:27.979000');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2019-02-10 22:17:27.987000');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2019-02-10 22:17:28.002000');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2019-02-10 22:17:28.017000');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2019-02-10 22:17:28.031000');
INSERT INTO `django_migrations` VALUES (12, 'rbac', '0001_initial', '2019-02-10 22:17:29.755000');
INSERT INTO `django_migrations` VALUES (13, 'sessions', '0001_initial', '2019-02-10 22:17:29.827000');

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
  `sort` int(11) NULL DEFAULT NULL,
  `component` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `pid_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `rbac_menu_pid_id_a43b3c84_fk_rbac_menu_id`(`pid_id`) USING BTREE,
  CONSTRAINT `rbac_menu_pid_id_a43b3c84_fk_rbac_menu_id` FOREIGN KEY (`pid_id`) REFERENCES `rbac_menu` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of rbac_menu
-- ----------------------------
INSERT INTO `rbac_menu` VALUES (1, '系统管理', 'system', 'system', 0, 0, NULL, NULL);
INSERT INTO `rbac_menu` VALUES (2, '用户管理', 'user', 'users', 0, 1, 'system/user/index', 1);
INSERT INTO `rbac_menu` VALUES (3, '菜单管理', 'menu', 'menus', 0, 2, 'system/menu/index', 1);
INSERT INTO `rbac_menu` VALUES (4, '角色管理', 'role', 'roles', 0, 4, 'system/role/index', 1);
INSERT INTO `rbac_menu` VALUES (5, '权限管理', 'permission', 'permissions', 0, 3, 'system/permission/index', 1);
INSERT INTO `rbac_menu` VALUES (6, '组织架构', 'peoples', 'organizations', 0, 5, 'system/organization/index', 1);

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
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of rbac_role
-- ----------------------------
INSERT INTO `rbac_role` VALUES (1, '系统管理员', '系统默认管理员');

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of rbac_role_permissions
-- ----------------------------
INSERT INTO `rbac_role_permissions` VALUES (1, 1, 1);

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of rbac_userprofile
-- ----------------------------
INSERT INTO `rbac_userprofile` VALUES (1, 'pbkdf2_sha256$120000$kIuV8Zaxl3xO$e+0RQyO3oSWdCEd4CM2Bys2tdW/ok2Bboj9UimfAgTY=', NULL, 1, 'admin', '', '', 1, 1, '2019-02-10 22:18:04.221000', '管理员', '', 'admin@admin.com', 'image/default.png', NULL, NULL, NULL);

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of rbac_userprofile_roles
-- ----------------------------
INSERT INTO `rbac_userprofile_roles` VALUES (1, 1, 1);

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
