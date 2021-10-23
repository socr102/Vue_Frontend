import {
    LIST_ARTICLES,
    TRENDING_ARTICLES,
    RECOMMENDED_ARTICLES,
    CONNECTED_ARTICLES
} from '@/Core/store/action-types';

import { SET_ARTICLES_LIST } from '@/Core/store/mutation-types';
import api from './article.api';

const initialState = {};
const state = {...initialState };

const actions = {
    async [LIST_ARTICLES]({ rootState, commit }, { params, persist }) {
        let response = await api.get(rootState.user.userProfile.access, params);
        if (persist == true)
            commit(SET_ARTICLES_LIST, response.data);
        return response.data;
    },

    async [TRENDING_ARTICLES]({ rootState }, { direction, params }) {
        let response = await api.trend(rootState.user.userProfile.access,
            direction, params);
        return response.data;
    },

    async [RECOMMENDED_ARTICLES]({ rootState }, article_ids) {
        let response = await api.recommendations(rootState.user.userProfile.access,
            article_ids);
        return response.data;
    },
    async [CONNECTED_ARTICLES]({ rootState }, product_ids) {
        let response = await api.connected(rootState.user.userProfile.access,
            product_ids)
        return response.data;
    },
};

const mutations = {
    [SET_ARTICLES_LIST](state, articlesList) {
        if (!Array.isArray(articlesList)) {
            articlesList = articlesList.results;
        }

        state.articlesList = articlesList.map(v => {
            // vueform/multiselect require value prop
            v.value = v.id;
            return v;
        });
    },
};
const getters = {
    articlesList(state) {
        return state.articlesList;
    },
    getArticleById: (state) => (id) => {
        return state.articlesList.find(article => article.id === id);
    }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations,
    getters
};