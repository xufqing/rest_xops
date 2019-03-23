import request from '@/utils/request'

export function DeployExcu(data) {
  return request({
    url: 'api/deploy/excu/',
    method: 'post',
    data
  })
}

export function getVers(id) {
  return request({
    url: 'api/deploy/ver/?id=' + id,
    method: 'get'
  })
}

export function getRecords(id) {
  return request({
    url: 'api/deploy/records/?project_id=' + id,
    method: 'get'
  })
}
