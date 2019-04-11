<template>
  <div class="container">
    <el-card class="box-card">
      <el-row>
        <el-col :span="12">
          <div class="clearfix">
            <span>项目名称：{{ project_data.name }}</span>
          </div>
        </el-col>
        <el-col :span="9">
          <el-form ref="project" :model="project_data" :rules="rules" size="small" label-width="80px">
            <el-form-item label="服务器" prop="server_ids">
              <el-select v-model="project_data.server_ids" placeholder="请选择服务器" style="width: 230px;">
                <el-option v-for="item in hosts" :key="item.key" :label="item.label" :value="item.key"/>
              </el-select>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="3">
          <el-button :loading="listloading" size="mini" type="primary" icon="el-icon-share" @click="doLoglist">获取列表</el-button>
        </el-col>
      </el-row>
    </el-card>
    <el-card>
      <div class="head-container" style="float: right">
        <div style="font-size:15px" class="filter-item">日志搜索：</div>
        <el-input v-model="search" style="display: inline-block;width: 200px" placeholder="请输入搜索内容" class="filter-item">
        </el-input>
      </div>
      <el-table :data="tables" size="small" border style="width: 100%;">
        <el-table-column label="序号" width="80" align="center">
          <template slot-scope="scope">
            <div>{{ scope.$index + 1 }}</div>
          </template>
        </el-table-column>
        <el-table-column label="日志列表">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="doDown(scope.row)">{{ scope.row }}</el-button>
          </template>
        </el-table-column>
        <el-table-column v-if="checkPermission(['admin','deploy_all','applog_list'])" label="操作" width="250px" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="doDown(scope.row)">下载</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { parseTime } from '@/utils/index'
import { getDeviceList } from '@/api/device'
import { ApplogExcu, ApplogDown } from '@/api/deploy'
import checkPermission from '@/utils/permission'
import { retrieve } from '@/api/project'
export default {
  data() {
    return {
      search: '',
      listloading: false,
      servers: '',
      project_data: {
        server_ids: ''
      },
      list_data: [],
      hosts: [],
      rules: {
        server_ids: [
          { required: true, message: '请选择服务器', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    // 模糊搜索
    tables() {
      const search = this.search
      if (search) {
        return this.list_data.filter(data => {
          return data.includes(search)
        })
      }
      return this.list_data
    }
  },
  created() {
    this.init()
    setTimeout(() => {
      getDeviceList('Linux').then(res => {
        const _servers = this.servers.split(',')
        const _hosts = this.hosts
        const _project_data = this.project_data
        res.forEach(function(data, index) {
          for (const i of _servers) {
            if (i === data.key) {
              _hosts.push(data)
            }
          }
        })
        _project_data.server_ids = _servers[0]
      })
    }, 500)
  },
  methods: {
    parseTime,
    checkPermission,
    init() {
      retrieve(this.$route.query.id).then(res => {
        this.project_data.name = res.name
        this.project_data.server_ids = res.server_ids
        this.project_data.app_log_path = res.app_log_path
        this.servers = res.server_ids
      })
    },
    doLoglist() {
      this.$refs['project'].validate((valid) => {
        if (valid) {
          this.listloading = true
          const form = {
            excu: 'list',
            host: this.project_data.server_ids,
            app_log_path: this.project_data.app_log_path
          }
          ApplogExcu(form).then(res => {
            this.listloading = false
            this.list_data = res.detail
          }).catch(err => {
            this.listloading = false
            console.log(err)
          })
        } else {
          return false
        }
      })
    },
    doDown(file) {
      // ApplogDown(this.project_data.server_ids, file).then(res => {
      //   this.downloading = false
      // }).catch(err => {
      //   this.downloading = false
      //   console.log(err)
      // })
      const form = {
        excu: 'filedown',
        host: this.project_data.server_ids,
        file_path: file
      }
      ApplogDown(form).then(res => {
        const content = res
        const blob = new Blob([content])
        const fileName = file.replace(/\.[^\.]+/, '.tar.gz')
        if ('download' in document.createElement('a')) { // 非IE下载
          const elink = document.createElement('a')
          elink.download = fileName
          elink.style.display = 'none'
          elink.href = URL.createObjectURL(blob)
          document.body.appendChild(elink)
          elink.click()
          URL.revokeObjectURL(elink.href) // 释放URL 对象
          document.body.removeChild(elink)
        } else { // IE10+下载
          navigator.msSaveBlob(blob, fileName)
        }
      }).catch(err => {
        console.log(err)
      })
    }
  }
}
</script>
