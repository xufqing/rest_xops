<template>
  <el-dialog :append-to-body="true" :visible.sync="dialog" :title="isAdd ? '新增角色' : '编辑角色'" width="500px">
    <el-form ref="form" :model="form" :rules="rules" size="small" label-width="66px">
      <el-form-item label="名称" prop="name">
        <el-input v-model="form.name" style="width: 370px;"/>
      </el-form-item>
      <el-form-item label="权限">
        <treeselect v-model="permissionIds" :multiple="true" :options="permissions" style="width: 370px;" placeholder="请选择权限" />
      </el-form-item>
      <el-form-item label="菜单">
        <treeselect v-model="menuIds" :multiple="true" :options="menus" :flat="true" :auto-select-ancestors="true" :auto-deselect-descendants="true" :default-expand-level="1" style="width: 370px;" placeholder="请选择菜单" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="form.desc" style="width: 370px;" rows="5" type="textarea"/>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button type="text" @click="cancel">取消</el-button>
      <el-button :loading="loading" type="primary" @click="doSubmit">确认</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { add, edit } from '@/api/role'
import Treeselect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
export default {
  components: { Treeselect },
  props: {
    permissions: {
      type: Array,
      required: true
    },
    menus: {
      type: Array,
      required: true
    },
    isAdd: {
      type: Boolean,
      required: true
    },
    sup_this: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      loading: false, dialog: false,
      form: { name: '', permissions: [], menus: [], desc: '' }, permissionIds: [], menuIds: [],
      rules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' }
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
          this.form.permissions = []
          this.form.menus = []
          const _this = this
          this.permissionIds.forEach(function(data, index) {
            _this.form.permissions.push(data)
          })
          this.menuIds.forEach(function(data, index) {
            _this.form.menus.push(data)
          })
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
      this.permissionIds = []
      this.menuIds = []
      this.form = { name: '', permissions: [], menus: [], desc: '' }
    }
  }
}
</script>

<style scoped>

</style>
