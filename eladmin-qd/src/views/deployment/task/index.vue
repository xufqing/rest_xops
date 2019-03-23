<template>
  <div class="app-container">
    <div class="head-container">
      <!-- 搜索 -->
      <el-input v-model="value" clearable placeholder="输入名称搜索" style="width: 200px;" class="filter-item" @keyup.enter.native="toQuery"/>
      <el-button class="filter-item" size="mini" type="primary" icon="el-icon-search" @click="toQuery">搜索</el-button>
      <!-- 新增 -->
      <div style="display: inline-block;margin: 0px 2px;">
        <el-button
          v-if="checkPermission(['admin','project_all','project_create'])"
          class="filter-item"
          size="mini"
          type="primary"
          icon="el-icon-plus"
          @click="toCreate">新增</el-button>
      </div>
    </div>
    <div class="tab-container">
      <el-tabs v-model="activeName" style="margin-top:15px;" type="card" @tab-click="handleClick">
        <el-tab-pane v-for="item in environments" :label="item.value" :key="item.key" :name="item.key">
          <keep-alive>
            <Tables :sup_this="sup_this"/>
          </keep-alive>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import Tables from './module/tables'
import initData from '@/mixins/initData'
import { getKey } from '@/api/dict'
export default {
  components: { Tables },
  mixins: [initData],
  data() {
    return {
      sup_this: this,
      activeName: 'all',
      dialog: false,
      loading: false,
      environments: [],
      value: null
    }
  },
  created() {
    getKey('ENVIRONMENT_TYPE').then(res => {
      this.environments = res[0].ENVIRONMENT_TYPE
    })
    this.$nextTick(() => {
      this.init()
    })
  },
  methods: {
    checkPermission,
    beforeInit() {
      this.url = 'api/projects/'
      const sort = 'id'
      const query = this.query
      const value = query.value
      const active = this.activeName
      if (active === 'all') {
        this.params = { page: this.page, size: this.size, ordering: sort }
      } else {
        this.params = { environment: active, page: this.page, size: this.size, ordering: sort }
      }
      if (value) { this.params['search'] = value }
      return true
    },
    handleClick() {
      this.$nextTick(() => {
        this.init()
      })
    },
    toQuery() {
      this.page = 1
      this.query.value = this.value
      this.init()
    },
    toCreate() {
      this.$router.push({
        path: 'projects/create'
      })
    }
  }
}
</script>

<style scoped>

</style>
