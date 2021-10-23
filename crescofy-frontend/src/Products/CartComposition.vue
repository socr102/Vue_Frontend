<template>
<div class="page-wrapper">
    <!-- Page Content-->
    <div class="page-content-tab">
        <div class="container">
            <div class="row">
                <div class="col-sm-12">
                    <div class="page-title-box">
                        <h4 class="page-title">Cart Composition</h4>
                    </div><!--end page-title-box-->
                </div><!--end col-->
            </div>

            <div class="row">
              <div class="col-lg-12">
                  <h4>Connected Categories</h4>
                  <div class="card report-card">
                      <div :id="connectedItemsId"></div>
                  </div>
              </div>
            </div>

            <div class="row">
              <div class="col-lg-12">
                  <h4>Categories Recommendations</h4>
              </div>
            </div>
            <rec
              v-if="productsList"
              v-model="selected_products"
              :endpoint="RECOMMENDED_PRODUCTS"
              :gridFields="gridFields"
              :fetchRecords="LIST_PRODUCTS"
              :initOptions="productsList"
              v-on:search="productIds = $event"
              selectPlaceholder="Choose categories to analyze"
            />

            <div class="row">
              <div class="col-lg-12">
                <h4>Connected Articles</h4>
                <div class="card report-card">
                    <ConnectedArticles :productIds="productIds"/>
                </div>
              </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

import Rec from './components/Recommendations';
import ConnectedArticles from '@/Articles/components/ConnectedArticles';

import { LIST_PRODUCTS,
         RECOMMENDED_PRODUCTS,
         CONNECTED_PRODUCTS }
from '@/Core/store/action-types';

export default {
  name: 'CartComposition',
  components: { Rec, ConnectedArticles },
  computed: {
    ...mapGetters('product', ['productsList', 'getProdById'])
  },
  mounted() {
    this[LIST_PRODUCTS]({persist: true}).then(() => {
      this.initGrid();
    });
  },
  methods: {
    ...mapActions('product', [LIST_PRODUCTS, RECOMMENDED_PRODUCTS, CONNECTED_PRODUCTS]),

    initGrid() {
      this.grid = window.$(`#${this.connectedItemsId}`).jsGrid({
        height: "90%",
        width: "100%",
        autoload: true,
        paging: true,
        pageSize: 7,
        fields: [
          { name: "product_ids", type: "text", width: "auto",
            sorting: true, title: "Products List", autosearch: true,
            itemTemplate: (ids) => {
              return ids.map(i => {
                return window.$("<span>")
                  .attr({class: 'rounded-pill badge larg-badge'})
                  .text(this.getProdById(i).name);
              })
            }
          },
          { name: "correlation", type: "number",
            title: "Products Connection in %", width: "auto",
            itemTemplate: (val) => Math.round(val)
          },
          { type: "control", width: "auto", editButton: false,
            deleteButton: false, title: "Select items",
            itemTemplate: (value, item) => {
              let $switchBtn = window.$("<button>").attr({class: 'jsgrid-button jsgrid-search-button'})
                .click((e) => {
                  this.selected_products = item.product_ids;
                  e.stopPropagation();
                });

              return window.$("<div>").append($switchBtn);
            }
          }
        ],
        controller: {
          loadData: () => this[CONNECTED_PRODUCTS]()
        },
      });
    },
  },

  data() {
    return {
      connectedItemsId: 'connectedItemsGrid',
      selected_products: [],
      productIds: [], // using for Article Connected component
      gridFields: [
        { name: "name", type: "text", width: "auto", sorting: true,
          title: "Recommended category", autosearch: true },
        { name: "number", type: "text", width: "auto", sorting: true,
          title: "Product Number", autosearch: true },
        { name: "percent", type: "number", title: "% with given products", width: "auto",
          itemTemplate: (val) => Math.round(val)
        },
        { name: "avg_order_value", type: "number", width: "auto",
          title: "Avg order price with product",
          itemTemplate: (val) => val ? parseInt(val) : ""
        },
        { name: "recs", type: "text", width: "auto", title: "Recommendations", },
      ]
    }
  }
}
</script>

<style>
.larg-badge {
    font-size: 1.2em !important;
    font-weight: bold;
}
</style>