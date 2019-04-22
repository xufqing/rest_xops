<template>
  <div style="display: inline-block;margin: 0px 1px;">
    <el-button size="mini" type="primary" @click="to">成员管理</el-button>
    <el-dialog :append-to-body="true" :visible.sync="dialog" title="项目成员管理" width="540px">
      <el-form ref="form" :model="form" label-position="top" size="small">
        <el-form-item>
          <el-transfer
            v-model="userIds"
            :filter-method="userFilterMethod"
            :data="user_data"
            :titles="user_name"
            filterable
            filter-placeholder="请选择用户"></el-transfer>
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
import { getUserList } from '@/api/user'
import { edit } from '@/api/project'
export default {
  props: {
    data: {
      type: Object,
      required: true
    },
    sup_this: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      loading: false, dialog: false,
      form: { user_id: '' },
      userIds: [],
      user_name: ['可选用户', '已选用户'],
      user_data: []
    }
  },
  methods: {
    to() {
      this.memberInit()
      this.dialog = true
    },
    memberInit() {
      getUserList().then(res => {
        this.user_data = []
        const _userdata = this.user_data
        res.forEach(function(data, index) {
          const new_data = {
            key: data.id.toString(),
            label: data.name
          }
          _userdata.push(new_data)
        })
      })
      this.userIds = this.data.user_id.split(',')
    },
    userFilterMethod(query, item) {
      return item.label.indexOf(query) > -1
    },
    doSubmit() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.form.user_id = this.userIds.filter(d => d).toString()
          this.loading = true
          edit(this.data.id, this.form).then(res => {
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
        } else {
          return false
        }
      })
    },
    cancel() {
      this.resetForm()
    },
    resetForm() {
      this.dialog = false
      this.$refs['form'].resetFields()
      this.form = { user_id: '' }
    }
  }
}
</script>
