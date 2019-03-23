<template>
  <el-form :model="form_base" size="small" label-width="80px">
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
        <el-form-item label="SSH端口">
          <el-input v-model="form_base.port" :readonly="is_Readonly" style="width: 300px;"/>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12">
        <el-form-item label="用户">
          <el-input v-model="form_base.username" :readonly="is_Readonly" style="width: 300px;"/>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item :label="form_base.auth_type === 'password' ? '密码' : '秘钥路径'">
          <el-input v-model="form_base.password" :readonly="is_Readonly" style="width: 300px;"/>
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
        <el-form-item label="系统类型">
          <el-input v-model="form_base.os_type" :readonly="is_Readonly" style="width: 300px;"/>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12">
        <el-form-item label="设备类型">
          <el-input v-model="form_base.device_type" :readonly="is_Readonly" style="width: 300px;"/>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="MAC地址">
          <el-input v-model="form_base.mac_address" :readonly="is_Readonly" style="width: 300px;"/>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12">
        <el-form-item label="入库时间">
          <span style="width: 300px;">{{ form_base.add_time }}</span>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row>
      <el-form-item v-if="form_base.error_message" label="错误信息">
        <el-input v-model="form_base.error_message" :readonly="is_Readonly" style="width: 720px;" type="textarea"/>
      </el-form-item>
    </el-row>
    <el-form-item size="medium">
      <div style="display: inline-block;margin: 70px 0px;float: left">
        <el-button type="primary" @click="closeTag">返回</el-button>
      </div>
    </el-form-item>
  </el-form>
</template>

<script>
import { retrieve } from '@/api/scan'
import { parseTime } from '@/utils/index'
export default {
  name: 'Base',
  data() {
    return {
      form_base: {
        id: '',
        add_time: '',
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
        os_type: '',
        device_type: '',
        error_message: ''
      },
      is_Readonly: true,
      types: [{ value: 'password', label: '密码认证' }, { value: 'key_filename', label: '密钥认证' }]
    }
  },
  created() {
    retrieve(this.$route.query.id).then(res => {
      this.form_base = res
      this.form_base.add_time = parseTime(this.form_base.add_time)
      this.form_base.modify_time = parseTime(this.form_base.modify_time)
    })
  },
  methods: {
    closeTag() {
      this.$store.dispatch('delView', this.$store.state.tagsView.visitedViews.slice(-1)[0])
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>

</style>
