import { createStore, createLogger } from 'vuex';

import user from "@/User/user.store";
import member from "@/Members/member.store";
import audience from "@/Audience/audience.store";
import article from "@/Articles/article.store";
import _store from "@/Stores/store.store";
import product from "@/Products/product.store";
import metrics from "@/Dashboard/metrics.store";
import org from "@/Orgs/org.store";
import campaign from "@/Campaigns/campaign.store";
import offer from "@/Offers/offer.store";
import receipt from "@/Receipts/receipt.store";

import {isDebugMode} from '@/Core/helpers/utils';

export const store = createStore({
  modules: {
    receipt,
    member,
    audience,
    offer,
    campaign,
    user,
    org,
    article,
    _store,
    product,
    metrics
  },
  strict: isDebugMode(),
  plugins: isDebugMode() ? [createLogger()] : []
});
