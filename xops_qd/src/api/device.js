import request from '@/utils/request'

export function getDevices() {
  return request({
    url: 'api/devices/',
    method: 'get'
  })
}

export function getDeviceList(os_type) {
  if (os_type) {
    return request({
      url: 'api/device/list/?os_type=' + os_type,
      method: 'get'
    })
  } else {
    return request({
      url: 'api/device/list/',
      method: 'get'
    })
  }
}

export function add(data) {
  return request({
    url: 'api/devices/',
    method: 'post',
    data
  })
}

export function retrieve(id) {
  return request({
    url: 'api/devices/' + id + '/',
    method: 'get'
  })
}

export function del(id) {
  return request({
    url: 'api/devices/' + id + '/',
    method: 'delete'
  })
}

export function edit(id, data) {
  return request({
    url: 'api/devices/' + id + '/',
    method: 'put',
    data
  })
}
