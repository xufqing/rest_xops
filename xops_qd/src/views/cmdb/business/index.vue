<template>
  <div class="app-container">
    <eHeader :query="query"/>
    <el-row :gutter="28">
      <el-col :span="span1">
        <!--表格渲染-->
        <el-table v-loading="loading" ref="tables" :data="data" highlight-current-row size="small" border style="width: 100%;" @current-change="handleCurrentChange">
          <el-table-column label="序号" width="60" align="center">
            <template slot-scope="scope">
              <div>{{ scope.$index + 1 }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="名称"/>
          <el-table-column v-if="table_show" prop="desc" label="描述"/>
          <el-table-column label="操作" align="center">
            <template slot-scope="scope">
              <edit v-if="checkPermission(['admin','business_all','business_edit'])" :data="scope.row" :sup_this="sup_this"/>
              <el-popover
                v-if="checkPermission(['admin','business_all','business_delete'])"
                :ref="scope.row.id"
                placement="top"
                width="180">
                <p>确定删除本条数据吗？</p>
                <div style="text-align: right; margin: 0">
                  <el-button size="mini" type="text" @click="$refs[scope.row.id].doClose()">取消</el-button>
                  <el-button :loading="Loading" type="primary" size="mini" @click="subDelete(scope.row.id)">确定</el-button>
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
      </el-col>
      <el-col :span="12">
        <el-card v-if="show && checkPermission(['admin','business_all','business_edit'])" class="box-card">
          <div slot="header" class="clearfix">
            <span>关联设备-{{ row_data.name }}</span>
            <el-button-group style="float: right; padding: 4px 10px; margin: 0px 2px;">
              <el-button :loading="Loading" class="filter-item" size="mini" type="success" @click="hostSave">保存</el-button>
              <el-button class="filter-item" size="mini" type="info" @click="cancel()">取消</el-button>
            </el-button-group>
          </div>
          <el-transfer
            v-if="show"
            v-model="serverIds"
            :filter-method="filterMethod"
            :data="transfer_data"
            :titles="transfer_name"
            style="height: 330px;"
            filterable
            filter-placeholder="请输入IP地址"></el-transfer>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import initData from '@/mixins/initData'
import { del, save, retrieve } from '@/api/business'
import { parseTime } from '@/utils/index'
import { getDeviceList } from '@/api/device'
import eHeader from './module/header'
import edit from './module/edit'
export default {
  components: { eHeader, edit },
  mixins: [initData],
  data() {
    return {
      row_data: null,
      span1: 24,
      show: false,
      table_show: true,
      transfer_name: ['可关联', '已关联'],
      transfer_data: [],
      serverIds: [],
      Loading: false,
      sup_this: this
    }
  },
  created() {
    this.$nextTick(() => {
      this.init_data()
    })
  },
  methods: {
    parseTime,
    checkPermission,
    init_data() {
      this.init()
      this.getHost()
    },
    handleCurrentChange(val) {
      this.row_data = val
      if (this.row_data) {
        this.serverIds = this.row_data.hosts
      }
      this.span1 = 12
      this.show = true
      this.table_show = false
    },
    beforeInit() {
      this.url = 'api/businesses/'
      const sort = 'id'
      const query = this.query
      const value = query.value
      this.params = { page: this.page, size: this.size, ordering: sort }
      if (value) { this.params['search'] = value }
      return true
    },
    subDelete(id) {
      this.Loading = true
      del(id).then(res => {
        this.Loading = false
        this.$refs[id].doClose()
        this.init()
        this.$message({
          showClose: true,
          type: 'success',
          message: '删除成功!',
          duration: 2500
        })
      }).catch(err => {
        this.Loading = false
        this.$refs[id].doClose()
        console.log(err)
      })
    },
    hostSave(id) {
      this.loading = true
      save(this.row_data.id, { hosts: this.serverIds }).then(res => {
        this.$message({
          showClose: true,
          type: 'success',
          message: '保存成功!',
          duration: 2500
        })
        this.loading = false
        this.update(this.row_data.id)
      }).catch(err => {
        this.loading = false
        console.log(err)
      })
    },
    cancel() {
      this.span1 = 24
      this.show = false
      this.table_show = true
    },
    getHost() {
      getDeviceList('Linux').then(res => {
        const _this = this
        res.forEach(function(data, index) {
          const host = { key: data.id, label: data.ip }
          _this.transfer_data.push(host)
        })
      })
    },
    update(id) {
      // 刷新选中行数据
      retrieve(id).then(res => {
        for (let i = 0; i < this.data.length; i++) {
          if (res.id === this.data[i].id) {
            this.data[i] = res
            break
          }
        }
      })
    },
    filterMethod(query, item) {
      return item.label.indexOf(query) > -1
    }
  }
}
</script>

<style>
  .el-card__header {
    font-size: 14px;
  }
</style>
