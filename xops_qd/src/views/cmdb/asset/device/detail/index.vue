<template>
  <div class="tab-container">
    <el-tabs v-model="activeName" style="margin-top:15px;" type="card" @tab-click="handleClick">
      <el-tab-pane label="设备信息" name="1">
        <Base ref="form_base"/>
      </el-tab-pane>
      <el-tab-pane label="硬件信息" name="2">
      </el-tab-pane>
      <el-tab-pane label="软件信息" name="3">
      </el-tab-pane>
      <el-tab-pane label="变更记录" name="4">
      </el-tab-pane>
      <el-tab-pane label="附加信息" name="5">
      </el-tab-pane>
      <el-tab-pane v-if="checkPermission(['admin'])" label="密码信息" name="6">
        <Passwd ref="form_passwd"/>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import Base from './form_base'
import Passwd from './form_passwd'
export default {
  name: 'Tab',
  components: { Base, Passwd },
  data() {
    return {
      activeName: '1',
      dialog: false,
      loading: false
    }
  },
  methods: {
    checkPermission,
    handleClick() {
      if (this.activeName === '6') {
        this.$refs['form_passwd'].host = this.$refs['form_base'].form_base.hostname
        this.$refs['form_passwd'].pinit()
      }
    }
  }
}
</script>

<style scoped>
  .tab-container{
    margin: 30px;
  }
</style>
