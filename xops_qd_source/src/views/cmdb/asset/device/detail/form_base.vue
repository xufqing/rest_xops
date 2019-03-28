<template>
  <div>
    <p class="warn-content">基础信息</p>
    <el-form ref="form" :model="form_base" :rules="rules" size="small" label-width="80px">
      <el-row>
        <el-col :span="12">
          <el-form-item label="主机名">
            <el-input v-model="form_base.sys_hostname" :readonly="is_Readonly" style="width: 300px;" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="IP/域名" prop="hostname">
            <el-input v-model="form_base.hostname" :readonly="is_Readonly" style="width: 300px;"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="认证类型">
            <el-select v-model="form_base.auth_type" :disabled="is_Readonly" style="width: 300px;" placeholder="请选择认证类型">
              <el-option v-for="item in types" :key="item.value" :label="item.label" :value="item.value"/>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="系统类型">
            <el-select v-model="form_base.os_type" :disabled="is_Readonly" style="width: 300px;" placeholder="请选择认证类型">
              <el-option v-for="item in os_types" :key="item.value" :label="item.label" :value="item.value"/>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="SN编号">
            <el-input v-model="form_base.sn_number" :readonly="is_Readonly" style="width: 300px;"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="系统版本">
            <el-input v-model="form_base.os_version" :readonly="is_Readonly" style="width: 300px;"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="设备类型">
            <el-select v-model="form_base.device_type" :disabled="is_Readonly" style="width: 300px;" placeholder="请选择设备类型">
              <el-option v-for="item in device_types" :key="item.key" :label="item.value" :value="item.key"/>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="MAC地址">
            <el-input v-model="form_base.mac_address" :readonly="is_Readonly" style="width: 300px;"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-form-item label="关联业务">
          <treeselect v-model="businessIds" :multiple="true" :options="businesstree" :disable-branch-nodes="true" style="width: 300px;" placeholder="请选择业务" />
        </el-form-item>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="入库时间">
            <span style="margin-left: 10px;">{{ form_base.add_time }}</span>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="变更时间">
            <span style="margin-left: 10px;">{{ form_base.modify_time }}</span>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-form-item v-if="form_base.error_message" label="错误信息">
          <el-input v-model="form_base.error_message" :readonly="is_Readonly" style="width: 720px;" type="textarea"/>
        </el-form-item>
      </el-row>
      <el-form-item>
        <div style="display: inline-block;margin: 20px 0px;float: left">
          <el-button v-if="checkPermission(['admin','asset_all','asset_edit']) && button == 'edit'" type="primary" @click="edit">编辑</el-button>
          <el-button v-if="checkPermission(['admin','asset_all','asset_edit']) && button == 'save'" type="success" @click="doSubmit">保存</el-button>
          <el-button v-if="checkPermission(['admin','asset_all','asset_edit']) && button == 'save'" type="warning" @click="cancel">取消</el-button>
          <el-button v-if="checkPermission(['admin','asset_all','asset_edit']) && button == 'edit'" @click="closeTag">返回</el-button>
        </div>
      </el-form-item>
    </el-form>
    <p class="warn-content">配置信息</p>
    <el-row>
      <el-col :span="12">
        <label class="el-form-item__label" style="width: 80px;">CPU</label>
        <div class="el-form-item__content" style="margin-left: 80px;">
          <span style="margin-left: 10px;">intelAAACPU</span>
        </div>
      </el-col>
      <el-col :span="12">
        <label class="el-form-item__label" style="width: 80px;">CPU核数</label>
        <div class="el-form-item__content" style="margin-left: 80px;">
          <span style="margin-left: 10px;">12核</span>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import Treeselect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
import { getKey } from '@/api/dict'
import { retrieve, edit } from '@/api/device'
import { getBusinessTree } from '@/api/business'
import { parseTime } from '@/utils/index'
export default {
  name: 'Base',
  components: { Treeselect },
  data() {
    return {
      loading: false,
      button: 'edit',
      form_base: {
        id: '',
        add_time: '',
        modify_time: '',
        hostname: '',
        auth_type: '',
        status: '',
        sys_hostname: '',
        mac_address: '',
        sn_number: '',
        os_version: '',
        os_type: '',
        device_type: '',
        businesses: [],
        error_message: ''
      },
      businesstree: [],
      businessIds: [],
      is_Readonly: true,
      types: [{ value: 'password', label: '密码认证' }, { value: 'key_filename', label: '密钥认证' }],
      os_types: [{ value: 'Linux', label: 'Linux系统' }, { value: 'Other', label: '其他系统' }],
      device_types: [{ key: 'VM', value: '虚拟机' }, { key: 'key', value: '物理机' }],
      rules: {
        hostname: [
          { required: true, message: '请输入主机地址', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.$nextTick(() => {
      this.init()
    })
  },
  methods: {
    checkPermission,
    init() {
      retrieve(this.$route.query.id).then(res => {
        this.form_base = res
        this.form_base.add_time = parseTime(this.form_base.add_time)
        this.form_base.modify_time = parseTime(this.form_base.modify_time)
        this.businessIds = this.form_base.businesses
      })
      getKey('DEVICE_TYPE').then(res => {
        this.device_types = res[0].DEVICE_TYPE
      })
      this.getBusinesses()
    },
    closeTag() {
      this.$store.dispatch('delView', this.$store.state.tagsView.visitedViews.slice(-1)[0])
      this.$router.go(-1)
    },
    cancel() {
      this.button = 'edit'
      this.is_Readonly = true
    },
    edit() {
      this.button = 'save'
      this.is_Readonly = false
    },
    doSubmit() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.form_base.businesses = []
          const _this = this
          this.businessIds.forEach(function(data, index) {
            _this.form_base.businesses.push(data)
          })
          this.loading = true
          edit(this.form_base.id, this.form_base).then(res => {
            this.resetForm()
            this.$message({
              showClose: true,
              type: 'success',
              message: '修改成功!',
              duration: 2500
            })
            this.loading = false
            this.button = 'edit'
            this.init()
          }).catch(err => {
            this.loading = false
            console.log(err.response.data.detail)
          })
        }
      })
    },
    resetForm() {
      // this.$refs['form_base'].resetFields()
      this.form_base = {
        id: '',
        add_time: '',
        modify_time: '',
        hostname: '',
        port: '',
        username: '',
        password: '',
        key_filename: '',
        auth_type: '',
        status: '',
        sys_hostname: '',
        mac_address: '',
        sn_number: '',
        os_version: '',
        os_type: '',
        device_type: '',
        businesses: [],
        error_message: ''
      }
      this.businessIds = []
    },
    getBusinesses() {
      getBusinessTree().then(res => {
        this.businesstree = res.detail
      })
    }
  }
}
</script>

<style scoped>

</style>
