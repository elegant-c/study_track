<template>
  <div class="register-page">
    <div class="register-box">
      <h2>注册</h2>
      <form @submit.prevent="register">
        <div class="form-group">
  <input type="text" v-model="form.name" placeholder="姓名" required />
</div>
<div class="form-group">
  <input type="text" v-model="form.student_no" placeholder="学号" required />
</div>
<div class="form-group">
  <input type="text" v-model="form.grade" placeholder="入学年份" required />
</div>
<div class="form-group">
  <input type="email" v-model="form.username" placeholder="邮箱" required />
</div>
<div class="form-group">
  <input type="text" v-model="form.major" placeholder="专业" required />
</div>
<div class="form-group">
  <input type="text" v-model="form.college" placeholder="学院" required />
</div>
<div class="form-group">
  <input type="text" v-model="form.school" placeholder="学校" required />
</div>
<div class="form-group">
  <input type="password" v-model="form.password" placeholder="密码" required />
</div>
<div class="form-group">
  <input type="password" v-model="form.confirm_password" placeholder="确认密码" required />
</div>

        <button type="submit" class="register-button">注册</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";	
	
export default {
  data() {
    return {
      form: {
        name: "",
        student_no: "",
        grade: "",
        username: "",
        major: "",
        college: "",
        school: "",
        password: "",
        confirm_password: ""
      },
      error: ""
    };
  },
  methods: {
    async register() {
      try {
        const res = await axios.post("http://127.0.0.1:8000/register", this.form);
        alert(res.data.message);
      } catch (err) {
        if (err.response && err.response.data.detail) {
          this.error = err.response.data.detail[0].msg || "注册失败";
        }
      }
    }
  },
};
</script>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f8ff;
}

.register-box {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 350px;
  text-align: center;
}

h2 {
  margin-bottom: 20px;
  color: #333333;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

input {
  width: 100%;
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

.register-button {
  width: 100%;
  padding: 10px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

.register-button:hover {
  background-color: #357abd;
}
</style>