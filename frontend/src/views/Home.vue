<template>
  <a-layout id="components-layout-demo-top" class="home-container">
    <a-layout-header>
      <!-- <div class="logo" style="background: url(~@/assets/log.svg)"></div> -->
      <a-menu
        theme="dark"
        mode="horizontal"
        :default-selected-keys="[key]"
        :selectedKeys="[key]"
        :style="{ lineHeight: '64px' }"
        @click="menuClick"
      >
        <!-- <a-avatar
          size="large"
          src="~@/assets/logo.png"
          style="margin-right: 20px"
          class="logo"
        /> -->
        <a-menu-item key="introduction"> 系统简介 </a-menu-item>
        <a-menu-item key="new"> 新增检测 </a-menu-item>
        <a-menu-item key="record"> 检测记录 </a-menu-item>
        <!-- <a-menu-item key="user" class="user"> -->
        <a-dropdown style="backgroud: red">
          <span style="float: right">
            <a-avatar
              size="large"
              src="https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png"
            />
            <span style="margin-left: 15px">Winter</span>
          </span>
          <a-menu slot="overlay">
            <a-menu-item>
              <div style="display: flex" @click="logout">
                <a-icon type="logout" style="margin-top: 5px" />
                <li style="margin-left: 5px">logout</li>
              </div>
            </a-menu-item>
          </a-menu>
        </a-dropdown>
        <!-- </a-menu-item> -->
      </a-menu>
    </a-layout-header>
    <a-layout-content style="padding: 0 50px; height: 100%">
      <a-breadcrumb style="margin: 32px 0">
        <!-- <a-breadcrumb-item>Home</a-breadcrumb-item> -->
      </a-breadcrumb>
      <div
        style="
          background: #fff;
          padding: 24px;
          width: 100%;
          display: inline-block;
        "
      >
        <router-view />
      </div>
    </a-layout-content>
    <a-layout-footer style="text-align: center; display: block">
      COVID-19 Detect System ©2021 Created by Winter
    </a-layout-footer>
  </a-layout>
</template>


<script>
import { getCookie, removeCookie } from "../utils/cookie.js";
export default {
  name: "Home",
  methods: {
    menuClick({ key }) {
      console.log(this.$router.currentRoute.path);
      this.key = key;
      if (this.$router.currentRoute.path != "/home/" + key) {
        this.$router.replace({
          path: "/home/" + key,
        });
      }
    },
    logout() {
      console.log(getCookie(getCookie));
      removeCookie("token");
      console.log(getCookie(getCookie));
      this.$router.replace("/Login");
    },
  },
  data() {
    return {
      key: "",
      collapsed: false,
      username: "",
    };
  },
  created() {
    this.key = this.$router.currentRoute.path.split("/")[2];
    let _token = getCookie("token");
    console.log(_token);
    if (_token === undefined || _token == "") {
      console.log("to login");
      this.$router.replace("/Login");
    }
    console.log(this.$route.params.username)
    this.username = this.$route.params.username
  },
  watch: {
    $route(to, from) {
      // this.key = to.path.split('/')[-1]
      this.key = to.path.split("/")[2];
      // console.log(to.path.split('/')[2])
      console.log("from ", from.path, " to ", to.path);
    },
  },
};
</script>
<style>
.home-container {
  height: 100%;
}
#components-layout-demo-top .logo {
  width: 120px;
  height: 31px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px 24px 16px 0;
  float: left;
}

.user {
  float: right;
}
</style>
