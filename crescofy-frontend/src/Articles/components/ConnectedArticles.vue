<template>
<div :id="connectedItemsId"></div>
</template>

<script>
import { mapActions } from 'vuex';

import { CONNECTED_ARTICLES } from '@/Core/store/action-types';

export default {
  name: 'ConnectedArticles',

  props: {
    productIds: {
      required: true,
      type: Array
    },
  },

  mounted() {
    this.initGrid();
  },
  methods: {
    ...mapActions('article', [CONNECTED_ARTICLES]),

    createSpanTag() {
      return window.$("<span>")
        .attr({class: 'rounded-pill badge larg-badge'});
    },

    initGrid() {
      this.grid = window.$(`#${this.connectedItemsId}`).jsGrid({
        height: "90%",
        width: "100%",
        autoload: true,
        paging: true,
        pageSize: 15,
        data: [],
        fields: [
          { name: "articles", type: "text", width: "auto",
            sorting: true, title: "Articles", autosearch: true,
            itemTemplate: (articles) => {
              return articles.map(a => {
                return this.createSpanTag().text(a.name);
              })
            }
          },
          { name: "categories", type: "text", width: "auto",
            sorting: true, title: "Categories", autosearch: true,
            itemTemplate: (c, item) => {
              let uniqueProducts = new Set(item.articles.map(a => a.product));
              return [...uniqueProducts].map(prod => {
                return this.createSpanTag().text(prod);
              })
            }
          },
          { name: "correlation", type: "number",
            title: "Connection in %", width: "auto",
            itemTemplate: (val) => Math.round(val)
          },
          { name: "recommended", type: "text",
            title: "Recommended articles", width: "auto",
            itemTemplate: (reccomendations) => {
              return reccomendations.map(a => {
                return this.createSpanTag().text(a.reccomendations);
              })
            }
          },
          
        ],
      });
    },
  },

  watch: {
    productIds: {
      handler: function() {
        if (this.productIds.length == 0) return;
        this[CONNECTED_ARTICLES](this.productIds).then(data => {
          console.log("test");
          console.log(data);
          this.grid.jsGrid("option", "data", data);
        })
      },
      deep: true
    }
  },

  data() {
    return {
      connectedItemsId: 'connectedArticlesGrid'
    }
  }
}
</script>

<style src='../../../public/assets/css/new_all.css'>
/*.larg-badge {
    font-size: 1.2em !important;
    font-weight: bold;
    display: inline;
}

.larg-badge:after {
    content:"\a";
    white-space: pre;
}*/
</style>
