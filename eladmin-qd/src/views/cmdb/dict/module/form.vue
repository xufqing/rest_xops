<template>
  <el-dialog :append-to-body="true" :visible.sync="dialog" :title="isAdd ? '新增字典' : '编辑字典'" width="500px">
    <el-form ref="form" :model="form" :rules="rules" size="small" label-width="80px">
      <el-form-item label="Key" prop="key">
        <el-input v-model="form.key" style="width: 360px;"/>
      </el-form-item>
      <el-form-item label="Value" prop="value">
        <el-input v-model="form.value" style="width: 360px;"/>
      </el-form-item>
      <el-form-item label="父级字典">
        <treeselect v-model="form.pid" :options="dicts" style="width: 360px;" placeholder="请选择父级字典" />
      </el-form-item>
      <el-form-item style="margin-bottom: 0px;" label="描述">
        <el-input v-model="form.desc" style="width: 360px;" rows="5" type="textarea"/>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button type="text" @click="cancel">取消</el-button>
      <el-button :loading="loading" type="primary" @click="doSubmit">确认</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { add, edit } from '@/api/dict'
import Treeselect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
export default {
  components: { Treeselect },
  props: {
    dicts: {
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
      form: { key: '', value: '', desc: '', pid: null },
      rules: {
        key: [
          { required: true, message: '请输入Key', trigger: 'blur' }
        ],
        value: [
          { required: true, message: '请输入Value', trigger: 'blur' }
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
        this.$parent.$parent.getDicts()
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
        this.sup_this.getDicts()
      }).catch(err => {
        this.loading = false
        console.log(err)
      })
    },
    resetForm() {
      this.dialog = false
      this.$refs['form'].resetFields()
      this.form = { key: '', value: '', desc: '', pid: null }
    }
  }
}
</script>

<style scoped>

</style>
