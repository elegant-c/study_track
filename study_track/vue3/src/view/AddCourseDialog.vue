<template>
  <div class="dialog-overlay">
    <div class="dialog-content">
      <h2>添加新课程</h2>
      
      <!-- 成功提示 -->
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
      
      <!-- 错误提示 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>课程名称:</label>
          <input v-model="newCourse.course_name" required>
        </div>
        
        <div class="form-group">
          <label>学期:</label>
          <input v-model="newCourse.semester" required>
        </div>
        
        <div class="form-group">
          <label>成绩:</label>
          <input v-model="newCourse.score" type="number" min="0" max="100" required>
        </div>
        
        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="handleClose">
            取消
          </button>
          <button type="submit" class="submit-btn" :disabled="isSubmitting">
            {{ isSubmitting ? '提交中...' : '添加' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AddCourseDialog',
  data() {
    return {
      newCourse: {
        course_name: '',
        semester: '',
        score: 0,
        student_no: ''
      },
      errorMessage: null,
      successMessage: null,
      isSubmitting: false
    }
  },
  async mounted() {
    const userInfo = JSON.parse(sessionStorage.getItem("userInfo"));
    this.newCourse.student_no = userInfo?.student_no || '';

    if (!this.newCourse.student_no) {
      this.errorMessage = "无法识别学生信息，请重新登录";
    }
  },
  methods: {
    async handleSubmit() {
      // 重置消息状态
      this.errorMessage = null;
      this.successMessage = null;
      this.isSubmitting = true;

      try {
        // 确保成绩是数字类型
        const payload = {
          ...this.newCourse,
          score: Number(this.newCourse.score)
        };

        // 发送请求到后端
        const response = await axios.post('http://127.0.0.1:8000/insert_grade', payload);

        // 处理后端响应
        if (response.data.msg === "success") {
          this.successMessage = "课程添加成功！";
          this.resetForm();
          // 3秒后自动关闭对话框
          setTimeout(() => {
            this.$emit('success');
          }, 1500);
        } else if (response.data.detail) {
          this.errorMessage = this.translateError(response.data.detail);
        }
      } catch (error) {
        // 处理网络错误或服务器错误
        if (error.response && error.response.data.detail) {
          this.errorMessage = this.translateError(error.response.data.detail);
        } else {
          this.errorMessage = "请求失败，请检查网络连接后重试";
        }
      } finally {
        this.isSubmitting = false;
      }
    },
    
    resetForm() {
      this.newCourse = { 
        course_name: '', 
        semester: '', 
        score: 0,
        student_no: this.newCourse.student_no // 保留学号
      };
    },
    
    translateError(detail) {
      const errorMap = {
        "Grade already exists for this student, course, and semester": "该课程在本学期已有成绩记录",
        "Course not found": "课程不存在"
      };
      return errorMap[detail] || detail;
    },
    
    handleClose() {
      this.resetForm();
      this.$emit('close');
    }
  }
}
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-content {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
}

h2 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.cancel-btn {
  padding: 8px 16px;
  background-color: #f1f1f1;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn:hover {
  background-color: #ddd;
}

.submit-btn {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #45a049;
}

.submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: #d32f2f;
  background-color: #fde0e0;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
  text-align: center;
}

.success-message {
  color: #388e3c;
  background-color: #ebf5eb;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
  text-align: center;
}
</style>