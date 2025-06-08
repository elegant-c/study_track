import router from "../router";
const filterRouter = () => {
  // 从sessionStorage 获取用户的菜单数据
  const menuList = JSON.parse(sessionStorage.getItem("menuList")) || [];
  // import.meta.glob 作用是 Vite 特有的功能,它允许你在模块内部匹配多个模块,基于文件系统的模式
  const modules = import.meta.glob("../view/**/*.vue");
  // 遍历菜单数据
  for (let index = 0; index < menuList.length; index++) {
    // 获取父菜单
    const e = menuList[index];
    // 因为我们在 home 页面的 el-main 设置了 router-view ，所以这里父级菜单默认指向 home页面
    e.component = modules["../view/home.vue"];
    // 遍历子菜单，
    for (let index = 0; index < e.children.length; index++) {
      const item = e.children[index];
      // 导入组件
      item.component = modules[`../view/${item.component}.vue`];
    }
  }
  return menuList;
};
export const initRouter = async () => {
  const menus = await filterRouter();
  menus.forEach((route) => {
    router.addRoute(route);
  });
};
