<template>
  <div>
    <router-view> </router-view>
  </div>
</template>
<script setup>
import { onMounted } from "vue";
import { initRouter } from "./utils/permission";
import router from "./router";
// 解决刷新页面，页面空白的问题
onMounted(async () => {
  await initRouter();
  // 获取路由 path 地址，并跳转
  router.replace(router.options.history.location);
});
</script>
