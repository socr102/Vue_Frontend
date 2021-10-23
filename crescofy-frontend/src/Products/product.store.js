import {
    LIST_PRODUCTS,
    TRENDING_PRODUCTS,
    CONNECTED_PRODUCTS,
    RECOMMENDED_PRODUCTS
  } from '@/Core/store/action-types';

import {SET_PRODUCTS_LIST} from '@/Core/store/mutation-types';
import api from './product.api';

const initialState = {};
const state = {...initialState};

const actions = {
  async [LIST_PRODUCTS]({rootState, commit}, {params, persist}) {
    var response = await api.get(rootState.user.userProfile.access, params);
    if (persist == true)
      commit(SET_PRODUCTS_LIST, response.data);
    return response.data;
  },

  async [TRENDING_PRODUCTS]({rootState}, {direction, params}) {
    let response = await api.trend(rootState.user.userProfile.access,
                                       direction, params)
    return response.data;
  },

  async [RECOMMENDED_PRODUCTS]({rootState}, product_ids) {
    let response = await api.recommendations(rootState.user.userProfile.access,
                                             product_ids)
    return response.data;
  },

  async [CONNECTED_PRODUCTS]({rootState}, params) {
    let response = await api.connected(rootState.user.userProfile.access,
                                       params)
    return response.data;
  },
};

const mutations = {
  [SET_PRODUCTS_LIST](state, productsList) {
    if (!Array.isArray(productsList)) {
      productsList = productsList.results;
    }

    state.productsList = productsList.map(v => {
      // vueform/multiselect require value prop
      v.value = v.id;
      return v;
    });
  },
};

const getters = {
  productsList(state) {
    return state.productsList;
  },
  getProdById: (state) => (id) => {
    return state.productsList.find(prod => prod.id === id)
  }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations,
    getters
};
