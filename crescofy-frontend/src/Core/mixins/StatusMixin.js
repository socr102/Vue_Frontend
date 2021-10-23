export default {
  methods: {
    getStatusFilterProps(filter) {
      let params = {};
      switch (filter.status) {
        case 1:
          params.is_active = 0;
          params.is_archive = 0;
          break;
        case 2:
          params.is_active = 1;
          break;
        case 3:
          params.is_archive = 1;
          break;
      }
      return params;
    },

    getStatusIcon(item) {
      let status = {};
      if (item.is_active) {
        status.text = this.statusList[2];
        status.icon = 'dripicons-pulse';
      }
      else if (item.is_archive) {
        status.text = this.statusList[3];
        status.icon = 'dripicons-trash';
      }
      else {
        status.text = this.statusList[1];
        status.icon = 'dripicons-clock';
      }
      return `<span><i class="${status.icon} text-muted` +
        ` mr-2"></i>${status.text}</span>`;
    }
  },
  data() {
    return {
      statusList: ["ALL", "Pending", "Active", "Expired"],
    }
  }
}
