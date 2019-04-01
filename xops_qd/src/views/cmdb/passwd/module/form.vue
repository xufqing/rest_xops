<template>
  <el-dialog :append-to-body="true" :visible.sync="dialog" :title="isAdd ? '新增密码' : '编辑密码'" width="550px">
    <el-form ref="form" :model="form" :rules="rules" size="small" label-width="100px">
      <el-form-item label="IP/URL" prop="hostname">
        <el-input v-model="form.hostname" style="width: 370px;"/>
      </el-form-item>
      <el-form-item label="服务类型" prop="auth_type">
        <el-select v-model="form.auth_type" style="width: 370px;" placeholder="请选择认证类型">
          <el-option v-for="item in service_types" :key="item.key" :label="item.value" :value="item.key"/>
        </el-select>
      </el-form-item>
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" style="width: 370px;"/>
      </el-form-item>
      <el-form-item label="密码/KEY" prop="password">
        <el-input v-model="form.password" style="width: 370px;"/>
      </el-form-item>
      <el-form-item label="是否公开" prop="is_public">
        <el-radio v-model="form.is_public" label="true">是</el-radio>
        <el-radio v-model="form.is_public" label="false" >否</el-radio>
      </el-form-item>
      <el-form-item label="端口" prop="port">
        <el-input v-model="form.port" style="width: 370px;"/>
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="form.desc" style="width: 370px;" rows="4" type="textarea"/>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button type="text" @click="cancel">取消</el-button>
      <el-button :loading="loading" type="primary" @click="doSubmit">确认</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { add, edit } from '@/api/connection'
export default {
  props: {
    isAdd: {
      type: Boolean,
      required: true
    },
    sup_this: {
      type: Object,
      default: null
    },
    service_types: {
      type: Array,
      default: null
    }
  },
  data() {
    return {
      loading: false, dialog: false,
      form: {
        id: '',
        hostname: '',
        auth_type: null,
        username: '',
        password: '',
        is_public: 'false',
        port: 0,
        desc: ''
      },
      rules: {
        hostname: [
          { required: true, message: '请输入IP/URL地址', trigger: 'blur' }
        ],
        auth_type: [
          { required: true, message: '请选择服务类型', trigger: 'blur' }
        ],
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ],
        is_public: [
          { required: true, message: '是否要公开该密码', trigger: 'blur' }
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
          if (this.isAdd) {
            this.doAdd()
          } else this.doEdit()
        } else {
          return false
        }
      })
    },
    doAdd() {
      add(this.form).then(res => {
        this.resetForm()
        this.$message({
          showClose: true,
          type: 'success',
          message: '添加成功!',
          duration: 2500
        })
        this.loading = false
        this.$parent.$parent.init()
      }).catch(err => {
        this.loading = false
        console.log(err)
      })
    },
    doEdit() {
      edit(this.form.id, this.form).then(res => {
        this.resetForm()
        this.$message({
          showClose: true,
          type: 'success',
          message: '修改成功!',
          duration: 2500
        })
        this.loading = false
        this.sup_this.init()
      }).catch(err => {
        this.loading = false
        console.log(err)
      })
    },
    resetForm() {
      this.dialog = false
      this.$refs['form'].resetFields()
      this.form = { hostname: '', auth_type: null, username: '', password: '', is_public: 'false', port: 0, desc: '' }
    }
  }
}
</script>

<style scoped>

</style>
