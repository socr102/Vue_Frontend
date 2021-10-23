import {
  LIST_MEMBERS,
  CREATE_MEMBER,
  DELETE_MEMBER,
  UPDATE_MEMBER,
  LIST_MEMBER_RECEIPTS,
  LIST_MEMBER_CAMPAIGNS,
  LIST_MEMBER_CAMPAIGN_ORDERS
} from '@/Core/store/action-types';

import {
  SET_MEMBERS_LIST,
  REMOVE_MEMBER,
  EDIT_MEMBER,
  ADD_MEMBER
} from '@/Core/store/mutation-types';

import api from './member.api'

const initialState = {};
const state = {...initialState};

const actions = {
  async [LIST_MEMBERS]({ commit, rootState }, {params, persist}) {
    const resp = await api.get(rootState.user.userProfile.access,
                               params);
    let members = resp.data.results ? resp.data.results: resp.data;
    if (persist) commit(SET_MEMBERS_LIST, members);
    return resp.data;
  },
  async [DELETE_MEMBER]({ rootState, commit }, objId) {
    try {
      await api.delete(rootState.user.userProfile.access, objId);
      commit(REMOVE_MEMBER, objId);
    } catch (e) {
      throw new Error("");
    }
  },
  async [CREATE_MEMBER]({ rootState, commit }, obj) {
    const resp = await api.create(rootState.user.userProfile.access, obj);
    commit(ADD_MEMBER, resp.data);
    return resp.data;
  },
  async [LIST_MEMBER_RECEIPTS]({ rootState }, {params, objId}) {
    const resp = await api.get_receipts(rootState.user.userProfile.access, params, objId);
    return resp.data;
  },
  async [LIST_MEMBER_CAMPAIGNS]({ rootState }, {params, objId}) {
    const resp = await api.get_campaigns(rootState.user.userProfile.access, params, objId);
    return resp.data;
  },
  async [LIST_MEMBER_CAMPAIGN_ORDERS]({ rootState }, {params, objId, campaignId}) {
    const resp = await api.get_campaign_orders(rootState.user.userProfile.access,
                                               params, objId, campaignId);
    return resp.data;
  },
  async [UPDATE_MEMBER]({ rootState, commit }, obj) {
    const response = await api.update(rootState.user.userProfile.access, obj);
    commit(EDIT_MEMBER, response.data);
    return response.data;
  }
};

const mutations = {
  [SET_MEMBERS_LIST](state, membersList) {
    state.membersList = membersList.results ? membersList.results: membersList;
  },
  [ADD_MEMBER](state, obj) {
    state.membersList.push(obj);
  },
  [EDIT_MEMBER](state, obj) {
    let idx = state.membersList.findIndex((u) => u.id == obj.id);

    if (idx > -1) {
      state.membersList[idx] = obj;
    }
  },
  [REMOVE_MEMBER](state, objId) {
    let idx = state.membersList.findIndex((u) => u.id == objId);

    if (idx > -1) {
      state.membersList[idx].is_active = false;
    }
  }
};

const getters = {
  membersList(state) {
    return state.membersList;
  }
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
};
