/*
 Navicat Premium Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 80022
 Source Host           : localhost:3306
 Source Schema         : sushe

 Target Server Type    : MySQL
 Target Server Version : 80022
 File Encoding         : 65001

 Date: 22/11/2020 17:02:24
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for m_table
-- ----------------------------
DROP TABLE IF EXISTS `m_table`;
CREATE TABLE `m_table`  (
  `MID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Mname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Msex` int(0) NULL DEFAULT NULL,
  `Mage` int(0) NULL DEFAULT NULL,
  `Mphone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`MID`) USING BTREE,
  INDEX `Mname`(`Mname`) USING BTREE,
  INDEX `MID`(`MID`, `Mname`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for s_table
-- ----------------------------
DROP TABLE IF EXISTS `s_table`;
CREATE TABLE `s_table`  (
  `Lno` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Sno` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `L_n` int(0) NULL DEFAULT NULL,
  `C_n` int(0) NULL DEFAULT NULL,
  `K_n` int(0) NULL DEFAULT NULL,
  `Location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Lno`, `Sno`) USING BTREE,
  INDEX `Sno`(`Sno`) USING BTREE,
  INDEX `Lno`(`Lno`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for x_table
-- ----------------------------
DROP TABLE IF EXISTS `x_table`;
CREATE TABLE `x_table`  (
  `SID` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Sname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Ssex` int(0) NULL DEFAULT NULL,
  `Lno` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Sno` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `MID` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Mname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`SID`) USING BTREE,
  INDEX `宿舍ID`(`Lno`, `Sno`) USING BTREE,
  INDEX `宿管`(`MID`) USING BTREE,
  INDEX `宿管ID`(`Mname`) USING BTREE,
  INDEX `宿舍号`(`Sno`) USING BTREE,
  CONSTRAINT `宿管` FOREIGN KEY (`MID`) REFERENCES `m_table` (`MID`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `宿管ID` FOREIGN KEY (`Mname`) REFERENCES `m_table` (`Mname`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `宿舍号` FOREIGN KEY (`Sno`) REFERENCES `s_table` (`Sno`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `楼号` FOREIGN KEY (`Lno`) REFERENCES `s_table` (`Lno`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
