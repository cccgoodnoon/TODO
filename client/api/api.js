/**
 * Created by Administrator on 2019/3/7.
 */
import axios from 'axios'
// import Qs from 'qs'

// const baseUrl =
//   process.env.NODE_ENV === "development" ?
//     "https://nei.netease.com/api/apimock/f3e5d93d5eaceda5a624378374ad5cd7"
//     : "http://127.0.0.1:5000"

const baseUrl = 'http://127.0.0.1:5000'

export const getAllTask = params => { return axios.get(`${baseUrl}/rest/anon/tasks`, {params: params}) }
export const addTask = params => { return axios.post(`${baseUrl}/rest/anon/tasks`, params).then(res => res.data) }
export const deleteTask = params => { return axios.post(`${baseUrl}/rest/anon/tasks`, params).then(res => res.data) }
export const updateTask = params => { return axios.post(`${baseUrl}/rest/anon/tasks`, params).then(res => res.data) }
export const updateManyTask = params => { return axios.post(`${baseUrl}/rest/anon/tasks`, params).then(res => res.data) }
export const deleteCompletedTask = params => { return axios.post(`${baseUrl}/rest/anon/tasks`, params) }
