import {
    SET_USER,
    SET_USERS_LIST,
    REMOVE_USER_FROM_LIST,
    ADD_NEW_USER,
    EDIT_USER_FROM_LIST
  } from '@/Core/store/mutation-types';

  import {
    REGISTER,
    LOGOUT,
    LOGIN,
    LIST_USERS,
    DEACTIVATE_USER,
    UPDATE_USER,
    FULL_DELETE_USER,
    CHANGE_OWN_PASSWORD
  } from '@/Core/store/action-types';

  import ServerErrorHandler from '@/Core/helpers/ServerErrorHandler';
  import {authHeader, API_URL} from '@/Core/helpers/utils';
  import {defineRulesFor} from '@/Core/helpers/ability';

  import axios from 'axios';

  function saveUserProfile(userProfile) {
    localStorage.setItem('userProfile', JSON.stringify(userProfile));
  }

  function loadUserProfile() {
    try {
      return JSON.parse(localStorage.getItem('userProfile') || '{}');
    } catch {
      return {};
    }
  }

  const initialState = {
    // my user profile
    userProfile: loadUserProfile(),
    // list of external users available to manage
    usersList: []
  };

  const state = {...initialState};

  const actions = {
    [REGISTER]({ getters, commit }, {userToCreate, actions}) {
      let url = `${API_URL}/api/v1/account/`;

      return axios.post(url, userToCreate, {
          headers: authHeader(getters.userProfile.access)
        })
        .then(function (response) {
          commit(ADD_NEW_USER, response.data);
          return response.data;
        })
        .catch(function (error) {
          ServerErrorHandler(actions, error.response);
          throw new Error("");
        });
    },

    [LOGOUT]({ commit }, ability) {
      commit(SET_USER, {});
      ability.update([]);
    },

    [UPDATE_USER]({ getters, commit }, {userToUpdate, actions}) {
      let url = `${API_URL}/api/v1/account/${userToUpdate.id}/`;

      return axios.patch(url, userToUpdate, {
          headers: authHeader(getters.userProfile.access)
        })
        .then(function (response) {
          commit(EDIT_USER_FROM_LIST, response.data);
          return response.data;
        })
        .catch(function (error) {
          ServerErrorHandler(actions, error.response);
          throw new Error("");
        });
    },

    [LOGIN]({ commit }, {values, actions, ability}) {
      let getTokenURL = `${API_URL}/api/v1/token/`;
      var userData = {}

      return axios.post(getTokenURL, values)
        .then(function (response) {
          userData = response.data;
          let getUserUrl = `${API_URL}/api/v1/account/${userData.id}/`;
          return axios.get(getUserUrl, {
            headers: authHeader(userData.access)
          })
        })
        .then(function (response) {
          userData = Object.assign(userData, response.data);
          commit(SET_USER, userData);
          ability.update(defineRulesFor(userData));
        })
        .catch(function (error) {
          commit(SET_USER, {});
          ServerErrorHandler(actions, error.response);
          ability.update([]);
          throw new Error("");
        });
    },

    [LIST_USERS]({ commit, getters }, params) {
      let url = `${API_URL}/api/v1/account/`;

      return axios.get(url, {
        params,
        headers: authHeader(getters.userProfile.access)
      })
        .then(function (response) {
          commit(SET_USERS_LIST, response.data);
          return response.data;
        })
    },

    [DEACTIVATE_USER]({ commit, getters }, userId) {
      let url = `${API_URL}/api/v1/account/${userId}/deactivate/`;
      return axios.delete(url, {
        headers: authHeader(getters.userProfile.access)
      })
        .then(function (response) {
          commit(EDIT_USER_FROM_LIST, response.data);
          return response.data;
        })
    },

    [FULL_DELETE_USER]({ getters, commit }, userId) {
      let url = `${API_URL}/api/v1/account/${userId}/`;

      return axios.delete(url, {
          headers: authHeader(getters.userProfile.access)
        })
        .then(function () {
          commit(REMOVE_USER_FROM_LIST, userId);
        })
        .catch(function () { throw new Error("") });
    },

    [CHANGE_OWN_PASSWORD]({ getters }, { values, actions, userId }) {
      let url = `${API_URL}/api/v1/account/${userId}/password/`;

      return axios.put(url, values, {
          headers: authHeader(getters.userProfile.access)
        })
        .then(function (response) { return response.data })
        .catch(function (error) {
          ServerErrorHandler(actions, error.response);
          throw new Error("");
        });
    },
  };

  const mutations = {
    [SET_USER](state, user) {
      state.userProfile = user;
      saveUserProfile(state.userProfile);
    },
    [SET_USERS_LIST](state, usersList) {
      state.usersList = usersList;
    },
    [ADD_NEW_USER](state, user) {
      state.usersList.push(user);
    },
    [EDIT_USER_FROM_LIST](state, editedUser) {
      let idx = state.usersList.findIndex((u) => u.id == editedUser.id);

      if (idx > -1) {
        state.usersList[idx] = editedUser;
      }
    },
    [REMOVE_USER_FROM_LIST](state, userId) {
      let idx = state.usersList.findIndex((u) => u.id == userId);

      if (idx > -1) {
        state.usersList.splice(idx, 1);
      }
    }
  };

  const getters = {
    userProfile(state) {
      return state.userProfile;
    },
    usersList(state) {
      return state.usersList;
    }
  };

  export default {
    namespaced: true,
    state,
    actions,
    mutations,
    getters
  };
