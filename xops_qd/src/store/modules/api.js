const baseUrl = process.env.BASE_API
const api = {
  state: {
    // 部署实时控制台
    socketApi: baseUrl + '/api/deploy/console/'
  }
}

export default api
