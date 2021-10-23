import {
  LIST_OFFERS,
  CREATE_OFFER,
  UPDATE_OFFER,
  DELETE_OFFER
} from '@/Core/store/action-types';

import {
  SET_OFFERS_LIST,
  ADD_OFFER,
  EDIT_OFFER,
  REMOVE_OFFER
} from '@/Core/store/mutation-types';

import api from './offer.api';

const initialState = {};
const state = {...initialState};

const actions = {
  async [LIST_OFFERS]({ commit, rootState }, params) {
    const response = await api.get(rootState.user.userProfile.access, params);
    commit(SET_OFFERS_LIST, response.data);
    return response.data;
  },
  async [CREATE_OFFER]({ commit, rootState }, {obj}) {
    const response = await api.create(rootState.user.userProfile.access, obj);
    commit(ADD_OFFER, response.data);
    return response.data;
  },

  async [UPDATE_OFFER]({ commit, rootState }, {obj}) {
    const response = await api.update(rootState.user.userProfile.access, obj);
    commit(EDIT_OFFER, response.data);
    return response.data;
  },

  async [DELETE_OFFER]({ commit, rootState }, objId) {
    try {
      await api.delete(rootState.user.userProfile.access, objId);
      commit(REMOVE_OFFER, objId);
    } catch (e) {
      throw new Error("");
    }
  },
};

const mutations = {
  [SET_OFFERS_LIST](state, offersList) {
    state.offersList = offersList;
  },
  [ADD_OFFER](state, offer) {
    state.offersList.push(offer);
  },
  [EDIT_OFFER](state, offer) {
    let idx = state.offersList.findIndex((u) => u.id == offer.id);

    if (idx > -1) {
      state.offersList[idx] = offer;
    }
  },
  [REMOVE_OFFER](state, offerId) {
    let idx = state.offersList.findIndex((u) => u.id == offerId);

    if (idx > -1) {
      state.offersList.splice(idx, 1);
    }
  }
};
const getters = {
  offersList(state) {
    return state.offersList;
  }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations,
    getters
};
