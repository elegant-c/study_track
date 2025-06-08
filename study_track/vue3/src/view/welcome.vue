<template>
  <div class="dashboard">
    <el-row class="welcome-section">
      <el-col :span="24">
        <h2>欢迎回来，{{ userInfo.name }}！</h2>
        <p>你可以在这里进行学业分析！</p>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="main-content">
      <!-- 左侧个人信息和学习建议 -->
      <el-col :span="6">
        <el-card class="profile-card">
          <div class="profile-header">
            <h3>{{ userInfo.name }}</h3>
            <p>{{ userInfo.school  }}</p>
            <p class="major-info">{{ userInfo.college  }}<br>{{ userInfo.major  }}</p>
          </div>
          
                    <div class="ai-advice-section">
            <h4>study track 功能介绍：</h4>
            <div class="advice-content">
                <p>点击趋势分析，查看AI预测绩点以及趋势分析</p>
                <p>点击成绩管理，查看&添加成绩</p>
                <p>点击学习建议，查看AI学习建议</p>
                <p>点击个人中心，查看&修改个人资料</p>
            </div>
            </div>
        </el-card>
      </el-col>
      
      <!-- 右侧主要内容区域 -->
      <el-col :span="18">
        <el-card class="chart-card">
          <div class="chart-header">
            <div class="header-left">
              <span class="section-title">重点分析</span>
              <span class="chart-title">绩点趋势图</span>
            </div>
            <div class="header-right">
              <el-input
                placeholder="Search"
                prefix-icon="el-icon-search"
                class="search-input"
              ></el-input>
              <el-button type="primary" class="export-btn" @click="exportData">Export data</el-button>
            </div>
          </div>
          
          <div class="time-filter">
            <el-tag class="time-tag active">Last 14 Days</el-tag>
          </div>
          
          <div class="chart-container">
            <line-chart :data="chartData"></line-chart>
          </div>
        </el-card>
        
        <!-- 底部功能按钮 - 两行两列布局 -->
        <div class="action-buttons-grid">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-button class="action-btn" @click="goToTrendAnalysis">趋势分析</el-button>
            </el-col>
            <el-col :span="12">
              <el-button class="action-btn" @click="goToGradeManagement">成绩管理</el-button>
            </el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 15px;">
            <el-col :span="12">
              <el-button class="action-btn" @click="goToLearningAdvice">学习建议</el-button>
            </el-col>
            <el-col :span="12">
              <el-button class="action-btn" @click="goToPersonalCenter">个人中心</el-button>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import LineChart from './LineChart.vue';
import axios from 'axios';

export default {
  components: {
    LineChart
  },
  data() {
    return {
      student_no: '',
      userInfo: {
        name: '',
        username: '',
        school: '',
        college: '',
        major: ''
      },
    };
  },
  async mounted() {
    const userInfo = JSON.parse(sessionStorage.getItem("userInfo"));
    this.student_no = userInfo?.student_no || '';

    if (!this.student_no) {
      console.warn("未从 sessionStorage 获取到 student_no");
      return;
    }

    try {
      const response = await axios.get(`http://127.0.0.1:8000/get_user_info/${this.student_no}`);
      if (response.data) {
        this.userInfo = {
          name: response.data.name || '',
          username: response.data.username || '',
          school: response.data.school || '',
          college: response.data.college || '',
          major: response.data.major || ''
        };
      }
    } catch (error) {
      console.error("获取用户信息失败:", error);
      // Fallback to default values
      this.userInfo = {
        name: '张三',
        school: '清华大学',
        college: '信息科学技术学院',
        major: '计算机科学与技术'
      };
    }
  },
  methods: {
    exportData() {
      console.log('Export data clicked');
    },
    goToTrendAnalysis() {
      this.$router.push('/trend-analysis');
    },
    goToGradeManagement() {
      this.$router.push('/grade-management');
    },
    goToLearningAdvice() {
      this.$router.push('/learning-advice');
    },
    goToPersonalCenter() {
      this.$router.push('/personal-center');
    }
  }
};
</script>


<style scoped>
.dashboard {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.welcome-section {
  margin-bottom: 20px;
}

.welcome-section h2 {
  color: #303133;
  margin-bottom: 5px;
}

.welcome-section p {
  color: #909399;
  font-size: 14px;
}

.main-content {
  margin-top: 20px;
}

.profile-card {
  height: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.profile-header {
  padding: 20px 0;
  text-align: center;
  border-bottom: 1px solid #ebeef5;
}

.profile-header h3 {
  margin-bottom: 5px;
  color: #303133;
}

.profile-header p {
  color: #606266;
  margin-bottom: 5px;
  font-size: 14px;
}

.major-info {
  color: #909399 !important;
  font-size: 13px !important;
  line-height: 1.5;
}

.ai-advice-section {
  padding: 20px;
}

.ai-advice-section h4 {
  color: #303133;
  margin-bottom: 15px;
  font-size: 16px;
}

.advice-content {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}

.advice-content p {
  margin-bottom: 10px;
}

.chart-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
}

.header-left {
  display: flex;
  align-items: center;
}

.section-title {
  font-size: 16px;
  color: #303133;
  font-weight: bold;
  margin-right: 15px;
}

.chart-title {
  font-size: 16px;
  color: #606266;
}

.header-right {
  display: flex;
  align-items: center;
}

.search-input {
  width: 200px;
  margin-right: 15px;
}

.export-btn {
  background-color: #409EFF;
  border-color: #409EFF;
}

.time-filter {
  padding: 10px 20px;
}

.time-tag {
  margin-right: 10px;
  cursor: pointer;
}

.time-tag.active {
  background-color: #409EFF;
  color: white;
}

.chart-container {
  padding: 20px;
  height: 300px;
}

.action-buttons-grid {
  margin-top: 20px;
}

.action-btn {
  width: 100%;
  background-color: white;
  color: #606266;
  border: 1px solid #dcdfe6;
  padding: 12px 0;
}
</style>