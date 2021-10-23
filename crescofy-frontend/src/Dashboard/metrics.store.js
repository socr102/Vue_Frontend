
import { GET_METRICS } from '@/Core/store/action-types';

import offerApi from '@/Offers/offer.api';
import orderApi from '@/Orders/order.api';
import campaignApi from '@/Campaigns/campaign.api';
import storeApi from '@/Stores/store.api';
import paymentApi from '@/Payments/payment.api';

const initialState = {};
const state = {...initialState};

const actions = {
  async [GET_METRICS]({rootState}, params) {
    let options = [rootState.user.userProfile.access, params];
    const [store, payment, order, campaign, offer] = await Promise.all([
      storeApi.metrics(...options),
      paymentApi.metrics(...options),
      orderApi.metrics(...options),
      campaignApi.metrics(...options),
      offerApi.metrics(...options),
    ]);
    return {
      totalStores: store.headers['x-total-count'],
      totalEarnings: payment.headers['x-total-price'],
      totalOrders: order.headers['x-total-count'],
      totalCompaigns: campaign.headers['x-total-count'],
      totalOffers: offer.headers['x-total-count']
    };
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
