<template>
  <div class="dashboard-container">
    <el-alert :closable="false" title="首页" type="success">
      <router-view />
    </el-alert>
  </div>
</template>
