<template>
  <div>
    <h4 class="header-title mt-0" >
      {{title}}
      <select v-model="trendType"
              style="float: right;"
              v-on:change="onChange">
        <option value="up">Up</option>
        <option value="down">Down</option>
      </select>
      <button type="button" class="btn btn-outline-info" data-toggle="tooltip" data-html="true"
        :title="tooltipNote">
        Info
      </button>
    </h4>

    <div class="tab-content table-responsive">
      <table class="table">
        <thead>
        <tr>
            <th scope="col">Name</th>
            <th scope="col">Change</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(item,i) in items" :key="i">
            <th scope="row">
              {{item.name}}
              <span v-if="item.number">({{item.number}})</span>
            </th>
            <td><span v-bind:class="badgeType(item[dataParam])"
                      class="badge trendDiff">{{item[dataParam]}}%
                </span>
            </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TopItems',
  props: {
    title: String,
    callback: Function,
    dataParam: String,
    dateRange: Object
  },
  mounted() {
    this.onChange();
    window.$('[data-toggle="tooltip"]').tooltip()
  },
  watch: {
    dateRange: {
      handler: function() {
        this.onChange()
      },
      deep: true
    },
  },
  methods: {
    badgeType(value) {
      if (value >= 0) return "bg-success";
      return "bg-danger";
    },

    onChange() {
      let options = {
        direction: this.trendType,
        params: this.dateRange
      }
      this.callback(options).then(res => {
        this.items = res;
      });
    }
  },
  data() {
    return {
        tooltipNote: `Splits selected time range to 2 equal parts. Compare items sold in first period to the second period.`,
        trendType: 'up',
        items: []
    }
  },
}
</script>

<style>
.trendDiff {
  color:aliceblue;
  font-weight: bold;
}
</style>
