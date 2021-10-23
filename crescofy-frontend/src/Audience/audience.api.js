import { API_URL, authHeader } from '@/Core/helpers/utils';
import axios from 'axios';

const RESOURCE_URL = `${API_URL}/api/v1/audience/`;

export default {
  get(token) {
    return axios.get(RESOURCE_URL, {
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
  }
}
