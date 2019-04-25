<template>
  <div class="app-container">
    <eHeader :query="query"/>
    <el-row :gutter="28">
      <el-col :span="span">
        <!--表格渲染-->
        <el-table v-loading="loading" :data="data" size="small" border style="width: 100%;" @current-change="handleCurrentChange">
          <el-table-column label="序号" width="60" align="center">
            <template slot-scope="scope">
              <div>{{ scope.$index + 1 }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="名称"/>
          <el-table-column v-if="table_show" prop="desc" label="描述"/>
          <el-table-column label="操作" align="center">
            <template slot-scope="scope">
              <edit v-if="checkPermission(['admin','role_all','role_edit'])" :data="scope.row" :sup_this="sup_this"/>
              <el-popover
                v-if="checkPermission(['admin','role_all','role_delete'])"
                :ref="scope.row.id"
                placement="top"
                width="180">
                <p>确定删除本条数据吗？</p>
                <div style="text-align: right; margin: 0">
                  <el-button size="mini" type="text" @click="$refs[scope.row.id].doClose()">取消</el-button>
                  <el-button :loading="Loading" type="primary" size="mini" @click="subDelete(scope.row.id)">确定</el-button>
                </div>
                <el-button slot="reference" :disabled="scope.row.id === 1" type="danger" size="mini">删除</el-button>
              </el-popover>
            </template>
          </el-table-column>
        </el-table>
        <!--分页组件-->
        <el-pagination
          :total="total"
          style="margin-top: 8px;"
          layout="total, prev, pager, next, sizes"
          @size-change="sizeChange"
          @current-change="pageChange"/>
      </el-col>
      <el-col :span="8">
        <el-card v-if="show && checkPermission(['admin','role_all','role_edit'])" class="box-card">
          <div slot="header" class="clearfix">
            <span>菜单分配-{{ row_data.name }}</span>
            <el-button :loading="Loading" icon="el-icon-check" size="mini" type="success" style="float: right; padding: 4px 8px" @click="toSave">保存</el-button>
          </div>
          <el-tree
            ref="menu"
            :data="menu_list"
            :default-checked-keys="menuIds"
            check-strictly
            show-checkbox
            accordion
            node-key="id"
            highlight-current>
          </el-tree>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card v-if="show && checkPermission(['admin','role_all','role_edit'])" class="box-card">
          <div slot="header" class="clearfix">
            <span>权限分配-{{ row_data.name }}</span>
            <el-button :loading="Loading" icon="el-icon-check" size="mini" type="success" style="float: right; padding: 4px 8px" @click="is_permissions=true; toSave()">保存</el-button>
          </div>
          <el-tree
            ref="permission"
            :data="permission_list"
            :default-checked-keys="permissionIds"
            show-checkbox
            accordion
            node-key="id"
            highlight-current>
          </el-tree>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { save, retrieve } from '@/api/role'
import { getMenuTree } from '@/api/menu'
import { getPermissionTree } from '@/api/permission'
import initData from '@/mixins/initData'
import { del } from '@/api/role'
import { parseTime } from '@/utils/index'
import eHeader from './module/header'
import edit from './module/edit'
export default {
  components: { eHeader, edit },
  mixins: [initData],
  data() {
    return {
      row_data: null,
      span: 24,
      show: false,
      is_permissions: false,
      table_show: true,
      Loading: false,
      sup_this: this,
      permission_list: [],
      menu_list: [],
      permissionIds: [], menuIds: [],
      defaultProps: {
        children: 'children',
        label: 'label'
      }
    }
  },
  created() {
    this.$nextTick(() => {
      this.init()
      this.getPermissions()
      this.getMenus()
    })
  },
  methods: {
    parseTime,
    checkPermission,
    beforeInit() {
      this.url = 'api/roles/'
      const sort = 'id'
      const query = this.query
      const value = query.value
      this.params = { page: this.page, size: this.size, ordering: sort }
      if (value) { this.params['search'] = value }
      return true
    },
    handleCurrentChange(val) {
      if (val.id !== 1) {
        if (this.show) {
          // 清空选中状态
          this.$refs.permission.setCheckedKeys([])
          this.$refs.menu.setCheckedKeys([])
        }
        this.span = 8
        this.table_show = false
        this.show = true
        this.row_data = val
        if (this.row_data) {
          this.permissionIds = this.row_data.permissions
          this.menuIds = this.row_data.menus
        }
      } else {
        this.$message({
          showClose: true,
          type: 'error',
          message: '默认管理员不可修改!',
          duration: 2500
        })
      }
    },
    subDelete(id) {
      this.Loading = true
      del(id).then(res => {
        this.Loading = false
        this.$refs[id].doClose()
        this.init()
        this.$message({
          showClose: true,
          type: 'success',
          message: '删除成功!',
          duration: 2500
        })
      }).catch(err => {
        this.Loading = false
        this.$refs[id].doClose()
        console.log(err)
      })
    },
    toSave(id) {
      this.Loading = true
      let form = { menus: this.$refs.menu.getCheckedKeys() }
      if (this.is_permissions) {
        form = { permissions: this.$refs.permission.getCheckedKeys() }
      }
      save(this.row_data.id, form).then(res => {
        this.$message({
          showClose: true,
          type: 'success',
          message: '保存成功!',
          duration: 2500
        })
        this.Loading = false
        this.update(this.row_data.id)
      }).catch(err => {
        this.Loading = false
        console.log(err)
      })
    },
    update(id) {
      // 刷新选中行数据
      retrieve(id).then(res => {
        for (let i = 0; i < this.data.length; i++) {
          if (res.id === this.data[i].id) {
            this.data[i] = res
            break
          }
        }
      })
    },
    getMenus() {
      if (Array.isArray(this.menu_list) && this.menu_list.length === 0) {
        getMenuTree().then(res => {
          this.menu_list = res.detail
        })
      }
    },
    getPermissions() {
      if (Array.isArray(this.permission_list) && this.permission_list.length === 0) {
        getPermissionTree().then(res => {
          this.permission_list = res.detail
        })
      }
    }
  }
}
</script>

<style>
  .el-card__header {
    font-size: 14px;
  }
</style>
