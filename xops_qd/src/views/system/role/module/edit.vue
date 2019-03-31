<template>
  <div>
    <el-button :disabled="data.id === 1" size="mini" type="success" @click="to">编辑</el-button>
    <eForm ref="form" :permissions="permissions" :menus="menus" :sup_this="sup_this" :is-add="false"/>
  </div>
</template>
<script>
import eForm from './form'
import { getMenuTree } from '@/api/menu'
import { getPermissionTree } from '@/api/permission'
export default {
  components: { eForm },
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
      permissions: [], menus: []
    }
  },
  methods: {
    to() {
      getMenuTree().then(res => {
        this.menus = res.detail
      })
      getPermissionTree().then(res => {
        this.permissions = res.detail
      })
      const _this = this.$refs.form
      _this.permissionIds = []
      _this.menuIds = []
      _this.form = { id: this.data.id, name: this.data.name, desc: this.data.desc, permissions: [], menus: [] }
      this.data.permissions.forEach(function(data, index) {
        _this.permissionIds.push(data.id)
      })
      this.data.menus.forEach(function(data, index) {
        _this.menuIds.push(data.id)
      })
      _this.dialog = true
    }
  }
}
</script>

<style scoped>
  div{
    display: inline-block;
    margin-right: 3px;
  }
</style>
