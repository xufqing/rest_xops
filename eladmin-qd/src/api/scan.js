import request from '@/utils/request'

export function getScanDevices() {
  return request({
    url: 'api/scan/devices/',
    method: 'get'
  })
}

export function del(id) {
  return request({
    url: 'api/scan/devices/' + id + '/',
    method: 'delete'
  })
}

export function retrieve(id) {
  return request({
    url: 'api/scan/devices/' + id + '/',
    method: 'get'
  })
}

export function save(id) {
  return request({
    url: 'api/scan/devices/' + id + '/',
    method: 'post'
  })
}

export function getScanSetting() {
  return request({
    url: 'api/scan/setting/',
    method: 'get'
  })
}

export function SettingSave(data) {
  return request({
    url: 'api/scan/setting/',
    method: 'post',
    data
  })
}

export function ScanExcu(data) {
  return request({
    url: 'api/scan/excu/',
    method: 'post',
    data
  })
}
