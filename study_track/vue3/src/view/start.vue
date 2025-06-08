<template>
  <div class="login-page">
    <div class="content">
      <h1>STUDY TRACK</h1>
      <p class="subtitle">成绩辅助智能助手，帮你解决学习难题</p>
      <p class="description">
        灵犀一言，以礼相待，智慧沟通，让言语成为桥梁。
      </p>
      <div class="buttons">
        <button class="login-btn" @click="handleLogin">登录</button>
        <button class="trial-btn" @click="handleTrial">注册</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

function handleLogin() {
  router.push('/login');
}

function handleTrial() {
  router.push('/register');
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(to bottom, #f0f4ff, #ffffff);
}

.content {
  text-align: center;
}

h1 {
  font-size: 48px;
  color: #1d2975;
  margin-bottom: 20px;
}

.subtitle {
  font-size: 16px;
  color: #5e7aa5;
  margin-bottom: 10px;
}

.description {
  font-size: 14px;
  color: #3a4c79;
  margin-bottom: 40px;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

button {
  padding: 10px 30px;
  font-size: 18px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}

.login-btn {
  background-color: #1d2975;
  color: white;
}

.trial-btn {
  background-color: white;
  color: #1d2975;
  border: 2px solid #1d2975;
}
</style>
