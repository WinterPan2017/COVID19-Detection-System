<template>
  <div id="App">
    <router-view></router-view>
  </div>
</template>


<script>
export default {
  name: "App",
  data() {
    return {
      message: "123",
      collapsed: false,
    };
  },
};
</script>



