<template>
  <el-tabs v-model="active" type="card" @tab-click="handleClick">
    <el-tab-pane label="综合工具" name="tools">
      <keep-alive>
        <Tools/>
      </keep-alive>
    </el-tab-pane>
    <el-tab-pane label="日志列表" name="logs"></el-tab-pane>
  </el-tabs>
</template>
<script>
import Tools from './module/tools'
export default {
  components: { Tools },
  data() {
    return {
      active: 'tools'
    }
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event)
    }
  }
}
</script>
