<template>
<div class="page-wrapper">
    <!-- Page Content-->
    <div class="page-content-tab">
        <div class="container">
            <div class="row">
                <div class="col-md-8">
                    <div class="page-title-box">
                        <h4 class="page-title">Dashboard</h4>
                    </div><!--end page-title-box-->
                </div><!--end col-->
                <div class="col-md-4">
                    <div class="page-title-box">
                      <input type="text" ref="date" class="form-control page-title"/>
                    </div><!--end page-title-box-->
                </div><!--end col-->
            </div>
            <div class="row">
              <div class="col">
                  <div class="card report-card">
                      <div class="card-body text-center">
                          <div class="report-main-icon bg-light-alt mx-auto">
                              <i class="las la-receipt text-primary font-30"></i>
                          </div>
                          <h4 class="font-22 font-weight-semibold">{{generalMetrics.totalOrders}}</h4>
                          <p class="text-muted mb-1 font-weight-normal font-13">Orders</p>
                      </div><!--end card-body-->
                  </div><!--end card-->
              </div><!-- end col-->
              <div class="col">
                  <div class="card report-card">
                      <div class="card-body text-center">
                          <div class="report-main-icon bg-light-alt mx-auto">
                              <i class="las la-store text-primary font-30"></i>
                          </div>
                          <h4 class="font-22 font-weight-semibold">{{generalMetrics.totalStores}}</h4>
                          <p class="text-muted mb-1 font-weight-normal font-13">Stores</p>
                      </div><!--end card-body-->
                  </div><!--end card-->
              </div><!-- end col-->
              <div class="col">
                  <div class="card report-card">
                      <div class="card-body text-center">
                          <div class="report-main-icon bg-light-alt mx-auto">
                              <i class="las la-ad text-primary font-30"></i>
                          </div>
                          <h4 class="font-22 font-weight-semibold">{{generalMetrics.totalCompaigns}}</h4>
                          <p class="text-muted mb-1 font-weight-normal font-13">Campaigns</p>
                      </div><!--end card-body-->
                  </div><!--end card-->
              </div><!-- end col-->
              <div class="col">
                  <div class="card report-card">
                      <div class="card-body text-center">
                          <div class="report-main-icon bg-light-alt mx-auto">
                              <i class="las la-hand-holding-usd text-primary font-30"></i>
                          </div>
                          <h4 class="font-22 font-weight-semibold">{{generalMetrics.totalEarnings}}</h4>
                          <p class="text-muted mb-1 font-weight-normal font-13">Earnings</p>
                      </div><!--end card-body-->
                  </div><!--end card-->
              </div><!-- end col-->
            <div class="col">
                  <div class="card report-card">
                      <div class="card-body text-center">
                          <div class="report-main-icon bg-light-alt mx-auto">
                              <i class="las la-gift text-primary font-30"></i>
                          </div>
                          <h4 class="font-22 font-weight-semibold">{{generalMetrics.totalOffers}}</h4>
                          <p class="text-muted mb-1 font-weight-normal font-13">Offers</p>
                      </div><!--end card-body-->
                  </div><!--end card-->
              </div><!-- end col-->
            </div>
            <div class="row">
                <div class="col-lg-4">
                  <div class="card">
                    <div class="card-body">
                      <top-items
                      title="Top selling stores"
                      dataParam="revenue"
                      sortParam="-revenue"
                      graphTooltip="Store revenue"
                      :dateRange="dateFilterParams"
                      :callback="LIST_STORES"
                        />
                    </div>
                  </div>
                </div>
                <div class="col-lg-4">
                  <div class="card">
                    <div class="card-body">
                      <top-items
                      title="Top performing campaigns"
                      dataParam="metadata.revenue"
                      sortParam="-revenue"
                      graphTooltip="Revenue"
                      :dateRange="dateFilterParams"
                      :callback="LIST_CAMPAIGNS"
                      />
                    </div>
                  </div>
                </div>
                <div class="col-lg-4">
                  <trending-items
                    title="Trending Articles"
                    dataParam="diff"
                    :dateRange="dateFilterParams"
                    :callback="TRENDING_ARTICLES"
                    />
                </div>
            </div>
            <div class="row">
                <div class="col-lg-4">
                  <div class="card">
                    <div class="card-body">
                      <top-items
                      title="Top selling articles"
                      dataParam="sold_items"
                      sortParam="-sold_items"
                      graphTooltip="Items sold"
                      :dateRange="dateFilterParams"
                      :callback="LIST_ARTICLES"
                        />
                    </div>
                  </div>
                </div>
                <div class="col-lg-4">
                  <div class="card">
                    <div class="card-body">
                      <top-items
                      title="Top selling products"
                      dataParam="sold_items"
                      sortParam="-sold_items"
                      graphTooltip="Items sold"
                      :dateRange="dateFilterParams"
                      :callback="LIST_PRODUCTS"
                      />
                    </div>
                  </div>
                </div>
                <div class="col-lg-4">
                  <trending-items
                    title="Trending Products"
                    dataParam="diff"
                    :dateRange="dateFilterParams"
                    :callback="TRENDING_PRODUCTS"
                    />
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import { mapActions } from 'vuex';

