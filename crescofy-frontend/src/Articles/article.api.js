import { API_URL, authHeader } from '@/Core/helpers/utils';
import axios from 'axios';

const RESOURCE_URL = `${API_URL}/api/v1/articles/`;
const RESOURCE_TREND_URL = `${API_URL}/api/v1/trends/article/`;

export default {
  get(token, params) {
    return axios.get(RESOURCE_URL, {
      params,
      headers: authHeader(token)
    });
  },
  trend(token, direction, params) {
    return axios.get(`${RESOURCE_TREND_URL}${direction}`, {
      params, headers: authHeader(token)
    })
  },
  recommendations(token, article_ids) {
    let url = `${RESOURCE_URL}rec/?`;
    article_ids.forEach((id) => { url += `&article=${id}` });
    return axios.get(url, { headers: authHeader(token) });
  },
  connected(token, product_ids) {
    let url = `${RESOURCE_URL}connected/?`;
    product_ids.forEach((id) => { url += `&product=${id}` });
    return axios.get(url, { headers: authHeader(token) });
  },
  metrics(token, params) {
    return axios.head(RESOURCE_URL, {
      params,
      headers: authHeader(token)
    });
  }
}
