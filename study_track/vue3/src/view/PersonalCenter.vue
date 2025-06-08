<template>
  <div class="personal-center">
    <el-card class="profile-card">
      <div class="header">
        <h1>个人中心</h1>
      </div>
      
      <div class="section">
        <h2>我的账户</h2>
        <el-divider></el-divider>
        
        <div class="info-item">
          <span class="label">用户名</span>
          <span v-if="!isEditing">{{ userInfo.name }}</span>
          <el-input v-else v-model="userInfo.name" />
        </div>
        
        <div class="info-item">
          <span class="label">账户名</span>
          <span class="value">{{ userInfo.username }}</span>
        </div>
        
        <div class="info-item">
          <span class="label">学校</span>
          <span class="value">{{ userInfo.school }}</span>
        </div>
        
        <div class="info-item">
          <span class="label">学院</span>
          <span class="value">{{ userInfo.college }}</span>
        </div>
        
        <div class="info-item">
          <span class="label">专业</span>
          <span class="value">{{ userInfo.major }}</span>
        </div>
      </div>
      
      <el-divider></el-divider>
      
      <div class="actions">
        <el-button 
          type="primary" 
          class="action-btn" 
          @click="isEditing ? cancelEdit() : handleEdit()"
        >
          {{ isEditing ? '取消' : '编辑' }}
        </el-button>
        <el-button 
          v-if="isEditing" 
          type="success" 
          class="action-btn" 
          @click="updateUserInfo"
        >
          保存
        </el-button>
        <el-button 
          type="primary" 
          class="action-btn" 
          @click="handleChangePassword"
        >
          修改密码
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus';
import axios from 'axios';

export default {
  name: 'PersonalCenter',
  data() {
    return {
      student_no: '',
      isEditing: false,
      originalUserInfo: {}, // 用来保存未修改前的用户信息，取消编辑时恢复
      userInfo: {
        name: '',
        username: '',
        school: '',
        college: '',
        major: ''
      }
    };
  },
  methods: {
    async fetchUserInfo() {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/get_user_info/${this.student_no}`);
        this.userInfo = {
          name: res.data.name || '无',
          username: res.data.username || '无',
          school: res.data.school || '无',
          college: res.data.college || '无',
          major: res.data.major || '无'
        };
        this.originalUserInfo = { ...this.userInfo }; // 备份一份原始数据
      } catch (err) {
        ElMessage.error('加载用户信息失败');
      }
    },
    async updateUserInfo() {
      try {
        await axios.put(`http://127.0.0.1:8000/update_user_info/${this.student_no}`, this.userInfo);
        ElMessage.success('更新成功');
        this.isEditing = false;
        this.originalUserInfo = { ...this.userInfo }; // 更新备份
      } catch (err) {
        ElMessage.error('更新失败');
      }
    },
    handleEdit() {
      this.isEditing = true;
    },
    cancelEdit() {
      this.userInfo = { ...this.originalUserInfo }; // 恢复数据
      this.isEditing = false;
    },
    handleChangePassword() {
      ElMessage.info('修改密码功能即将开放');
    }
  },
  async mounted() {
    const userInfo = JSON.parse(sessionStorage.getItem("userInfo"));
    this.student_no = userInfo?.student_no || '';

    if (!this.student_no) {
      console.warn("未从 sessionStorage 获取到 student_no");
      ElMessage.warning('无法获取用户信息，请重新登录');
      return;
    }
    
    await this.fetchUserInfo();
  }
};
</script>

<style scoped>
.personal-center {
  padding: 20px;
  max-width: 400px;
  margin: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.profile-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: 100%;
}

.header h1 {
  color: #303133;
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
}

.section h2 {
  color: #303133;
  font-size: 18px;
  margin-bottom: 10px;
}

.info-item {
  display: flex;
  margin-bottom: 16px;
  padding: 0 10px;
}

.label {
  width: 120px;
  color: #909399;
  font-size: 14px;
}

.value {
  flex: 1;
  color: #606266;
  font-size: 14px;
}

.el-divider {
  margin: 20px 0;
}

.actions {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 10px;
  gap: 20px;
}

.action-btn {
  width: 100px;
}
</style>
