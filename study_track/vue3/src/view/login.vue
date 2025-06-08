<template>
  <div class="content">
    <el-card class="login-card">
      <h1>STUDY TRACK</h1>

      <el-form :model="form">
        <el-form-item label="学号">
          <el-input v-model="form.username" placeholder="请输入学号" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-button" @click="onSubmit">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import router from "../router/index";
import { ElMessage } from 'element-plus';

const form = reactive({
  username: "zhifou",
  password: "123456",
});

// 登录
const onSubmit = async () => {
  try {
    // 发送登录请求到后端
    const response = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        student_no: form.username,
        password: form.password
      })
    });

    if (!response.ok) {
      throw new Error('登录失败');
    }

    const data = await response.json();
    
    // 保留原有的菜单逻辑
    let menusOne = [
      {
        id: 69,
        parentId: null,
        name: "用户管理",
        type: 0,
        path: "/user",
        component: "",
        perms: "",
        children: [
          {
            id: 87,
            parentId: 69,
            name: "用户列表",
            type: 1,
            path: "list",
            component: "user/index",
            perms: "",
            children: null,
          },
        ],
      },
      {
        id: 78,
        parentId: null,
        name: "商品管理",
        type: 0,
        path: "/goods",
        component: "",
        perms: "",
        children: [
          {
            id: 78,
            parentId: 79,
            name: "商品列表",
            type: 1,
            path: "list",
            component: "goods/index",
            perms: "",
            children: null,
          },
        ],
      },
      {
        id: 88,
        parentId: null,
        name: "订单管理",
        type: 0,
        path: "/order",
        component: "",
        perms: "",
        children: [
          {
            id: 89,
            parentId: 88,
            name: "订单列表",
            type: 1,
            path: "list",
            component: "order/index",
            perms: "",
            children: null,
          },
        ],
      },
    ];
    
    let menusTwo = [
      {
        id: 69,
        parentId: null,
        name: "用户管理",
        type: 0,
        path: "/user",
        component: "",
        perms: "",
        children: [
          {
            id: 87,
            parentId: 69,
            name: "用户列表",
            type: 1,
            path: "list",
            component: "user/index",
            perms: "",
            children: null,
          },
        ],
      },
    ];

    // 根据用户名设置不同的菜单
    const menuList = form.username === "admin" ? menusOne : menusTwo;
    
    sessionStorage.setItem("menuList", JSON.stringify(menuList));
    sessionStorage.setItem("userInfo", JSON.stringify({ student_no: form.username }));
    
    router.push("/home");
    
  } catch (error) {
    ElMessage.error(error.message || '登录过程中发生错误');
    console.error('Login error:', error);
  }
};
</script>

<style lang="scss" scoped>
.content {
  background: linear-gradient(135deg, #ddffd3, #95d4cd);
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  padding: 30px;
  width: 400px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  background-color: white;
}

.el-form-item {
  margin-bottom: 20px;
}

.login-button, .register-button {
  width: 100%;
  height: 45px;
  border-radius: 5px;
  font-size: 16px;
}

.login-button {
  background-color: #5465E6;
  color: white;
  border: none;
}
</style>