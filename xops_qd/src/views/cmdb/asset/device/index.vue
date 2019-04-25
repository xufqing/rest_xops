<template>
  <div class="app-container">
    <eHeader :query="query"/>
    <!--表格渲染-->
    <el-table v-loading="loading" ref="table" :data="data" size="small" border style="width: 100%;" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center">
      </el-table-column>
      <el-table-column label="序号" width="60" align="center">
        <template slot-scope="scope">
          <div>{{ scope.$index + 1 }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="hostname" label="IP/域名" width="120"/>
      <el-table-column label="业务类型" width="120">
        <template slot-scope="scope">
          <el-tag v-for="item in scope.row.businesses" :key="item.id" size="small" style="display: inline-block;margin: 0px 2px;">{{ item.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="设备标签">
        <template slot-scope="scope">
          <el-tag v-for="item in scope.row.labels" :key="item.id" size="small" style="display: inline-block;margin: 0px 2px;">{{ item.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="os_version" label="系统版本"/>
      <el-table-column label="状态" width="100">
        <template slot-scope="scope">
          <span v-if="scope.row.status == 'online'" style="color:#00CC00">在线</span>
          <span v-else style="color:red">下线</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150px" align="center">
        <template slot-scope="scope">
          <el-button v-if="checkPermission(['admin','device_all','device_list'])" size="mini" type="primary" @click="toDetail(scope.row.id)">详情</el-button>
          <el-popover
            v-if="checkPermission(['admin','device_all','device_delete'])"
            :ref="scope.row.id"
            placement="top"
            width="180">
            <p>确定删除本条数据吗？</p>
            <div style="text-align: right; margin: 0">
              <el-button size="mini" type="text" @click="$refs[scope.row.id].doClose()">取消</el-button>
              <el-button :loading="delLoading" type="primary" size="mini" @click="subDelete(scope.row.id)">确定</el-button>
            </div>
            <el-button slot="reference" type="danger" size="mini">删除</el-button>
          </el-popover>
        </template>
      </el-table-column>
    </el-table>
    <!--分页组件-->
    <el-pagination
      :total="total"
      style="margin-top: 8px;"
      layout="total, prev, pager, next, sizes"
      @size-change="sizeChange"
      @current-change="pageChange"/>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import initData from '@/mixins/initData'
import { del } from '@/api/device'
import { parseTime } from '@/utils/index'
import eHeader from './module/header'
export default {
  components: { eHeader },
  mixins: [initData],
  data() {
    return {
      delLoading: false, sup_this: this, allSelect: false
    }
  },
  created() {
    this.$nextTick(() => {
      this.init()
    })
  },
  methods: {
    parseTime,
    checkPermission,
    beforeInit() {
      this.url = 'api/devices/'
      const sort = 'id'
      const query = this.query
      const value = query.value
      const status = query.status
      const groups = query.groups
      const labels = query.labels
      const businesses = query.businesses
      const device_type = query.device_type
      const os_type = query.os_type
      this.params = { page: this.page, size: this.size, ordering: sort }
      if (status !== '' && status !== null) { this.params['status'] = status }
      if (groups !== '' && groups !== null) { this.params['groups'] = groups }
      if (labels !== '' && labels !== null) { this.params['labels'] = labels }
      if (businesses !== '' && businesses !== null) { this.params['businesses'] = businesses }
      if (os_type !== '' && os_type !== null) { this.params['os_type'] = os_type }
      if (device_type !== '' && device_type !== null) { this.params['device_type'] = device_type }
      if (value) { this.params['search'] = value }
      return true
    },
    subDelete(id) {
      this.delLoading = true
      del(id).then(res => {
        this.delLoading = false
        this.$refs[id].doClose()
        this.init()
        this.$message({
          showClose: true,
          type: 'success',
          message: '删除成功!',
          duration: 2500
        })
      }).catch(err => {
        this.delLoading = false
        this.$refs[id].doClose()
        console.log(err)
      })
    },
    // 全选
    toggleSelection(rows) {
      if (rows) {
        rows.forEach(row => {
          this.$refs.table.toggleRowSelection(row, !this.allSelect)
        })
        this.allSelect = !this.allSelect
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    // 批量删除
    doSelectionDel() {
      const resultArr = []
      this.multipleSelection.forEach(function(data, index) {
        const result = del(data.id).catch(err => {
          console.log(err)
        })
        resultArr.push(result)
      })
      Promise.all(resultArr).then((resultArr) => {
        this.init()
      })
    },
    // 详情
    toDetail(id) {
      this.$router.push({
        path: 'devices/detail',
        query: { id: id }
      })
    },
    handleNodeClick(data) {
      console.log(data)
    }
  }
}
</script>

<style scoped>

</style>
