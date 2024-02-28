<template >
  <div>
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      :ellipsis="false"
      @select="handleSelect"
    >
      <el-menu-item index="0">
        <img
          style="width: 100px"
          src="/images/element-plus-logo.svg"
          alt="Element logo"
        />
      </el-menu-item>
      <div class="flex-grow" />
      <el-menu-item index="1">Feature</el-menu-item>
      <el-menu-item index="2">ShowCase</el-menu-item>
      <el-menu-item index="3">Learn</el-menu-item>
      <el-menu-item index="4">About</el-menu-item>
      <el-menu-item index="5">Community</el-menu-item>
      <el-menu-item index="6">Login</el-menu-item>
    </el-menu>
    <RouterView />
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";

const activeIndex = ref("1");
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
</script>

<style>
.flex-grow {
  flex-grow: 1;
}

</style>
