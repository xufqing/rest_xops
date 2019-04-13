<template>
  <div :style="'width:' + width" class="container">
    <el-row>
      <el-col :span="21">
        <el-card class="box-card">
          <el-tooltip content="返回上一页" class="closepage item" effect="dark" placement="left">
            <el-button type="info" size="mini" circle @click="closeTag"><svg-icon icon-class="return"/></el-button>
          </el-tooltip>
          <el-tooltip :content="content" class="lock item" effect="dark" placement="left">
            <el-button type="info" size="mini" circle @click="doLock"><svg-icon :icon-class="ico"/></el-button>
          </el-tooltip>
          <div id="console" :style="'height:'+ height" class="console">
            <div v-for="item in data" :key="item.id">
              <span class="line-html" v-html="item"/>
            </div>
            <div style="text-align:center">
              <span v-loading="sequence == 6 ? false : true" element-loading-spinner="el-icon-loading"/>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card class="box-card">
          <div :style="'height:' + height">
            <el-steps :active="sequence" direction="vertical" finish-status="success" align-center>
              <el-step title="检出前置"></el-step>
              <el-step title="检出代码"></el-step>
              <el-step title="检出后置"></el-step>
              <el-step title="部署前置"></el-step>
              <el-step title="部署"></el-step>
              <el-step title="部署后置"></el-step>
            </el-steps>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Vue from 'vue'
import { parseTime } from '@/utils/index'
import { getToken } from '@/utils/auth'
import { DeployExcu } from '@/api/deploy'
import VueNativeSock from 'vue-native-websocket'
export default {
  data() {
    return {
      ico: 'unlock', unlock: true, content: '锁定滚动条',
      height: document.documentElement.clientHeight - 94.5 + 'px;',
      width: document.documentElement.clientWidth - 225 + 'px;',
      data: [],
      vm: null,
      sequence: 1
    }
  },
  // 监听控制滚动条
  watch: {
    data: {
      handler(val, oldVal) {
        this.$nextTick(() => {
          if (this.unlock) {
            var div = document.getElementById('console')
            div.scrollTop = div.scrollHeight
          }
        })
      }
    }
  },
  mounted: function() {
    if (this.$route.query.scenario === 0) {
      this.initWebSocket()
    } else {
      this.readLog()
    }
    const that = this
    window.onresize = function temp() {
      that.height = document.documentElement.clientHeight - 94.5 + 'px;'
    }
  },
  beforeDestroy: function() {
    if (this.$route.query.scenario === 0) {
      this.vm.$disconnect(this.$route.query.id)
      console.log('---离开页面关闭Websocket---')
    }
  },
  methods: {
    parseTime,
    initWebSocket() {
      const wsuri = 'ws://' + process.env.BASE_API.replace(/http:\/\//, '') + '/websocket/console?token=' + getToken()
      Vue.use(VueNativeSock, wsuri, {
        // format: 'json',
        connectManually: true,
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 3000
      })
      this.vm = new Vue()
      this.vm.$connect()
      console.log('---连接Websocket----')
      this.$socket.onopen = (data) => {
        if (data.target.readyState === 1) {
          console.log('--------等待数据!--------')
          this.$socket.onmessage = (data) => {
            const color_data = this.getColor(data.data)
            this.data.push(color_data)
          }
        }
        this.$nextTick(() => {
          this.start()
        })
      }
    },
    start() {
      const data = {
        excu: 'deploymsg',
        id: this.$route.query.id,
        alias: this.$route.query.alias,
        record: this.$route.query.record,
        scenario: this.$route.query.scenario
      }
      // 开始读取
      DeployExcu(data)
    },
    // 读取部署日志
    readLog() {
      const form = {
        excu: 'readlog',
        id: this.$route.query.id,
        alias: this.$route.query.alias,
        record: this.$route.query.record,
        scenario: 1
      }
      DeployExcu(form).then(res => {
        const content = res.split('\n')
        const _this = this
        content.forEach(function(new_data, index) {
          _this.data.push(_this.getColor(new_data))
        })
      }).catch(err => {
        console.log(err)
      })
    },
    closeTag() {
      this.$confirm('是否关闭页面并返回上一页?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if (this.$route.query.scenario === 0) {
          this.vm.$disconnect()
          console.log('---离开页面关闭Websocket---')
        }
        this.$router.go(-1)
        this.$store.dispatch('delView', this.$store.state.tagsView.visitedViews.slice(-1)[0])
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消操作'
        })
      })
    },
    getColor(text) {
      const info = text.match(/INFO/i)
      const warn = text.match(/WARN/i)
      const warning = text.match(/WARNING/i)
      const debug = text.match(/DEBUG/i)
      const host = text.match(/\[(.*?)@(.*?)\]/)
      const error = text.match(/ERROR/i)
      const sequence = text.match(/(.*?[\u4e00-\u9fa5])\[(.*?\d)\]------/)
      if (sequence) {
        this.sequence = parseInt(sequence[2])
      }
      if (info) {
        return text.replace(/INFO/i, '<span style="color: #7FFF00;">' + info + '</span>')
      } else if (warning) {
        return text.replace(/WARNING/i, '<span style="color: #FFFF00;">' + warning + '</span>')
      } else if (warn) {
        return text.replace(/WARN/i, '<span style="color: #FFFF00;">' + warn + '</span>')
      } else if (debug) {
        return text.replace(/DEBUG/i, '<span style="color: #0000ff;">' + debug + '</span>')
      } else if (host) {
        return text.replace(/\[(.*?)@(.*?)\]/, '<span style="color: #FFA54F;">' + host[0] + '</span>')
      } else if (error) {
        return text.replace(/ERROR/i, '<span style="color: #FF0000;">' + error + '</span>')
      } else {
        return text
      }
    },
    doLock() {
      if (this.unlock) {
        this.content = '解除锁定'
        this.ico = 'lock'
      } else {
        this.content = '锁定滚动条'
        this.ico = 'unlock'
      }
      this.unlock = !this.unlock
    }
  }
}
</script>
<style>
  button,input,textarea {
    outline: 0
  }
  .loadclass {
    height: 25px;
  }
  .line-html {
    line-height: 1.85
  }
  .closepage {
    margin: 40px;
    position: fixed;
    right: 115px;
    bottom: 2%;
    z-index: 100000;
  }
  .el-card__body {
    padding: 5px;
  }
  .container {
    width: 100%;
    margin: 5px
  }
  .container .console {
    font-family: "Interstate", "Hind", -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol;
    overflow-y: scroll;
    background: #494949;
    color: #f7f7f7;
    padding: 10px;
    font-size: 14px;
    border-radius: 3px 1px 3px 3px;
  }
  .lock {
    position: fixed;
    right: 155px;
    bottom: 2%;
    z-index: 100000
  }
</style>

