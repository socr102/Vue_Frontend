import { API_URL, authHeader } from '@/Core/helpers/utils';
import axios from 'axios';

const RESOURCE_URL = `${API_URL}/api/v1/products/`;
const RESOURCE_TREND_URL = `${API_URL}/api/v1/trends/product/`;

export default {
  get(token, params) {
    return axios.get(RESOURCE_URL, {
      params,
      headers: authHeader(token)
    });
  },
  trend(token, direction, params) {
    return axios.get(`${RESOURCE_TREND_URL}${direction}`, {
      params,
      headers: authHeader(token)
    })
  },
  connected(token, params) {
    return axios.get(`${RESOURCE_URL}connected/`, {
      params,
      headers: authHeader(token)
    });
  },
  recommendations(token, product_ids) {
    let url = `${RESOURCE_URL}rec/?`;
    product_ids.forEach((id) => {
      url += `&product=${id}`;
    });
    return axios.get(url, { headers: authHeader(token) });
  },
  metrics(token, params) {
    return axios.head(RESOURCE_URL, {
      params,
      headers: authHeader(token)
    });
  }
}
