<template>
  <div class="learning-advice-container">
    <h1>学习建议</h1>
    
    <div class="ai-advice">
      <h2>AI建议：</h2>
      <p>{{ adviceText }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'LearningAdvice',
  data() {
    return {
      student_no: "",
      adviceText: "加载中..."
    };
  },
  async mounted() {
    const userInfo = JSON.parse(sessionStorage.getItem("userInfo"));
    this.student_no = userInfo?.student_no || '';

    if (!this.student_no) {
      console.warn("未从 sessionStorage 获取到 student_no");
      this.adviceText = "无法获取学生信息，请先登录";
      return;
    }

    await this.fetchAdvice(); // 注意方法名也要对应修改
  },
  methods: {
    async fetchAdvice() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/ask_llm", {
          student_no: this.student_no
        });
        this.adviceText = response.data.advice; // 修正为正确的字段名
      } catch (error) {
        this.adviceText = "获取学习建议失败: " + error.message;
        console.error("API请求错误:", error);
      }
    }
  }
};
</script>

<style scoped>
.learning-advice-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  color: #333;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

.ai-advice {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #2c3e50;
  margin-bottom: 15px;
}

p {
  line-height: 1.6;
  font-size: 16px;
}
</style>