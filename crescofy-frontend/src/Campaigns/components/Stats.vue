<template>
<div class="modal fade" :id="modalId" tabindex="-1" role="dialog" aria-labelledby="{{modalId}}" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" :id="modalId">{{header_text}}</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
          <div class="table-responsive">
            <table class="table border-dashed mb-0">
              <tbody>
              <tr>
                  <th class="border-top-0 text-dark" scope="row">
                    <i class="far fa-money-bill-alt text-primary font-24 mr-2 align-middle"></i>Revenue
                  </th>
                  <td class="border-top-0 text-right">{{getRevenue()}}</td>
              </tr>
              <tr>
                  <th class="text-dark" scope="row">
                    <i class="far fa-smile text-primary font-24 mr-2 align-middle"></i>% of Members that participated
                  </th>
                  <td class="text-right">{{getParticipatedPerc()}}%</td>
              </tr>
              <tr>
                  <th class="text-dark" scope="row">
                    <i class="far fa-user text-primary font-24 mr-2 align-middle"></i>Number of Members that participated
                  </th>
                  <td class="text-right">{{getParticipatedNumber()}}</td>
              </tr>
              <tr>
                  <th class="text-dark" scope="row">
                    <i class="far fa-address-book text-primary font-24 mr-2 align-middle"></i>Campaign Audince size
                  </th>
                  <td class="text-right">{{getAudienceSize()}}</td>
              </tr>
              </tbody>
            </table>
          </div>
      </div>
			<div class="modal-footer">
				<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
			</div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'CampaignStats',
  props: {
    modalId: {
      required: true,
      type: String,
    },
    metadata: {
      required: false,
      type: Object,
    },
  },
  methods: {
    isMetaEmpty() {
      if (!this.metadata) return true;
      if(Object.entries(this.metadata).length === 0) return true;
      return false;
    },
    getRevenue() {
      return this.isMetaEmpty() ? 0: this.metadata.revenue.toFixed(2);
    },
    getParticipatedPerc() {
      if (this.isMetaEmpty()) return 0;
      return (this.metadata.members_participated /
              this.metadata.campaign_members).toFixed(2) * 100;
    },
    getParticipatedNumber() {
      return this.isMetaEmpty() ? 0: this.metadata.members_participated;
    },
    getAudienceSize() {
      return this.isMetaEmpty() ? 0: this.metadata.campaign_members;
    }
  },
  data() {
      return {
          header_text: "Campaign Statistics"
      }
  }
}
</script>
