import {
  LIST_AUDIENCE,
  DELETE_AUDIENCE,
  UPDATE_AUDIENCE,
  CREATE_AUDIENCE
} from '@/Core/store/action-types';

import {
  SET_AUDIENCE_LIST,
  REMOVE_AUDIENCE,
  ADD_AUDIENCE,
  EDIT_AUDIENCE
} from '@/Core/store/mutation-types';

import api from './audience.api'

const initialState = {};
const state = {...initialState};

const actions = {
  [LIST_AUDIENCE]({ commit, rootState }) {
    api.get(rootState.user.userProfile.access)
      .then(resp => {
        commit(SET_AUDIENCE_LIST, resp.data);
        return resp.data;
      })
  },
  [DELETE_AUDIENCE]({ rootState, commit }, objId) {
    return api.delete(rootState.user.userProfile.access, objId)
      .then(function () { commit(REMOVE_AUDIENCE, objId) })
      .catch(function () { throw new Error("") });
  },
  [CREATE_AUDIENCE]({ rootState, commit }, obj) {
    return api.create(rootState.user.userProfile.access, obj)
      .then(resp => {
        commit(ADD_AUDIENCE, resp.data);
        return resp.data;
      })

  },
  [UPDATE_AUDIENCE]({ rootState, commit }, obj) {
    return api.update(rootState.user.userProfile.access, obj)
      .then(function (response) {
        commit(EDIT_AUDIENCE, response.data);
        return response.data;
      })
  },
};

const mutations = {
  [SET_AUDIENCE_LIST](state, audienceList) {
    state.audienceList = audienceList;
  },
  [ADD_AUDIENCE](state, obj) {
    state.audienceList.push(obj);
  },
  [EDIT_AUDIENCE](state, obj) {
    let idx = state.audienceList.findIndex((u) => u.id == obj.id);

    if (idx > -1) {
      state.audienceList[idx] = obj;
    }
  },
  [REMOVE_AUDIENCE](state, objId) {
    let idx = state.audienceList.findIndex((u) => u.id == objId);

    if (idx > -1) {
      state.audienceList.splice(idx, 1);
    }
  }
};

const getters = {
  audienceList(state) {
    return state.audienceList;
  },
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
};
