import { mapGetters, mapActions } from 'vuex';

import { LIST_MEMBERS } from '@/Core/store/action-types';

export default {
  computed: {
    ...mapGetters('member', ["membersList"]),
    ...mapGetters('user', ["userProfile"])
  },
  methods: {
    ...mapActions('member', [LIST_MEMBERS]),

    gridFields() {
      return [
        { name: "name", type: "text", width: "auto", sorting: true,
          title: "Name", autosearch: true },
        { name: "sex", type: "number", width: "auto", title: "Sex", filtering: false},
        { name: "phone", type: "number", width: "auto", title: "Phone", filtering: false},
        { name: "birth_date", type: "number", width: "auto", title: "Birth", filtering: false},
        { name: "id", type: "number", visible: false, width: "auto" },
      ]
    },
    /**
     * Load members from server and apply filters
     */
    loadMembers(filter) {
      let params = {};
      if (filter.name) params.q = filter.name;
      if (filter.is_active !== undefined )
        params.is_active = filter.is_active;
      if (filter.pageIndex !== undefined ) {
        params.limit = filter.pageSize;
        params.offset = filter.pageSize * (filter.pageIndex - 1);
      }

      return this[LIST_MEMBERS]({persist: true, params}).then(resp => {
        return {data: resp.results, itemsCount: resp.count};
      });
    },

    gridOptions() {
      return {
        height: "90%",
        width: "100%",
        autoload: true,
        paging: true,
        heading: true,
        editing: false,
        pageSize: 5,
        confirmDeleting: false,
        pageLoading: true,
        fields: this.getGridFields(),
        controller: {loadData: this.loadMembers}
      }
    }
  },
  watch: {
    membersList: {
      handler: function() {
        this.grid.jsGrid("option", "data", this.membersList);
      },
      deep: true
    },
  },
  data() {
    return {}
  }
}
