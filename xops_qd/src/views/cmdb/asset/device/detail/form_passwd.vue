<template>
  <div class="app-container">
    <!--表格渲染-->
    <div style="display: inline-block;margin: 10px 10px;float: right">
      <el-button
        v-if="checkPermission(['admin','device_all','device_create'])"
        size="mini"
        type="primary"
        icon="el-icon-plus"
        @click="toAdd">新增</el-button>
      <eForm ref="form" :service_types="service_types"/>
    </div>
    <el-table v-loading="loading" ref="table" :data="data" size="small" border style="width: 100%;">
      <el-table-column label="序号" width="60" align="center">
        <template slot-scope="scope">
          <div>{{ scope.$index + 1 }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="hostname" label="IP/域名" width="150"/>
      <el-table-column prop="auth_type" label="服务类型" width="100"/>
      <el-table-column prop="username" label="用户名" width="100"/>
      <el-table-column prop="password" label="密码/KEY"/>
      <el-table-column prop="port" label="端口" width="80"/>
      <el-table-column prop="desc" label="备注"/>
      <el-table-column label="操作" width="150px" align="center">
        <template slot-scope="scope">
          <el-button v-if="checkPermission(['admin','connection_all','connection_edit'])" size="mini" type="success" @click="toEdit(scope.row.id)">编辑</el-button>
          <el-popover
            v-if="checkPermission(['admin','connection_all','connection_delete'])"
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
import { retrieve, del } from '@/api/connection'
import { getKey } from '@/api/dict'
import eForm from './form'
import initData from '@/mixins/initData'
export default {
  name: 'Passwd',
  components: { eForm },
  filters: {
    authFilter(auth_type) {
      const authMap = {
        password: 'SSH密码',
        draft: 'info',
        mysql: 'MYSQL服务'
      }
      return authMap[auth_type]
    }
  },
  mixins: [initData],
  data() {
    return {
      host: '',
      isadd: true,
      delLoading: false,
      service_types: []
    }
  },
  methods: {
    checkPermission,
    pinit() {
      this.$nextTick(() => {
        this.init(
          getKey('SERVICE_TYPE').then(res => {
            this.service_types = res[0].SERVICE_TYPE
          })
        )
      })
    },
    beforeInit() {
      this.url = 'api/connections/'
      const sort = 'id'
      this.params = { search: this.host, page: this.page, size: this.size, ordering: sort }
      return true
    },
    toAdd() {
      this.$refs.form.is_add = true
      this.$refs.form.form = { hostname: '', auth_type: null, username: '', password: '', port: '', desc: '' }
      this.$refs.form.dialog = true
    },
    toEdit(id) {
      this.$refs.form.is_add = false
      retrieve(id).then(res => {
        this.$refs.form.form.id = res.id
        this.$refs.form.form.hostname = res.hostname
        this.$refs.form.form.auth_type = res.auth_type
        this.$refs.form.form.username = res.username
        this.$refs.form.form.password = res.password
        this.$refs.form.form.port = res.port
        this.$refs.form.form.desc = res.desc
        this.$refs.form.dialog = true
      })
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
    }
  }
}
</script>

<style scoped>
.edit-input {
  padding-right: 100px;
}
.cancel-btn {
  position: absolute;
  right: 15px;
  top: 10px;
}
.app-container{
  margin: -30px 0px;
}
</style>
