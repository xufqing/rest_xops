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

export function ApplogExcu(data) {
  return request({
    url: 'api/deploy/applog/',
    method: 'post',
    data
  })
}

// export function ApplogDown(sid, file) {
//   return request({
//     url: 'api/deploy/applog/?sid=' + sid + '&file=' + file,
//     method: 'get'
//   })
// }
export function ApplogDown(data) {
  return request({
    url: 'api/deploy/applog/',
    method: 'post',
    data,
    responseType: 'blob'
  })
}

