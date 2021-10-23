import { LIST_STORES } from '@/Core/store/action-types';
import api from './store.api';

const initialState = {};
const state = {...initialState};

const actions = {
  async [LIST_STORES]({rootState}, {params}) {
    let response = await api.get(rootState.user.userProfile.access, params);
    return response.data;
  },
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
