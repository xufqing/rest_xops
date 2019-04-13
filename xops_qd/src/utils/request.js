import axios from 'axios'
import router from '@/router'
import { Notification, detailBox } from 'element-ui'
import store from '../store'
import { getToken } from '@/utils/auth'

// 创建axios实例
const service = axios.create({
  baseURL: process.env.BASE_API, // api 的 base_url
  timeout: 60000 // 请求超时时间
})

// request拦截器
service.interceptors.request.use(
  config => {
    if (getToken()) {
      config.headers['Authorization'] = 'Bearer ' + getToken() // 让每个请求携带自定义token 请根据实际情况自行修改
    }
    config.headers['Content-Type'] = 'application/json'
    if (config.data !== undefined) {
      if (config.data.excu !== undefined) {
        if (config.data.excu === 'tail_start') {
          config.timeout = 60000 * 20
        } else {
          config.timeout = 20000
        }
      }
    }
    return config
  },
  error => {
    // Do something with request error
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// response 拦截器
service.interceptors.response.use(
  response => {
    const code = response.status
    if (code < 200 || code > 300) {
      Notification.error({
        title: '错误',
        message: response.detail
      })
      return Promise.reject('error')
    } else {
      return response.data
    }
  },
  error => {
    let code = 0
    try {
      code = error.response.data.status
    } catch (e) {
      if (error.toString().indexOf('timeout')) {
        Notification.error({
          title: '错误',
          message: '请求超时!'
        })
        return Promise.reject(error)
      }
    }
    if (code === 401) {
      detailBox.confirm(
        '登录状态过期了哦，您可以继续留在该页面，或者重新登录',
        '系统提示',
        {
          confirmButtonText: '重新登录',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        store.dispatch('LogOut').then(() => {
          location.reload() // 为了重新实例化vue-router对象 避免bug
        })
      })
    } else if (code === 403) {
      router.push({ path: '/401' })
    } else if (code === 502) {
      Notification.error({
        title: '错误',
        message: '后端服务器连接失败!'
      })
    } else {
      const errorMsg = error.response.data.detail
      if (errorMsg !== undefined) {
        Notification.error({
          title: '错误',
          message: errorMsg,
          duration: 2500
        })
      }
    }
    return Promise.reject(error)
  }
)
export default service
