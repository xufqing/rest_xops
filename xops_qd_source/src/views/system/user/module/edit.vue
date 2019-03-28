<template>
  <div>
    <el-button :disabled="data.id === 1" size="mini" type="success" @click="to">编辑</el-button>
    <eForm ref="form" :roles="roles" :organizations="organizations" :orgusers="orgusers" :sup_this="sup_this" :is-add="false"/>
  </div>
</template>
<script>
import eForm from './form'
import { getOrganizationUserTree } from '@/api/organization'
export default {
  components: { eForm },
  props: {
    organizations: {
      type: Array,
      required: true
    },
    roles: {
      type: Array,
      required: true
    },
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
    return {
      orgusers: []
    }
  },
  methods: {
    to() {
      const _this = this.$refs.form
      _this.roleIds = []
      let did = null
      if (this.data.department !== null) {
        did = this.data.department.id
      }
      let uid = null
      if (this.data.superior !== null) {
        uid = this.data.superior.id
      }
      _this.form = {
        id: this.data.id,
        username: this.data.username,
        name: this.data.name,
        email: this.data.email,
        mobile: this.data.mobile,
        is_active: this.data.is_active.toString(),
        department: did,
        superior: uid,
        position: this.data.position,
        roles: [] }
      this.data.roles.forEach(function(data, index) {
        _this.roleIds.push(data.id)
      })
      _this.dialog = true
      getOrganizationUserTree().then(res => {
        this.orgusers = res.detail
      })
    }
  }
}
</script>

<style scoped>
  div{display: inline-block;margin-right: 3px;}
</style>
