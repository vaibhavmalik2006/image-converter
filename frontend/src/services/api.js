import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 120000,
})

export const uploadImage = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const convertImage = (params) => api.post('/convert', null, { params, responseType: 'blob' })
export const resizeImage = (params) => api.post('/resize', null, { params, responseType: 'blob' })
export const compressImage = (params) => api.post('/compress', null, { params, responseType: 'blob' })
export const changeDpi = (params) => api.post('/change-dpi', null, { params, responseType: 'blob' })
export const downloadFile = (fileId, params) => api.get(`/download/${fileId}`, { params, responseType: 'blob' })
