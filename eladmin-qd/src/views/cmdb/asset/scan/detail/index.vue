<template>
  <div class="tab-container">
    <el-tabs v-model="activeName" style="margin-top:15px;" type="card">
      <el-tab-pane label="基础信息" name="first">
        <Base ref="form_base" />
      </el-tab-pane>
      <!-- <el-tab-pane label="高级信息" name="second">
      </el-tab-pane>
      <el-tab-pane label="使用说明" name="third">
      </el-tab-pane> -->
    </el-tabs>
  </div>
</template>

<script>
import Base from './form_base'
export default {
  name: 'Tab',
  components: { Base },
  data() {
    return {
      activeName: 'first',
      dialog: false,
      loading: false
    }
  }
}
</script>

<style scoped>
  .tab-container{
    margin: 30px;
  }
</style>
