import {
  LIST_CAMPAIGNS,
  DELETE_CAMPAIGN,
  UPDATE_CAMPAIGN,
  CREATE_CAMPAIGN,
  DUPLICATE_CAMPAIGN
} from '@/Core/store/action-types';

import {
  SET_LIST_CAMPAIGNS,
  REMOVE_CAMPAIGN,
  ADD_CAMPAIGN,
  EDIT_CAMPAIGN
} from '@/Core/store/mutation-types';

import api from './campaign.api';

const initialState = {};
const state = {...initialState};

const actions = {
  async [LIST_CAMPAIGNS]({ commit, rootState }, {params, persist}) {
    const resp = await api.get(rootState.user.userProfile.access, params);
    if (persist == true)
      commit(SET_LIST_CAMPAIGNS, resp.data);
    return resp.data;
  },
  async [DELETE_CAMPAIGN]({ rootState, commit }, objId) {
    try {
      await api.delete(rootState.user.userProfile.access, objId);
      commit(REMOVE_CAMPAIGN, objId);
    } catch (e) {
      throw new Error("");
    }
  },
  async [CREATE_CAMPAIGN]({ rootState, commit }, obj) {
    const resp = await api.create(rootState.user.userProfile.access, obj);
    commit(ADD_CAMPAIGN, resp.data);
    return resp.data;
  },
  async [DUPLICATE_CAMPAIGN]({ rootState, commit }, obj) {
    const response = await api.duplicate(rootState.user.userProfile.access, obj);
    commit(ADD_CAMPAIGN, response.data);
    return response.data;
  },
  async [UPDATE_CAMPAIGN]({ rootState, commit }, obj) {
    const response = await api.update(rootState.user.userProfile.access, obj);
    commit(EDIT_CAMPAIGN, response.data);
    return response.data;
  },
};

const mutations = {
  [SET_LIST_CAMPAIGNS](state, campaignsList) {
    state.campaignsList = campaignsList;
  },
  [ADD_CAMPAIGN](state, obj) {
    state.campaignsList.push(obj);
  },
  [EDIT_CAMPAIGN](state, obj) {
    let idx = state.campaignsList.findIndex((u) => u.id == obj.id);

    if (idx > -1) {
      state.campaignsList[idx] = obj;
    }
  },
  [REMOVE_CAMPAIGN](state, objId) {
    let idx = state.campaignsList.findIndex((u) => u.id == objId);

    if (idx > -1) {
      state.campaignsList.splice(idx, 1);
    }
  }
};

const getters = {
  campaignsList(state) {
    return state.campaignsList;
  },
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
};
