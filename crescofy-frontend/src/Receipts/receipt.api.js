import { API_URL, authHeader } from '@/Core/helpers/utils';
import axios from 'axios';

const RESOURCE_URL = `${API_URL}/api/v1/receipts/`;

export default {
  get_detail(token, params, objId) {
    return axios.get(`${RESOURCE_URL}${objId}/`, {
      params,
      headers: authHeader(token)
    });
  },
}
