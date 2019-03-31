<template>
  <div style="display: inline-block">
    <el-button :disabled="data.id === 1" size="mini" class="button" type="primary" @click="dialog = true">密码</el-button>
    <el-dialog :visible.sync="dialog" :title="title" width="500px" @close="cancel">
      <el-form ref="form" :model="form" :rules="rules" size="small" label-width="88px">
        <el-form-item label="新密码" prop="new_password1">
          <el-input v-model="form.new_password1" type="password" auto-complete="on" style="width: 370px;"/>
        </el-form-item>
        <el-form-item label="确认密码" prop="new_password2">
          <el-input v-model="form.new_password2" type="password" auto-complete="on" style="width: 370px;"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="text" @click="cancel">取消</el-button>
        <el-button :loading="loading" type="primary" @click="doSubmit">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { updatePasswd } from '@/api/user'
export default {
  props: {
    data: {
      type: Object,
      required: true
    },
    // index.vue 的this 可用于刷新数据
    sup_this: {
      type: Object,
      required: true
    }
  },
  data() {
    const confirmPass = (rule, value, callback) => {
      if (this.form.new_password1 !== value) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    return {
      loading: false, dialog: false, title: '修改密码', form: { new_password1: '', new_password2: '' },
      rules: {
        new_password1: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
        ],
        new_password2: [
          { required: true, validator: confirmPass, trigger: 'blur' }
        ]
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
          this.loading = true
          updatePasswd(this.data.id, this.form).then(res => {
            this.resetForm()
            this.$message({
              showClose: true,
              type: 'success',
              message: '密码修改成功!请重新登录!',
              duration: 2500
            })
            this.sup_this.init()
          }).catch(err => {
            this.loading = false
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
      this.form = { new_password1: '', new_password2: '' }
    }
  }
}
</script>

<style scoped>

</style>
