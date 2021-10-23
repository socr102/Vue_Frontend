<template>
  <div>
    <h4 class="header-title mt-0">
      {{title}}
    </h4>

    <div class="tab-content">
      <apexchart
          type="bar"
          :options="graphOptions"
          :series="graphSeries"
      ></apexchart>
    </div>
  </div>
</template>


<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: 'TopItems',
  props: {
    title: String,
    graphTooltip: String,
    callback: Function,
    dataParam: String,
    sortParam: String,
    dateRange: Object
  },
  components: {
    apexchart: VueApexCharts,
  },
  mounted() {
    this.onDateChange()
  },
  watch: {
    dateRange: {
      handler: function() {
        this.onDateChange()
      },
      deep: true
    },
  },
  methods: {
    getAttr(path, obj) {
      return path.split('.').reduce((p,c)=>p&&p[c]||0, obj);
    },
    onDateChange() {
      let params = {...this.apiParams, ...this.dateRange};

      this.callback({params: params, persist: true}).then(res => {
        this.graphSeries = [{
          name: this.graphTooltip,
          data: res.results.map(i => this.getAttr(this.dataParam, i).toFixed(0))
        }]

        this.graphOptions = this.getChartOptions(res.results);
      });
    },

    getChartOptions(items) {
      return {
        plotOptions: { bar: { horizontal: true } },
        dataLabels: { enabled: false },
        xaxis: {
          categories: items.map(i => {
            if (!i.number) return i.name;
            return `${i.name}(${i.number})`;
          }),
          labels: { show: false}
        }
      }
    },
  },
  data() {
    return {
        graphOptions: {},
        graphSeries: [],
        apiParams: {order: this.sortParam, limit: 10},
    }
  },
}
</script>
