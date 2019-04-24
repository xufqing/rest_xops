import request from '@/utils/request'

export function getLabels() {
  return request({
    url: 'api/labels/',
    method: 'get'
  })
}

export function add(data) {
  return request({
    url: 'api/labels/',
    method: 'post',
    data
  })
}

export function del(id) {
  return request({
    url: 'api/labels/' + id + '/',
    method: 'delete'
  })
}

export function retrieve(id) {
  return request({
    url: 'api/labels/' + id + '/',
    method: 'get'
  })
}

export function edit(id, data) {
  return request({
    url: 'api/labels/' + id + '/',
    method: 'put',
    data
  })
}

export function save(id, data) {
  return request({
    url: 'api/labels/' + id + '/',
    method: 'patch',
    data
  })
}

