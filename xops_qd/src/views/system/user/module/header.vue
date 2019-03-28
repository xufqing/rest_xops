<template>
  <div class="head-container">
    <!-- 搜索 -->
    <el-input v-model="query.value" clearable placeholder="输入关键字搜索" style="width: 200px;" class="filter-item" @keyup.enter.native="toQuery"/>
    <el-select v-model="query.is_active" clearable placeholder="状态" class="filter-item" style="width: 90px" @change="toQuery">
      <el-option v-for="item in enabledTypeOptions" :key="item.key" :label="item.display_name" :value="item.key"/>
    </el-select>
    <el-button class="filter-item" size="mini" type="primary" icon="el-icon-search" @click="toQuery">搜索</el-button>
    <!-- 新增 -->
    <div style="display: inline-block;margin: 0px 2px;">
      <el-button
        v-if="checkPermission(['admin','user_all','user_create'])"
        class="filter-item"
        size="mini"
        type="primary"
        icon="el-icon-plus"
        @click="$refs.form.dialog = true; getOrgUserTree()">新增</el-button>
      <eForm ref="form" :roles="roles" :organizations="organizations" :orgusers="orgusers" :is-add="true"/>
    </div>
    <!-- 导出 -->
    <el-button
      v-if="checkPermission(['admin','user_all'])"
      :loading="downloadLoading"
      size="mini"
      class="filter-item"
      type="primary"
      icon="el-icon-download"
      @click="download">导出</el-button>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission' // 权限判断函数
import { getOrganizationUserTree } from '@/api/organization'
import eForm from './form'
// 查询条件
export default {
  components: { eForm },
  props: {
    organizations: {
      type: Array,
      required: true
    },
    roles: {
      type: Array,
      required: true
    },
    query: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      orgusers: [],
      downloadLoading: false,
      enabledTypeOptions: [
        { key: 'true', display_name: '激活' },
        { key: 'false', display_name: '锁定' }
      ]
    }
  },
  methods: {
    checkPermission,
    // 去查询
    toQuery() {
      this.$parent.page = 1
      this.$parent.init()
    },
    // 导出
    getOrgUserTree() {
      getOrganizationUserTree().then(res => {
        this.orgusers = res.detail
      })
    },
    download() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['ID', '用户名', '邮箱', '头像地址', '状态', '注册日期', '最后修改密码日期']
        const filterVal = ['id', 'username', 'email', 'avatar', 'is_active', 'createTime', 'lastPasswordResetTime']
        const data = this.formatJson(filterVal, this.$parent.data)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    // 数据转换
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'is_active') {
          return v[j] ? '启用' : '禁用'
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>
