<template>
  <el-dialog :append-to-body="true" :visible.sync="dialog" title="扫描设置" width="600px">
    <el-form ref="form" :model="form" size="small" label-width="80px">
      <el-form-item label="扫描网段" prop="net_address">
        <el-input v-model="form.net_address" style="width: 460px;"/>
      </el-form-item>
      <el-form-item label="认证方式" prop="auth_type">
        <el-select v-model="form.auth_type" style="width: 200px;" placeholder="请选择认证类型">
          <el-option v-for="item in types" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="登陆用户" prop="ssh_username">
        <el-input v-model="form.ssh_username" style="width: 200px;"/>
      </el-form-item>
      <el-form-item v-if="form.auth_type == 'password'" label="登陆密码" prop="ssh_password">
        <el-input v-model="form.ssh_password" style="width: 200px;"/>
      </el-form-item>
      <el-form-item v-if="form.auth_type == 'key_filename'" label="密钥路径" prop="ssh_private_key">
        <el-input v-model="form.ssh_private_key" style="width: 460px;"/>
      </el-form-item>
      <el-form-item label="SSH端口" prop="ssh_port">
        <el-input v-model="form.ssh_port" style="width: 200px;"/>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button type="text" @click="cancel">取消</el-button>
      <el-button :loading="loading" type="primary" @click="doSubmit">确认</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { SettingSave } from '@/api/scan'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
export default {
  data() {
    return {
      loading: false, dialog: false,
      types: [{ value: 'password', label: '密码认证' }, { value: 'key_filename', label: '密钥认证' }],
      form: {
        net_address: '',
        auth_type: '',
        ssh_username: '',
        ssh_password: '',
        ssh_port: '',
        ssh_private_key: '',
        commands: {}
      }
    }
  },
  methods: {
    cancel() {
      this.resetForm()
    },
    doSubmit() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.doSave()
        }
      })
    },
    doSave() {
      SettingSave(this.form).then(res => {
        this.resetForm()
        this.$message({
          showClose: true,
          type: 'success',
          message: '保存成功!',
          duration: 2500
        })
        this.loading = false
        console.log(this)
        this.$parent.getSettings()
      }).catch(err => {
        this.loading = false
        console.log(err)
      })
    },
    resetForm() {
      this.dialog = false
      this.$refs['form'].resetFields()
      this.form = {
        net_address: '',
        auth_type: '',
        ssh_username: '',
        ssh_password: '',
        ssh_port: '',
        ssh_private_key: '',
        commands: {}
      }
    }
  }
}
</script>

<style scoped>

</style>
