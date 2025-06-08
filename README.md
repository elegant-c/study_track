# 📚 学业追踪平台 | Academic Tracker

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Vue](https://img.shields.io/badge/Vue-3.x-brightgreen.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**学业追踪平台** 是一个基于Python/FastAPI + Vue.js + MySQL的全栈项目，致力于为师生提供智能化学业管理解决方案。平台包含四大核心模块，实现从用户管理到AI辅助分析的全流程覆盖。

## 🌟 项目特色
- 🔐 **角色认证系统**：学生通过学校信息认证
- 📊 **数据可视化**：成绩趋势图、
- 🤖 **AI学业分析**：基于大模型的成绩预测、学习建议生成

## 🛠 技术栈
| 分类       | 技术选型                          |
|------------|---------------------------------|
| **前端**   | Vue 3.x + Pinia + Vite + Element Plus |
| **后端**   | FastAPI + Uvicorn + mysql       |
| **数据库** | MySQL 8.x           |
| **AI模块** | Deepseek-reasoner |
| **部署**   | 华为云服务器              |

## 📌 核心功能模块

### 1. 用户验证系统
- 学校+学号+姓名认证
- 密码强度校验与加密存储

### 2. 用户信息管理
- 👨🎓 学生端：个人信息维护、密码修改

### 3. 成绩管理系统
- 📝 成绩录入
- 📈 动态成绩曲线（按学期计算GPA）


### 4. AI辅助模块
- 🔮 成绩预测：基于历史数据预测未来成绩趋势
- 📚 智能推荐：针对薄弱科目生成学习建议

## 🚀 快速开始

### 环境要求
| 服务   | 依赖项                          |
|--------|-------------------------------|
| **前端** | Node.js 18+ / npm 9+          |
| **后端** | Python 3.9+ / pip 22+         |
| **数据库** | MySQL 8.x          |

### 项目部署（Python/FastAPI/Vue）
###后端
```bash
# 克隆仓库
git clone https://github.com/yourname/academic-tracker-backend.git
cd academic-tracker-backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置MySQL数据库
# 1. 创建数据库：CREATE DATABASE academic_db;
# 2. 修改.env文件配置：
cp .env.example .env
# 填写DB_NAME/DB_USER/DB_PASSWORD等字段

# 初始化数据
alembic upgrade head  # 数据库迁移

# 启动开发服务器（带自动重载）
uvicorn main:app --reload --log-level debug

# 访问API文档：http://localhost:8000/docs
###  前端部署（Vue.js）
```bash
# 克隆仓库
git clone https://github.com/yourname/academic-tracker-frontend.git
cd academic-tracker-frontend

# 安装依赖
npm install

# 配置API地址（.env.development）
VITE_API_BASE_URL = "http://localhost:8000/api"

# 启动开发服务器（带热更新）
npm run dev

# 访问前端：http://localhost:3000
###项目结构
academic-tracker/
├── server/          # FastAPI后端代码
│   ├── crud/         # 数据库操作
│   ├── models/       # 数据模型（Pydantic/SQLAlchemy）
│   ├── routers/      # API路由
│   └── core/         # 配置与安全
├── vue3/         # Vue前端代码
│   ├── src/
│   │   ├── views/    # 页面组件
│   │   └── api/     # 接口封装
│   └── ...
└── docs/             # 项目文档
