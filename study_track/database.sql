-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: database
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `course_code` varchar(15) NOT NULL COMMENT '课程代码',
  `course_name` varchar(100) NOT NULL,
  `credit` float NOT NULL,
  PRIMARY KEY (`course_code`),
  CONSTRAINT `courses_chk_1` CHECK ((`credit` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES ('AI101','人工智能基础',2),('CS101','计算机导论',3),('CS102','程序设计基础',4),('CS201','数据结构',3),('CS202','计算机组成原理',3),('CS301','操作系统',3),('CS302','数据库系统',3),('CS303','计算机网络',3),('DS101','数据分析导论',2),('SE101','软件工程导论',2);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grades`
--

DROP TABLE IF EXISTS `grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_no` varchar(20) NOT NULL COMMENT '学号',
  `course_code` varchar(15) NOT NULL COMMENT '课程代码',
  `score` float NOT NULL,
  `semester` varchar(15) NOT NULL COMMENT '格式: YYYY-学期 如2023秋',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_grade_record` (`student_no`,`course_code`,`semester`),
  KEY `course_code` (`course_code`),
  CONSTRAINT `grades_ibfk_1` FOREIGN KEY (`student_no`) REFERENCES `students` (`student_no`) ON DELETE CASCADE,
  CONSTRAINT `grades_ibfk_2` FOREIGN KEY (`course_code`) REFERENCES `courses` (`course_code`) ON DELETE CASCADE,
  CONSTRAINT `grades_chk_1` CHECK ((`score` between 0 and 100))
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` VALUES (20,'S20230001','CS101',85,'2023春'),(21,'S20230001','CS102',78,'2023Fall'),(22,'S20230001','CS201',88,'2024春'),(23,'S20230002','CS101',90,'2023秋'),(24,'S20230002','CS102',84,'2023秋'),(25,'S20230002','CS201',81,'2024春'),(26,'S20230003','CS101',75,'2023秋'),(27,'S20230003','AI101',92,'2023秋'),(28,'S20230003','CS201',70,'2024春'),(29,'S20230004','CS101',68,'2023秋'),(80,'S20230011','AI101',89,'2024秋');
/*!40000 ALTER TABLE `grades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester_gpa`
--

DROP TABLE IF EXISTS `semester_gpa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semester_gpa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_no` varchar(20) NOT NULL COMMENT '学号',
  `semester` varchar(15) NOT NULL,
  `semester_gpa` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_semester_record` (`student_no`,`semester`),
  CONSTRAINT `semester_gpa_ibfk_1` FOREIGN KEY (`student_no`) REFERENCES `students` (`student_no`) ON DELETE CASCADE,
  CONSTRAINT `semester_gpa_chk_1` CHECK ((`semester_gpa` between 0 and 4.0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester_gpa`
--

LOCK TABLES `semester_gpa` WRITE;
/*!40000 ALTER TABLE `semester_gpa` DISABLE KEYS */;
INSERT INTO `semester_gpa` VALUES (1,'S20230001','2023Fall',2.43),(2,'S20230002','2023秋',3.43),(3,'S20230001','2024春',3.7),(4,'S20230002','2024秋',3.7),(5,'S20230004','2024秋',3.7),(6,'S20230005','2024秋',3.85),(7,'S20230001','2024秋',4),(8,'S20230008','2024秋',3.7),(9,'S20230011','2024秋',3.7),(10,'S20230006','2024秋',3.7);
/*!40000 ALTER TABLE `semester_gpa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_no` varchar(20) NOT NULL COMMENT '学号',
  `name` varchar(30) NOT NULL,
  `major` varchar(30) NOT NULL COMMENT '专业',
  `grade` varchar(30) NOT NULL,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '账户名',
  `school` varchar(255) NOT NULL COMMENT '学校',
  `college` varchar(255) NOT NULL COMMENT '学院',
  `password` varchar(255) NOT NULL COMMENT '密码',
  PRIMARY KEY (`student_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES ('20230001','张三','计算机科学','大三','zhangsan','清华大学','计算机学院','$2b$12$s8Df0WWYRTyN94X.bo4EoupKJBF6PNEf0g5sW1aWBhmV7tB.lgIB6'),('S20230001','张三','计算机科学与技术','大三','zhangsan123','清华大学','信息科学技术学院',''),('S20230002','李丽','软件工程','大三','S20230001@seu.edu.cn','东南大学','计算机科学与工程学院',''),('S20230003','王强','人工智能','大三','S20230001@seu.edu.cn','东南大学','东南大学计算机科学与工程学院',''),('S20230004','赵敏','网络工程','大三','S20230001@seu.edu.cn','东南大学','计算机科学与工程学院',''),('S20230005','陈晨','数据科学与大数据技术','大三','S20230001@seu.edu.cn','东南大学','计算机科学与工程学院',''),('S20230006','刘洋','计算机科学与技术','大二','S20230001@seu.edu.cn','东南大学','计算机科学与工程学院',''),('S20230007','孙娜','软件工程','大二','S20230001@seu.edu.cn','东南大学','计算机科学与工程学院',''),('S20230008','周杰','人工智能','大二','S20230001@seu.edu.cn','东南大学','计算机科学与工程学院',''),('S20230009','李四','计算机科学','2023','lisi','清华大学','计算机学院','$2b$12$5TeMTqze8K7UE7eq/NGcW.KN/.LpcDP5He12f5Yvr5P59F2/Nonpy'),('S20230010','王五','计算机科学','2023','S20230010@seu.edu.cn','清华大学','计算机学院','$2b$12$PV/eEYPMVpnouvpDrNGHouHPaYz.6MQzIozNO3BgImzS7RZFiaIc6'),('S20230011','王五','计算机科学','2023','S20230011@seu.edu.cn','清华大学','计算机学院','$2b$12$li68L/BCSaB73qLVSc8l.OmR1aiPfIyq3hGsobM3DIH6PmvjiURw2');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `study_advices`
--

DROP TABLE IF EXISTS `study_advices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `study_advices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_no` varchar(20) NOT NULL COMMENT '学号',
  `advice` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_no` (`student_no`),
  CONSTRAINT `study_advices_ibfk_1` FOREIGN KEY (`student_no`) REFERENCES `students` (`student_no`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `study_advices`
--

LOCK TABLES `study_advices` WRITE;
/*!40000 ALTER TABLE `study_advices` DISABLE KEYS */;
INSERT INTO `study_advices` VALUES (1,'S20230001','根据学生提供的计算机科学与技术专业大三成绩单，结合课程关联性和专业发展需求，以下是针对性分析及建议：\n\n---\n\n### 一、优势学科与待加强学科分析\n1. **优势学科**  \n   - **数据结构（88分）**：成绩显著高于其他课程，说明对数据组织方式、基础算法（排序/查找）和逻辑抽象能力掌握扎实，具备解决复杂问题的潜力。  \n   - **计算机导论（85分）**：对计算机体系结构、操作系统基础等宏观概念理解到位，为后续系统级课程（如计算机网络）奠定基础。\n\n2. **待加强学科**  \n   - **程序设计基础（78分）**：可能需关注编程实践能力（如代码调试、复杂逻辑实现）和算法设计规范性（如边界条件处理）。此课程是后续编译原理、算法设计的核心前置课，建议重点提升。\n\n---\n\n### 二、专业核心课程掌握情况\n| 课程              | 关联性分析                                                                 | 建议方向                                                                 |\n|-------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------|\n| **数据结构**      | 与算法分析、数据库系统强关联，88分表明具备实现链表/树/图的能力。           | 深化动态规划、图算法（如Dijkstra）的代码实现，尝试LeetCode中等难度题目。 |\n| **程序设计基础**  | 低分可能反映面向对象编程（OOP）或递归逻辑的薄弱，影响后续软件工程课程。    | 通过GitHub开源项目（如小型管理系统）强化工程化编码习惯。                 |\n| **计算机导论**    | 硬件层（CPU/内存）与软件层（进程管理）的衔接能力较强。                    | 结合《CSAPP》教材实践Lab项目（如缓存优化），提升系统视角。               |\n\n---\n\n### 三、跨学科知识衔接建议\n1. **数学基础强化**  \n   - **离散数学**：直接影响算法设计与密码学课程，建议补充命题逻辑、图论证明题训练。  \n   - **概率统计**：为机器学习（如贝叶斯分类）做准备，可借助《概率导论》配套MIT公开课。\n\n2. **硬件/系统层扩展**  \n   - 若对嵌入式开发感兴趣，需补充数字电路（如FPGA编程）；若侧重系统开发，建议提前学习《操作系统导论》中的虚拟化与并发章节。\n\n3. **前沿领域交叉**  \n   - 人工智能方向需关注Python科学计算库（NumPy/Pandas）；区块链开发需补足密码学基础。\n\n---\n\n### 四、学习资源推荐\n| 类别                | 推荐内容                                                                 |\n|---------------------|--------------------------------------------------------------------------|\n| **编程能力提升**    | - 书籍：《算法（第4版）》图解版<br>- 平台：Codeforces（竞赛级题目训练） |\n| **系统底层深化**    | - 课程：CMU 15-213 CSAPP（中文字幕版）<br>- 实验：xv6操作系统源码剖析    |\n| **跨学科工具**      | - 数学：3Blue1Brown线性代数动画系列<br>- 数据科学：Kaggle入门竞赛实战     |\n| **工程实践**        | - 参与GSoC（谷歌编程之夏）开源项目<br>- 开发全栈项目（如基于Spring Boot的分布式系统） |\n\n---\n\n### 总结建议\n当前应聚焦**程序设计基础**的实践短板，结合数据结构优势构建算法-工程双能力；同时通过《CSAPP》等资源打通软硬件知识断层。若计划考研或留学，需在数学建模（如美赛）或科研项目（如CV/NLP）中积累差异化竞争力。');
/*!40000 ALTER TABLE `study_advices` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-21 23:42:07
