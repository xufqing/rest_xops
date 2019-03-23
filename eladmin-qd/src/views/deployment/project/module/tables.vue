<template>
  <div>
    <!--表格渲染-->
    <el-table v-loading="sup_this.loading" :data="sup_this.data" size="small" border style="width: 100%;">
      <el-table-column prop="name" label="名称"/>
      <el-table-column prop="environment" label="环境" width="200"/>
      <el-table-column label="状态" width="150">
        <template slot-scope="scope">
          <span v-if="scope.row.status == 'Succeed'" style="color:#00CC00">成功</span>
          <span v-else style="color:red">失败</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="350px" align="center">
        <template slot-scope="scope">
          <div style="display: inline-block;margin: 0px 1px;">
            <el-button v-if="checkPermission(['admin','project_all','project_edit'])" :loading="initLoading" size="mini" type="success" @click="toInit(scope.row.id)">检查</el-button>
          </div>
          <el-button v-if="checkPermission(['admin','project_all','project_list'])" size="mini" type="primary" @click="toDetail(scope.row.id)">详情</el-button>
          <el-popover
            v-if="checkPermission(['admin','project_all','project_delete'])"
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
    <el-pagination
      :total="sup_this.total"
      style="margin-top: 8px;"
      layout="total, prev, pager, next, sizes"
      @size-change="sup_this.sizeChange"
      @current-change="sup_this.pageChange"/>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission' // 权限判断函数
import { del } from '@/api/project'
import { DeployExcu } from '@/api/deploy'
import { parseTime } from '@/utils/index'
export default {
  props: {
    sup_this: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      initLoading: false,
      delLoading: false
    }
  },
  methods: {
    parseTime,
    checkPermission,
    // 初始化
    toInit(id) {
      this.initLoading = true
      DeployExcu({
        'excu': 'init',
        'id': id
      }).then(res => {
        this.initLoading = false
        this.$message({
          showClose: true,
          type: 'success',
          message: '初始化成功!',
          duration: 2500
        })
        this.init()
      }).catch(err => {
        this.initLoading = false
        console.log(err)
      })
    },
    // 详情
    toDetail(id) {
      this.$router.push({
        path: 'projects/detail',
        query: { id: id }
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

</style>
