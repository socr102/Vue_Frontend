<template>
<div class="page-wrapper">
    <!-- Page Content-->
    <div class="page-content-tab">
        <div class="container">
            <div class="row">
                <div class="col-sm-12">
                    <div class="page-title-box">
                        <h4 class="page-title">Article Analytics</h4>
                    </div><!--end page-title-box-->
                </div><!--end col-->
            </div>
            <rec
              v-model="selected_articles"
              valueProp="id"
              :endpoint="RECOMMENDED_ARTICLES"
              :gridFields="gridFields"
              :fetchRecords="LIST_ARTICLES"
              selectPlaceholder="Choose articles to analyze"
            />
        </div>
    </div>
</div>
</template>

<script>
import { mapActions } from 'vuex';

import Rec from '@/Products/components/Recommendations'
import { LIST_ARTICLES, RECOMMENDED_ARTICLES } from '@/Core/store/action-types';

export default {
  name: 'ArticleAnalysis',
  components: { Rec },
  mixins: [],

  methods: {
    ...mapActions('article', [LIST_ARTICLES, RECOMMENDED_ARTICLES]),
  },

  data() {
    return {
      selected_articles: [],
      gridFields: [
        { name: "name", type: "text", width: "auto", sorting: true,
          title: "Recommended article", autosearch: true },
        { name: "percent", type: "number", title: "% with given articles", width: "auto",
          itemTemplate: (val) => Math.round(val)
        },
        { name: "avg_order_value", type: "number", width: "auto",
          title: "Avg order price with article",
          itemTemplate: (val) => val ? parseInt(val) : ""
        },
        { name: "recs", type: "text", width: "auto", title: "Recommendations", },
      ]
    }
  }
}
</script>
