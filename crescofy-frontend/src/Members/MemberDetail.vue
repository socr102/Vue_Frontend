<template>
<div class="page-wrapper">
  <div class="page-content-tab">
    <div class="container">
      <div class="row">
        <div class="col-sm-6">
          <div class="page-title-box">
            <h4 class="mt-0 header-title">Member Purchases</h4>
            <MemberPurchase/>
          </div>
        </div>
        <div class="col-sm-6">
          <div class="page-title-box">
            <h4 class="mt-0 header-title">Member Campaigns</h4>
            <MemberCampaigns/>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import MemberPurchase from './components/MemberPurchase';
import MemberCampaigns from './components/MemberCampaigns';

export default {
  name: 'MemberDetail',
  components: { MemberPurchase, MemberCampaigns },
}
</script>
