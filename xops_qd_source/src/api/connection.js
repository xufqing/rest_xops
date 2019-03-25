import request from '@/utils/request'

export function getConnections() {
  return request({
    url: 'api/connections/',
    method: 'get'
  })
}
export function search(hostname) {
  return request({
    url: 'api/connections/?search=' + hostname,
    method: 'get'
  })
}

export function add(data) {
  return request({
    url: 'api/connections/',
    method: 'post',
    data
  })
}
export function retrieve(id) {
  return request({
    url: 'api/connections/' + id + '/',
    method: 'get'
  })
}

export function del(id) {
  return request({
    url: 'api/connections/' + id + '/',
    method: 'delete'
  })
}

export function edit(id, data) {
  return request({
    url: 'api/connections/' + id + '/',
    method: 'put',
    data
  })
}
