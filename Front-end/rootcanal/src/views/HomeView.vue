<template>
  <div class="main">
    <div style="">Good

    </div>
    <div><n-button ghost>
      Try It Now
    </n-button>
    <n-button ghost>
      Feature
    </n-button></div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';


@Options({

})
export default class HomeView extends Vue {}
</script>

<style scoped>

.main {
  height: calc(100vh - 80px);
  min-height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>