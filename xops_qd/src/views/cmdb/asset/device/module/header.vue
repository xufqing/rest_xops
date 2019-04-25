<template>
  <div class="head-container">
    <!-- 搜索 -->
    <el-input v-model="query.value" clearable placeholder="输入IP/域名搜索" style="width: 192px;" class="filter-item" @keyup.enter.native="toQuery"/>
    <el-button class="filter-item" size="mini" type="primary" icon="el-icon-search" @click="toQuery">搜索</el-button>
    <div style="display: inline-block;margin: 0px 2px;">
      <el-button-group>
        <el-button v-if="checkPermission(['admin','device_all','device_delete'])" class="filter-item" size="mini" type="primary" @click="getPtoggleSelect">全选</el-button>
        <el-button v-if="checkPermission(['admin','device_all','device_delete'])" class="filter-item" size="mini" type="danger" @click="deleteSelect">删除</el-button>
        <el-button class="filter-item" size="mini" type="primary" @click="refresh">刷新</el-button>
      </el-button-group>
    </div>
    <div style="display: inline-block;margin: 0px 8px;float: right">
      <el-button-group v-if="checkPermission(['admin','device_all'])">
        <el-button
          :loading="updateLoading"
          class="filter-item"
          size="mini"
          type="warning"
          icon="el-icon-plus">全部更新</el-button>
      </el-button-group>
    </div>
    <br>
    <el-select v-model="query.groups" clearable placeholder="设备组" class="filter-item" style="width: 192px" @change="toQuery">
      <el-option v-for="item in group_list" :key="item.id" :label="item.name" :value="item.id"/>
    </el-select>
    <el-select v-model="query.businesses" clearable placeholder="业务类型" class="filter-item" style="width: 192px" @change="toQuery">
      <el-option v-for="item in business_list" :key="item.id" :label="item.name" :value="item.id"/>
    </el-select>
    <el-select v-model="query.labels" clearable placeholder="标签" class="filter-item" style="width: 192px" @change="toQuery">
      <el-option v-for="item in label_list" :key="item.id" :label="item.name" :value="item.id"/>
    </el-select>
    <el-select v-model="query.device_type" clearable placeholder="设备类型" class="filter-item" style="width: 192px" @change="toQuery">
      <el-option v-for="item in device_types" :key="item.key" :label="item.value" :value="item.key"/>
    </el-select>
    <el-select v-model="query.os_type" clearable placeholder="操作系统" class="filter-item" style="width: 192px" @change="toQuery">
      <el-option v-for="item in os_types" :key="item.value" :label="item.label" :value="item.value"/>
    </el-select>
    <el-select v-model="query.status" clearable placeholder="状态" class="filter-item" style="width: 100px" @change="toQuery">
      <el-option v-for="item in status_list" :key="item.value" :label="item.label" :value="item.value"/>
    </el-select>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission' // 权限判断函数
import { getBusinesses } from '@/api/business'
import { getGroups } from '@/api/group'
import { getLabels } from '@/api/label'
import { getKey } from '@/api/dict'
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
      updateLoading: false,
      status_list: [{ value: 'online', label: '在线' }, { value: 'offline', label: '下线' }],
      group_list: [],
      label_list: [],
      business_list: [],
      device_types: [],
      os_types: [{ value: 'Linux', label: 'Linux系统' }, { value: 'Windows', label: 'Windows系统' }, { value: 'Other', label: '其他系统' }]
    }
  },
  created() {
    this.$nextTick(() => {
      this.getAllBusiness()
      this.getAllGroup()
      this.getAllLable()
      this.getAllDeviceType()
    })
  },
  methods: {
    checkPermission,
    toQuery() {
      this.$parent.page = 1
      this.$parent.init()
    },
    to() {
      const _this = this.$refs.form
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
    getAllGroup() {
      if (Array.isArray(this.group_list) && this.group_list.length === 0) {
        getGroups().then(res => {
          this.group_list = res.results
        })
      }
    },
    getAllLable() {
      if (Array.isArray(this.label_list) && this.label_list.length === 0) {
        getLabels().then(res => {
          this.label_list = res.results
        })
      }
    },
    getAllBusiness() {
      if (Array.isArray(this.business_list) && this.business_list.length === 0) {
        getBusinesses().then(res => {
          this.business_list = res.results
        })
      }
    },
    getAllDeviceType() {
      if (Array.isArray(this.business_list) && this.business_list.length === 0) {
        getKey('DEVICE_TYPE').then(res => {
          this.device_types = res[0].DEVICE_TYPE
        })
      }
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
