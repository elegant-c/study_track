<template>
  <div>
    <el-container class="home-container">
      <!-- 菜单 -->
      
      <el-container>
        <el-header>
          <el-dropdown style="float: right; margin: 20px">
            <span class="el-dropdown-link">
              {{ userForm.username }} &nbsp;&nbsp;
              <el-icon class="el-icon--right">
                <arrow-down />
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click.native="toUpdatePassword"
                  >修改密码</el-dropdown-item
                >
                <el-dropdown-item @click.native="logout">退出系统</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-header>

        <el-main>
          <router-view v-slot="{ Component }">
            <transition name="fade-transition" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>

        <el-footer>Copyright © 灵犀一言</el-footer>
      </el-container>
    </el-container>
  </div>
</template>
<script setup>
import { onBeforeMount, onMounted, ref, reactive } from "vue";
import router from "../router/index";
let menuList = JSON.parse(sessionStorage.getItem("menuList"));
let userForm = reactive(JSON.parse(sessionStorage.getItem("userInfo")));
// 挂载 DOM 之前
onBeforeMount(() => {
  // 当前激活的菜单
  activePath.value = sessionStorage.getItem("activePath")
    ? sessionStorage.getItem("activePath")
    : "/index";
});
// 当前激活的路由
let activePath = ref("");
// 保存链接的激活状态
const saveActiveNav = (path) => {
  // 当前激活的菜单
  activePath.value = path;
  sessionStorage.setItem("activePath", path);
};
const logout = () => {
  // 清除缓存
  sessionStorage.clear();
  router.push("/login");
};
</script>

<style scoped lang="scss">
.home-container {
  position: absolute;
  height: 100%;
  top: 0px;
  left: 0px;
  width: 100%;
}

.el-header {
  height: 50px;
  background: #fff;
  overflow: hidden;
  position: relative;
  padding: 0px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}
.el-main {
  padding: 10px;
}
.el-aside {
  width: auto;
}
.el-menu {
  height: 100%;
}
.el-menu-style:not(.el-menu--collapse) {
  width: auto;
  min-height: 400px;
}

.el-footer {
  height: 40px !important;
  line-height: 40px !important;
  color: #bdbaba;
  font-size: 13px;
  text-align: center;
  padding: 0px !important;
}

.toggle-button {
  width: 50px;
  height: 50px;
  vertical-align: middle;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;

  &:hover {
    background: rgba(0, 0, 0, 0.025);
  }
}

.el-menu-item.is-active {
  color: #fff !important;
  font-size: 15px;
  font-weight: bold;
  background-color: #28d094 !important;
  border-radius: 1px;
  text-align: center;
  height: 50px;
  line-height: 50px;
  box-sizing: border-box;
}
.el-menu-item.is-active .el-icon {
  margin-left: -5px !important;
}
.el-dropdown-link {
  cursor: pointer;
  color: black;
  border: none !important;
}
.el-icon-arrow-down {
  font-size: 12px;
  border: none !important;
}
.el-dropdown-link:focus {
  outline: none !important;
}
</style>
