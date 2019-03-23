<template>
  <div class="head-container">
    <!-- 搜索 -->
    <el-input v-model="query.value" clearable placeholder="输入主机名/IP/域名搜索" style="width: 200px;" class="filter-item" @keyup.enter.native="toQuery"/>
    <el-select v-model="query.status" clearable placeholder="状态" class="filter-item" style="width: 90px" @change="toQuery">
      <el-option v-for="item in statusOptions" :key="item.key" :label="item.display_name" :value="item.key"/>
    </el-select>
    <el-button class="filter-item" size="mini" type="primary" icon="el-icon-search" @click="toQuery">搜索</el-button>
    <div style="display: inline-block;margin: 0px 2px;">
      <el-button-group v-if="checkPermission(['admin','scan_all'])">
        <el-button class="filter-item" size="mini" type="primary" @click="getPtoggleSelect">全选</el-button>
        <el-button class="filter-item" size="mini" type="danger" @click="deleteSelect">删除</el-button>
        <el-button class="filter-item" size="mini" type="primary" @click="refresh">刷新</el-button>
      </el-button-group>
    </div>
    <div style="display: inline-block;margin: 0px 0px;float: right">
      <!-- 扫描设置 -->
      <el-button-group v-if="checkPermission(['admin','scan_all'])">
        <el-button
          class="filter-item"
          size="mini"
          type="primary"
          icon="el-icon-plus"
          @click="to">扫描设置</el-button>
        <!-- 入库 -->
        <el-button
          :loading="inboundLoading"
          class="filter-item"
          size="mini"
          type="success"
          icon="el-icon-plus"
          @click="excuInbound">全部入库</el-button>
        <!-- 执行扫描 -->
        <el-button
          :loading="scanLoading"
          class="filter-item"
          size="mini"
          type="warning"
          icon="el-icon-plus"
          @click="excuScan">执行扫描</el-button>
      </el-button-group>
      <eForm ref="form" />
    </div>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission' // 权限判断函数
import { getScanSetting, ScanExcu } from '@/api/scan'
import eForm from './setting'
// 查询条件
export default {
  components: { eForm },
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
        { key: 'Succeed', display_name: '成功' },
        { key: 'Failed', display_name: '失败' }
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
  mounted() {
    this.getSettings()
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
    getSettings() {
      this.$nextTick(() => {
        getScanSetting().then(res => {
          this.settings = res.hosts
        })
      })
    },
    excuScan() {
      this.scanLoading = true
      this.$nextTick(() => {
        ScanExcu({ 'excu': 'scan' }).then(res => {
          if (res.code === 200) {
            this.$message({
              showClose: true,
              type: 'success',
              message: res.detail,
              duration: 3000
            })
          } else {
            this.$message({
              showClose: true,
              type: 'error',
              message: res.detail,
              duration: 3000
            })
          }
          this.scanLoading = false
        })
      })
    },
    excuInbound() {
      this.$confirm('是否将扫描成功的设备入库?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.inboundLoading = true
        ScanExcu({ 'excu': 'inbound' }).then(res => {
          if (res.code === 200) {
            this.$message({
              showClose: true,
              type: 'success',
              message: res.detail,
              duration: 3000
            })
          } else {
            this.$message({
              showClose: true,
              type: 'error',
              message: res.detail,
              duration: 3000
            })
          }
          this.inboundLoading = false
          this.$parent.init()
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消操作'
        })
      })
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
