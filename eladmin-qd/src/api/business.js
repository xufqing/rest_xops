import request from '@/utils/request'

// 获取所有的business
export function getBusinessTree() {
  return request({
    url: 'api/business/tree/',
    method: 'get'
  })
}

export function add(data) {
  return request({
    url: 'api/businesses/',
    method: 'post',
    data
  })
}

export function del(id) {
  return request({
    url: 'api/businesses/' + id + '/',
    method: 'delete'
  })
}

export function edit(id, data) {
  return request({
    url: 'api/businesses/' + id + '/',
    method: 'put',
    data
  })
}
