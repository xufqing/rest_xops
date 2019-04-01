<template>
  <div class="head-container">
    <!-- 搜索 -->
    <el-input v-model="query.value" clearable placeholder="输入名称搜索" style="width: 200px;" class="filter-item" @keyup.enter.native="toQuery"/>
    <el-button class="filter-item" size="mini" type="primary" icon="el-icon-search" @click="toQuery">搜索</el-button>
    <div style="display: inline-block;margin: 10px 2px;">
      <el-button-group>
        <el-button v-if="checkPermission(['admin','connection_all', 'connection_delete'])" class="filter-item" size="mini" type="primary" @click="getPtoggleSelect">全选</el-button>
        <el-button v-if="checkPermission(['admin','connection_all', 'connection_delete'])" class="filter-item" size="mini" type="danger" @click="deleteSelect">删除</el-button>
        <el-button v-if="checkPermission(['admin','connection_all', 'connection_create'])" class="filter-item" size="mini" type="primary" @click="add">创建</el-button>
      </el-button-group>
      <eForm ref="form" :is-add="true" :service_types="service_types"/>
    </div>
    <!-- 导出 -->
    <el-button v-if="checkPermission(['admin'])" :loading="downloadLoading" size="mini" class="filter-item" type="primary" icon="el-icon-download" style="display: inline-block;margin: 0px 20px;float: right" @click="download">导出</el-button>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission' // 权限判断函数
import eForm from './form'
// 查询条件
export default {
  components: { eForm },
  props: {
    query: {
      type: Object,
      required: true
    },
    service_types: {
      type: Array,
      default: null
    }
  },
  data() {
    return {
      downloadLoading: false
    }
  },
  methods: {
    checkPermission,
    toQuery() {
      this.$parent.page = 1
      this.$parent.init()
    },
    add() {
      this.$refs.form.dialog = true
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
    download() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['ID', 'IP/URL', '认证类型', '用户名', '密码', '端口', '备注']
        const filterVal = ['id', 'hostname', 'auth_type', 'username', 'password', 'port', 'user_name', 'desc', 'is_public']
        const data = this.formatJson(filterVal, this.$parent.data)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        return v[j]
      }))
    }
  }
}
</script>
