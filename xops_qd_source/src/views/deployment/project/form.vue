<template>
  <div class="formpage">
    <el-form ref="form" :model="form" :rules="rules" label-position="top" size="small">
      <sticky>
        <el-form-item>
          <div style="display: inline-block;margin: 0px 0px;float: right">
            <el-button v-if="checkPermission(['admin','project_all','project_edit']) && button == 'edit' && $route.path === '/deploy/projects/detail'" type="primary" @click="edit">编辑</el-button>
            <el-button v-if="checkPermission(['admin','project_all','project_edit']) && button == 'save' && $route.path === '/deploy/projects/detail'" type="success" @click="doSubmit">保存</el-button>
            <el-button v-if="checkPermission(['admin','project_all','project_edit']) && button == 'save' && $route.path === '/deploy/projects/detail'" type="warning" @click="cancel">取消</el-button>
            <el-button v-if="checkPermission(['admin','project_all','project_edit']) && button == 'edit' && $route.path === '/deploy/projects/detail'" @click="closeTag">返回</el-button>
            <el-button v-if="checkPermission(['admin','project_all','project_create']) && button == 'save' && $route.path === '/deploy/projects/create'" type="success" @click="doSubmit">保存</el-button>
            <el-button v-if="checkPermission(['admin','project_all','project_create']) && button == 'save' && $route.path === '/deploy/projects/create'" @click="closeTag">返回</el-button>
          </div>
        </el-form-item>
      </sticky>
      <p class="warn-content">基础配置</p>
      <el-card class="box-card">
        <el-row>
          <el-col :span="12">
            <el-form-item label="项目名称" prop="name">
              <el-input v-model="form.name" :readonly="is_Readonly" style="width: 300px;" />
            </el-form-item>
            <el-form-item label="项目别名" prop="alias">
              <el-input v-model="form.alias" :readonly="is_Readonly" style="width: 300px;" />
            </el-form-item>
            <el-form-item label="环境" prop="environment">
              <el-select v-model="form.environment" :disabled="is_Readonly" style="width: 300px;" placeholder="请选择认证类型">
                <el-option v-for="item in env_types" :key="item.key" :label="item.value" :value="item.key"/>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Git Repo" prop="repo_url">
              <el-input v-model="form.repo_url" :readonly="is_Readonly" style="width: 300px;"/>
            </el-form-item>
            <el-form-item label="分支/tag" prop="repo_mode">
              <el-select v-model="form.repo_mode" :disabled="is_Readonly" style="width: 300px;" placeholder="请选择认证类型">
                <el-option v-for="item in repo_modes" :key="item.key" :label="item.value" :value="item.key"/>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>
      <p class="warn-content">服务器配置</p>
      <el-card class="box-card">
        <el-form-item>
          <el-transfer
            v-model="serverIds"
            :filter-method="filterMethod"
            :data="transfer_data"
            :titles="transfer_name"
            filterable
            filter-placeholder="请输入IP地址"></el-transfer>
        </el-form-item>
        <el-row>
          <el-col :span="9">
            <el-form-item>
              <span class="x-info">目标服务器部署（WEB）路径<i class="el-icon-info"></i></span>
              <el-input v-model="form.target_root" :readonly="is_Readonly" style="width: 300px;"/>
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item>
              <span class="x-info">目标服务器RELEASE路径（版本仓库）<i class="el-icon-info"></i></span>
              <el-input v-model="form.target_releases" :readonly="is_Readonly" style="width: 300px;"/>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item>
              <span class="x-info">仓库版本保留数<i class="el-icon-info"></i></span>
              <el-input v-model="form.version_num" :readonly="is_Readonly" style="width: 200px;"/>
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>
      <p class="warn-content">任务配置</p>
      <el-card class="box-card">
        <el-row>
          <el-col :span="12">
            <el-form-item>
              <span class="x-info">排除的文件<i class="el-icon-info"></i></span>
              <el-radio v-model="form.is_include" label="false">排除</el-radio>
              <el-radio v-model="form.is_include" label="true">包含</el-radio>
              <codemirror v-model="form.excludes" :options="cmOptions" class="x-code"></codemirror>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item>
              <el-tooltip class="item" effect="dark" placement="top">
                <div slot="content">目标路径：{WEB_ROOT}<br/>代码路径：{CODE_ROOT}<br/>项目别名：{ALIAS}<br/>执行时间：{START_TIME}<br/><span style="color:#ff9955;">其他变量可自定义</span></div>
                <span class="x-info">全局变量<i class="el-icon-info"></i></span>
              </el-tooltip>
              <codemirror v-model="form.task_envs" :options="cmOptions" class="x-code"></codemirror>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item>
              <span class="x-info">Deploy前置任务<i class="el-icon-info"></i></span>
              <codemirror v-model="form.prev_deploy" :options="cmOptions" class="x-code"></codemirror>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item>
              <span class="x-info">Deploy后置任务<i class="el-icon-info"></i></span>
              <codemirror v-model="form.post_deploy" :options="cmOptions" class="x-code"></codemirror>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item>
              <span class="x-info">Release前置任务<i class="el-icon-info"></i></span>
              <codemirror v-model="form.prev_release" :options="cmOptions" class="x-code"></codemirror>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item>
              <span class="x-info">Release后置任务<i class="el-icon-info"></i></span>
              <codemirror v-model="form.post_release" :options="cmOptions" class="x-code"></codemirror>
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>
      <p class="warn-content">工具配置</p>
      <el-card class="box-card">
        <el-row>
          <el-col :span="9">
            <el-form-item>
              <span class="x-info">项目启动脚本路径+文件名<i class="el-icon-info"></i></span>
              <el-input v-model="form.app_start" :readonly="is_Readonly" style="width: 300px;"/>
            </el-form-item>
          </el-col>
          <el-col :span="9">
            <el-form-item>
              <span class="x-info">项目停止脚本路径+文件名<i class="el-icon-info"></i></span>
              <el-input v-model="form.app_stop" :readonly="is_Readonly" style="width: 300px;"/>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item>
              <span class="x-info">项目日志文件路径<i class="el-icon-info"></i></span>
              <el-input v-model="form.app_log_file" :readonly="is_Readonly" style="width: 200px;"/>
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>
    </el-form>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
