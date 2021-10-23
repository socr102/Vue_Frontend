import {
  LIST_RECEIPT_ORDERS
} from '@/Core/store/action-types';

import api from './receipt.api'

const initialState = {};
const state = {...initialState};

const actions = {
  async [LIST_RECEIPT_ORDERS]({ rootState }, {params, objId}) {
    const resp = await api.get_detail(rootState.user.userProfile.access, params, objId);
    return resp.data;
  }
};

const mutations = {};
const getters = {};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
};
