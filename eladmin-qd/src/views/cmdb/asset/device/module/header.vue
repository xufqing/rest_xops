<template>
  <div class="head-container">
    <!-- 搜索 -->
    <el-input v-model="query.value" clearable placeholder="输入主机名/IP/域名搜索" style="width: 200px;" class="filter-item" @keyup.enter.native="toQuery"/>
    <el-select v-model="query.status" clearable placeholder="状态" class="filter-item" style="width: 90px" @change="toQuery">
      <el-option v-for="item in statusOptions" :key="item.key" :label="item.display_name" :value="item.key"/>
    </el-select>
    <el-button class="filter-item" size="mini" type="primary" icon="el-icon-search" @click="toQuery">搜索</el-button>
    <div style="display: inline-block;margin: 0px 2px;">
      <el-button-group>
        <el-button v-if="checkPermission(['admin','device_all','device_delete'])" class="filter-item" size="mini" type="primary" @click="getPtoggleSelect">全选</el-button>
        <el-button v-if="checkPermission(['admin','device_all','device_delete'])" class="filter-item" size="mini" type="danger" @click="deleteSelect">删除</el-button>
        <el-button class="filter-item" size="mini" type="primary" @click="refresh">刷新</el-button>
      </el-button-group>
    </div>
    <div style="display: inline-block;margin: 0px 0px;float: right">
      <el-button-group v-if="checkPermission(['admin','device_all'])">
        <el-button
          :loading="scanLoading"
          class="filter-item"
          size="mini"
          type="warning"
          icon="el-icon-plus">全部更新</el-button>
      </el-button-group>
    </div>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission' // 权限判断函数
// 查询条件
export default {
  props: {
    query: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      delLoading: false,
      inboundLoading: false,
      scanLoading: false,
      statusOptions: [
        { key: 'online', display_name: '在线' },
        { key: 'offline', display_name: '下线' }
      ],
      settings: {
        net_address: '',
        auth_type: '',
        ssh_username: '',
        ssh_password: '',
        ssh_port: '',
        ssh_private_key: '',
        commands: ''
      },
      status: ''
    }
  },
  methods: {
    checkPermission,
    toQuery() {
      this.$parent.page = 1
      this.$parent.init()
    },
    to() {
      const _this = this.$refs.form
      _this.form = {
        net_address: String(this.settings.net_address),
        auth_type: this.settings.auth_type,
        ssh_username: this.settings.ssh_username,
        ssh_password: this.settings.ssh_password,
        ssh_port: this.settings.ssh_port,
        ssh_private_key: this.settings.ssh_private_key,
        commands: this.settings.commands
      }
      _this.dialog = true
    },
    getPtoggleSelect() {
      this.$parent.toggleSelection(this.$parent.data)
    },
    deleteSelect() {
      if (this.$parent.multipleSelection) {
        const count = this.$parent.multipleSelection.length
        this.$confirm('此操作将删除' + count + '条数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$parent.doSelectionDel()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      } else {
        this.$message({
          type: 'info',
          message: '请先选择数据'
        })
      }
    },
    refresh() {
      this.$parent.init()
    },
    // 数据转换
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'Succeed') {
          return v[j] ? '成功' : '失败'
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>
