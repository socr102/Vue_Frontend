<template>
  <div>
      <div ref="grid"></div>
      <ReceiptDetail :orders="campaignOrders" :modalId="modalId"/>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

import { LIST_MEMBER_CAMPAIGNS, LIST_MEMBER_CAMPAIGN_ORDERS } from '@/Core/store/action-types';
import ReceiptDetail from './ReceiptDetail';
import '@/Core/helpers/DateRangeField';

export default {
  name: 'MemberCampaignsGrid',
  components: {ReceiptDetail},
  methods: {
    ...mapActions('member', [LIST_MEMBER_CAMPAIGN_ORDERS, LIST_MEMBER_CAMPAIGNS]),

    getControlField() {
      return { type: "control", width: "auto", editButton: false,
        deleteButton: false, title: "Detail view",
        itemTemplate: (value, item) => {
          let $detailBtn = window.$("<button>")
            .attr({class: 'jsgrid-button jsgrid-search-button'})
            .click((e) => {
              this[LIST_MEMBER_CAMPAIGN_ORDERS]({objId: this.$route.params.memberId,
                                                 campaignId: item.id}).then(data => {
                // open detail modal window
                this.campaignOrders = data;
                window.$(`#${this.modalId}`).modal('toggle');
              })

              e.stopPropagation();
            });

          return window.$("<div>").append($detailBtn);
        }
      }
    },

    getGridFields() {
      return [
        { name: "name", type: "text", width: "auto", sorting: true,
          title: "Campaign name", autosearch: true},
        { name: "offer.name", type: "text", width: "auto", sorting: true,
          title: "Offer name", autosearch: true},
        { name: "audience.name", type: "text", width: "auto", sorting: true,
          title: "Audience name", autosearch: true},
        { name: "id", type: "number", width: "auto", filtering: false },
        this.getControlField()
      ]
    },

    loadPurchase() {
      let params = {order: '-end_date'};

      return this[LIST_MEMBER_CAMPAIGNS]({
        params,
        objId: this.$route.params.memberId
      });
    }
  },

  mounted() {
    this.grid = window.$(this.$refs.grid).jsGrid({
      height: "90%",
      width: "100%",
      autoload: true,
      paging: true,
      editing: false,
      pageSize: 15,
      confirmDeleting: false,
      controller: {
        loadData: this.loadPurchase
      },
      fields: this.getGridFields(),
    });
  },

  data() {
    return {
      campaignOrders: [],
      modalId: 'campaignOrderDetails'
    }
  }
}
</script>