// codemirror
import { codemirror } from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/monokai.css'
import 'codemirror/addon/hint/show-hint.css'
import 'codemirror/addon/hint/show-hint.js'
import 'codemirror/mode/shell/shell.js'
import Sticky from '@/components/Sticky'
import { getKey } from '@/api/dict'
import { getDeviceList } from '@/api/device'
import { add, edit, retrieve } from '@/api/project'
import { isvalidChinaese } from '@/utils/validate'
var validChinaese = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入项目英文名称'))
  } else if (!isvalidChinaese(value)) {
    callback(new Error('不能输入中文'))
  } else {
    callback()
  }
}
export default {
  components: { codemirror, Sticky },
  data() {
    return {
      is_Readonly: true,
      cmOptions: {
        tabSize: 4,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        mode: 'text/x-sh',
        lineWrapping: true,
        theme: 'monokai',
        readOnly: true
      },
      transfer_name: ['可选服务器', '目标服务器'],
      transfer_data: [],
      loading: false,
      button: 'edit',
      form: {
        name: '',
        environment: '',
        excludes: '',
        is_include: 'false',
        target_root: '',
        target_releases: '',
        task_envs: '',
        prev_deploy: '',
        post_deploy: '',
        prev_release: '',
        post_release: '',
        server_ids: '',
        version_num: 10,
        repo_url: '',
        repo_mode: ''
      },
      serverIds: [],
      env_types: [],
      repo_modes: [],
      rules: {
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ],
        alias: [
          { required: true, trigger: 'blur', validator: validChinaese }
        ],
        environment: [
          { required: true, message: '请选择环境', trigger: 'blur' }
        ],
        repo_mode: [
          { required: true, message: '请选择模式', trigger: 'blur' }
        ],
        repo_url: [
          { required: true, message: '请输入repo url', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    getKey('ENVIRONMENT_TYPE', 'REPO_TYPE').then(res => {
      this.env_types = res[0].ENVIRONMENT_TYPE.filter(t => t.key !== 'all')
      this.repo_modes = res[1].REPO_TYPE
    })
    getDeviceList('Linux').then(res => {
      this.transfer_data = res
    })
    if (this.$route.path === '/deploy/projects/detail') {
      this.$nextTick(() => {
        this.init()
      })
    } else {
      this.button = 'save'
      this.is_Readonly = false
      this.cmOptions.readOnly = false
    }
  },
  methods: {
    checkPermission,
    init() {
      retrieve(this.$route.query.id).then(res => {
        res.is_include = res.is_include.toString()
        this.form = res
        this.serverIds = this.form.server_ids.split(',')
      })
    },
    filterMethod(query, item) {
      return item.label.indexOf(query) > -1
    },
    closeTag() {
      this.$store.dispatch('delView', this.$store.state.tagsView.visitedViews.slice(-1)[0])
      this.$router.go(-1)
    },
    cancel() {
      this.button = 'edit'
      this.is_Readonly = true
      this.cmOptions.readOnly = true
    },
    edit() {
      this.button = 'save'
      this.is_Readonly = false
      this.cmOptions.readOnly = false
    },
    doSubmit() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.loading = true
          this.form.server_ids = this.serverIds.filter(d => d).toString()
          if (this.$route.path === '/deploy/projects/detail') {
            edit(this.form.id, this.form).then(res => {
              this.resetForm()
              this.$message({
                showClose: true,
                type: 'success',
                message: '修改成功!',
                duration: 2500
              })
              this.loading = false
              this.cmOptions.readOnly = true
              this.button = 'edit'
              this.init()
            }).catch(err => {
              this.loading = false
              console.log(err.response.data.detail)
            })
          } else {
            add(this.form).then(res => {
              this.resetForm()
              this.$message({
                showClose: true,
                type: 'success',
                message: '添加成功!',
                duration: 2500
              })
              this.loading = false
              this.closeTag()
            }).catch(err => {
              this.loading = false
              console.log(err.response.data.detail)
            })
          }
        }
      })
    },
    resetForm() {
      this.$refs['form'].resetFields()
      this.form = {
        name: '',
        environment: '',
        excludes: '',
        is_include: 'false',
        target_root: '',
        target_releases: '',
        task_envs: '',
        prev_deploy: '',
        post_deploy: '',
        prev_release: '',
        post_release: '',
        server_ids: '',
        version_num: 10,
        repo_url: '',
        repo_mode: ''
      }
    }
  }
}
</script>

<style scoped>
  .formpage{
    margin: 30px;
  }
  .warn-content{
    padding: 0.5rem;
    font-size: 15px;
  }
  .x-info {
    height: 18px;
    line-height: 18px;
    color: #303133;
    cursor: pointer;
    border-bottom: 1px solid #ebeef5;
    font-size: 14px;
    font-weight: 500;
    -webkit-transition: border-bottom-color .3s;
    transition: border-bottom-color .3s;
    outline: 0;
    margin: 10px;
  }
  .x-div {
    margin-left: 10px;
  }
  .el-transfer {
    margin: 30px;
  }
  .el-transfer >>> .el-transfer-panel{
    border: 1px solid #ebeef5;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    display: inline-block;
    vertical-align: middle;
    width: 350px;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    position: relative;
  }
  .vue-codemirror >>> .CodeMirror {
    border: 1px solid #eee;
    height: 150px;
    width: 400px;
  }
  .x-code {
    padding: 10px;
    line-height: 20px;
  }
</style>

