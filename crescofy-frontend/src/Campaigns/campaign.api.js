import { API_URL, authHeader } from '@/Core/helpers/utils';
import axios from 'axios';

const RESOURCE_URL = `${API_URL}/api/v1/campaigns/`;

export default {
  get(token, params) {
    return axios.get(RESOURCE_URL, {
      params,
      headers: authHeader(token)
    })
  },
  update(token, obj) {
    let url = `${RESOURCE_URL}${obj.id}/`;
    return axios.patch(url, obj, {
      headers: authHeader(token)
    })
  },
  create(token, obj) {
    return axios.post(RESOURCE_URL, obj, {
      headers: authHeader(token)
    })
  },
  delete(token, objId) {
    let url = `${RESOURCE_URL}${objId}/`;
    return axios.delete(url, {
      headers: authHeader(token)
    })
  },
  duplicate(token, objId) {
    let url = `${RESOURCE_URL}${objId}/duplicate/`;
    return axios.post(url, {}, {
      headers: authHeader(token)
    })
  },
  metrics(token, params) {
    return axios.head(RESOURCE_URL, {
      params,
      headers: authHeader(token)
    })
  }
}
