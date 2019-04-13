<template>
  <div class="page">
    <el-row :gutter="32">
      <el-col :span="9">
        <el-card class="box-card">
          <el-form ref="form" :model="form" :rules="rules" size="small" label-width="80px">
            <el-form-item label="项目名称" prop="name">
              <el-input v-model="form.name" :readonly="true" style="width: 230px;"/>
            </el-form-item>
            <el-form-item label="项目别名" prop="alias">
              <el-input v-model="form.alias" :readonly="true" style="width: 230px;"/>
            </el-form-item>
            <el-form-item label="部署环境" prop="environment">
              <el-input v-model="form.environment" :readonly="true" style="width: 230px;"/>
            </el-form-item>
            <el-form-item label="选择版本" prop="version">
              <el-select :loading="changeFlag" v-model="form.version" style="width: 230px;" placeholder="请选择版本" @visible-change="getVersion($event, $route.query.id)">
                <el-option v-for="item in vers" :key="item.id" :label="item.value" :value="item.value"/>
              </el-select>
            </el-form-item>
            <el-form-item label="服务器" prop="server_ids">
              <el-radio v-model="host_radio" label="true">全量</el-radio>
              <el-radio v-model="host_radio" label="false">自定义</el-radio>
              <el-select v-if="host_radio != 'true'" v-model="form.server_ids" multiple style="width: 230px;" placeholder="请选择">
                <el-option v-for="item in hosts" :key="item.key" :label="item.label" :value="item.key"/>
              </el-select>
            </el-form-item>
            <el-form-item>
              <div style="display: inline-block;margin: 0px 0px;">
                <el-button v-if="checkPermission(['admin','deploy_all','deploy_excu'])" :loading="formloading" type="primary" @click="doSubmit">提交</el-button>
                <el-button v-if="checkPermission(['admin','deploy_all','deploy_excu'])" @click="closeTag">返回</el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="15">
        <el-card>
          <el-table :data="data" height="226">
            <el-table-column prop="id" label="ID" width="70" align="center"/>
            <el-table-column label="历史记录">
              <template slot-scope="scope">
                <el-button type="text" size="small" @click="toDetail(scope.row.alias,scope.row.name)">{{ scope.row.name }}</el-button>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template slot-scope="scope">
                <span v-if="scope.row.status == 'Succeed'" style="color:#00CC00">成功</span>
                <span v-else style="color:red">失败</span>
              </template>
            </el-table-column>
            <el-table-column v-if="checkPermission(['admin','deploy_all','deploy_excu'])" label="操作" width="150px" align="center">
              <template slot-scope="scope">
                <el-button v-if="scope.row.is_rollback && scope.row.status == 'Succeed' " :loading="rollbackloading" size="mini" type="primary" @click="toRollback(scope.row.id,scope.row.project_id,scope.row.alias)">回滚</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            :total="total"
            background
            layout="prev, pager, next"
            @size-change="sizeChange"
            @current-change="pageChange"/>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-card>
        <div slot="header" class="clearfix">
          <span>项目统计</span>
        </div>
      </el-card>
    </el-row>
  </div>
</template>

<script>
import { DeployExcu, getVers } from '@/api/deploy'
import initData from '@/mixins/initData'
import { retrieve } from '@/api/project'
import { getDeviceList } from '@/api/device'
import checkPermission from '@/utils/permission'
import { parseTime } from '@/utils/index'
export default {
  mixins: [initData],
  data() {
    return {
      formloading: false,
      rollbackloading: false,
      changeFlag: false,
      vers: null,
      host_radio: 'true',
      hosts: [],
      records: [],
      form: {
        name: '',
        alias: '',
        environment: '',
        version: '',
        server_ids: ''
      },
      rules: {
        version: [
          { required: true, message: '请选择版本', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    getDeviceList('Linux').then(res => {
      this.hosts = res
    })
    this.$nextTick(() => {
      this.publishInit()
      this.init()
    })
  },
  methods: {
    parseTime,
    checkPermission,
    beforeInit() {
      this.url = 'api/deploy/records/?project_id=' + this.$route.query.id
      const sort = '-id'
      this.params = { page: this.page, size: this.size, ordering: sort }
      return true
    },
    publishInit() {
      retrieve(this.$route.query.id).then(res => {
        this.form.id = res.id
        this.form.name = res.name
        this.form.alias = res.alias
        this.form.environment = res.environment
        this.form.server_ids = res.server_ids
        this.form.server_ids = this.form.server_ids.split(',')
      })
    },
    cancel() {
      this.resetForm()
    },
    doSubmit() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.formloading = true
          this.form.excu = 'deploy'
          DeployExcu(this.form).then(res => {
            // this.resetForm()
            this.formloading = false
            this.$router.push({
              path: '/deploy/tasks/console',
              query: { id: this.$route.query.id, alias: this.form.alias, record: res.detail, scenario: 0 }
            })
          }).catch(err => {
            this.formloading = false
            console.log(err)
          })
        } else {
          return false
        }
      })
    },
    resetForm() {
      this.dialog = false
      this.$refs['form'].resetFields()
      this.form = {
        name: '',
        alias: '',
        environment: '',
        version: '',
        server_ids: ''
      }
    },
    toRollback(id, project_id, alias) {
      this.$confirm('是否回滚到上一个版本?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.rollbackloading = true
        const data = {
          excu: 'rollback',
          id: id,
          project_id: project_id,
          alias: alias
        }
        DeployExcu(data).then(res => {
          this.rollbackloading = false
          this.$router.push({
            path: '/deploy/tasks/console',
            query: { id: this.$route.query.id, alias: alias, record: res.detail, scenario: 1 }
          })
        }).catch(err => {
          console.log(err)
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消操作'
        })
      })
    },
    toDetail(alias, record_id) {
      const reg = new RegExp(alias + '_(.*\\d)', '')
      record_id = record_id.match(reg)
      this.$router.push({
        path: '/deploy/tasks/console',
        query: { id: this.$route.query.id, alias: alias, record: record_id[0], scenario: 1 }
      })
    },
    closeTag() {
      this.$store.dispatch('delView', this.$store.state.tagsView.visitedViews.slice(-1)[0])
      this.$router.go(-1)
    },
    getVersion: function(callback, id) {
      if (callback) {
        if (this.vers === null) {
          this.changeFlag = true
          getVers(id).then(res => {
            const _this = this
            _this.vers = []
            res.detail.forEach(function(data, index) {
              _this.vers.push({
                id: index,
                value: data
              })
            })
            this.changeFlag = false
          })
        }
      }
    }
  }
}
</script>

<style scoped>
.page {
  margin: 30px;
}
.box-card >>> .el-form-item__label {
  line-height: 32px;
}
.box-card >>> .el-form-item__content {
  line-height: 32px;
}
.el-table >>> th.is-leaf {
  padding: 5px 0;
}
.el-table--enable-row-transition >>> .el-table__body td {
  padding: 8px 0;
}
.el-pagination {
    padding: 25px 5px;
}
</style>
