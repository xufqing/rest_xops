<template>
  <el-tabs v-model="active" type="card">
    <el-tab-pane label="综合工具" name="tools">
      <keep-alive>
        <Tools/>
      </keep-alive>
    </el-tab-pane>
    <el-tab-pane label="日志列表" name="logs">
      <keep-alive>
        <Applog/>
      </keep-alive>
    </el-tab-pane>
  </el-tabs>
</template>
<script>
import Tools from './module/tools'
import Applog from './module/applog'
export default {
  components: { Tools, Applog },
  data() {
    return {
      active: 'tools'
    }
  }
}
</script>
