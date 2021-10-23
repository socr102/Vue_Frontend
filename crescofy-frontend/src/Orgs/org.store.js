import {
  LIST_ORGS,
  DELETE_ORG,
  CREATE_ORG,
  UPDATE_ORG
} from '@/Core/store/action-types';

import {
  SET_ORGS_LIST,
  ADD_NEW_ORG,
  EDIT_ORG_FROM_LIST,
  REMOVE_ORG_FROM_LIST
} from '@/Core/store/mutation-types';

import { API_URL, authHeader } from '@/Core/helpers/utils';
import ServerErrorHandler from '@/Core/helpers/ServerErrorHandler';

import axios from 'axios';

const initialState = {};
const state = {...initialState};

const actions = {
  [LIST_ORGS]({ commit, rootState }) {
    let url = `${API_URL}/api/v1/orgs/`;

    return axios.get(url, {
      headers: authHeader(rootState.user.userProfile.access)
    })
      .then(function (response) {
        commit(SET_ORGS_LIST, response.data);
        return response.data;
      })
  },
  [DELETE_ORG]({ rootState, commit }, orgId) {
    let url = `${API_URL}/api/v1/orgs/${orgId}/`;

    return axios.delete(url, {
        headers: authHeader(rootState.user.userProfile.access)
      })
      .then(function () {
        commit(REMOVE_ORG_FROM_LIST, orgId);
      })
      .catch(function () { throw new Error("") });
  },
  [CREATE_ORG]({ rootState, commit }, {orgToCreate, actions}) {
    let url = `${API_URL}/api/v1/orgs/`;

    return axios.post(url, orgToCreate, {
        headers: authHeader(rootState.user.userProfile.access)
      })
      .then(function (response) {
        commit(ADD_NEW_ORG, response.data);
        return response.data;
      })
      .catch(function (error) {
        ServerErrorHandler(actions, error.response);
        throw new Error("");
      });
  },
  [UPDATE_ORG]({ rootState, commit }, {orgToUpdate, actions}) {
    let url = `${API_URL}/api/v1/orgs/${orgToUpdate.id}/`;

    return axios.patch(url, orgToUpdate, {
        headers: authHeader(rootState.user.userProfile.access)
      })
      .then(function (response) {
        commit(EDIT_ORG_FROM_LIST, response.data);
        return response.data;
      })
      .catch(function (error) {
        ServerErrorHandler(actions, error.response);
        throw new Error("");
      });
  },
};

const mutations = {
  [SET_ORGS_LIST](state, orgsList) {
    state.orgsList = orgsList;
  },
  [ADD_NEW_ORG](state, org) {
    state.orgsList.push(org);
  },
  [EDIT_ORG_FROM_LIST](state, editedOrg) {
    let idx = state.orgsList.findIndex((u) => u.id == editedOrg.id);

    if (idx > -1) {
      state.orgsList[idx] = editedOrg;
    }
  },
  [REMOVE_ORG_FROM_LIST](state, orgId) {
    let idx = state.orgsList.findIndex((u) => u.id == orgId);

    if (idx > -1) {
      state.orgsList.splice(idx, 1);
    }
  }
};
const getters = {
  orgsList(state) {
    return state.orgsList;
  },
  getOrgById: (state) => (id) => {
    return state.orgsList.find(org => org.id === id)
  }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations,
    getters
};
