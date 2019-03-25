import request from '@/utils/request'

// 获取所有的字典树
export function getDictTree() {
  return request({
    url: 'api/dict/tree/',
    method: 'get'
  })
}

export function add(data) {
  return request({
    url: 'api/dicts/',
    method: 'post',
    data
  })
}

export function del(id) {
  return request({
    url: 'api/dicts/' + id + '/',
    method: 'delete'
  })
}

export function edit(id, data) {
  return request({
    url: 'api/dicts/' + id + '/',
    method: 'put',
    data
  })
}

export function getKey(...key) {
  return request({
    url: 'api/dicts/?&key=' + key,
    method: 'get'
  })
}