import { LIST_ARTICLES,
         LIST_STORES,
         LIST_PRODUCTS,
         LIST_CAMPAIGNS,
         TRENDING_ARTICLES,
         TRENDING_PRODUCTS,
         GET_METRICS } from '@/Core/store/action-types';

import TopItems from './components/TopItems.vue';
import TrendingItems from './components/TrendingItems.vue';
import { DATE_FORMAT } from '@/Core/helpers/utils';

export default {
  name: 'Dashboard',
  components: {
    TopItems,
    TrendingItems
  },
  methods: {
    ...mapActions('article', [LIST_ARTICLES, TRENDING_ARTICLES]),
    ...mapActions('product', [LIST_PRODUCTS, TRENDING_PRODUCTS]),
    ...mapActions('_store', [LIST_STORES]),
    ...mapActions('metrics', [GET_METRICS]),
    ...mapActions('campaign', [LIST_CAMPAIGNS]),

    barChartOptions(items) {
      return {
        plotOptions: { bar: { horizontal: true } },
        dataLabels: { enabled: false },
        xaxis: {
          categories: items.map(i => i.name),
          labels: { show: false}
        }
      }
    },

    onDateChange(start, end) {
      this.dateFilterParams = {
        date_after: start.format(DATE_FORMAT),
        date_before: end.format(DATE_FORMAT)
      }
      this.initMetrics();
    },

    initMetrics() {
      this[GET_METRICS](this.dateFilterParams).then(res => {
        this.generalMetrics = res;
      });
    }
  },
  created() {
    this.initDateRange = [
      this.predefindedDates['This Year'][0],
      this.predefindedDates['This Year'][1]
    ]
    this.onDateChange(this.initDateRange[0], this.initDateRange[1]);
  },
  mounted() {
    window.$(this.$refs.date).daterangepicker({
      startDate: this.initDateRange[0],
      endDate: this.initDateRange[1],
      ranges: this.predefindedDates
    }, this.onDateChange);

    this.initMetrics();
  },
  data: function() {
    return {
      dateFilterParams: {},
      generalMetrics: {},
      predefindedDates: {
        'Yesterday': [window.moment().subtract(1, 'days'), window.moment()],
        'Last 7 Days': [window.moment().subtract(6, 'days'), window.moment()],
        'Last 30 Days': [window.moment().subtract(29, 'days'), window.moment()],
        'This Month': [window.moment().startOf('month'), window.moment().endOf('month')],
        'This Year': [window.moment().startOf('year'),
                      window.moment().endOf('year')]
      }
    };
  },
}
</script>
