<template>
  <div>
    <RegistrationModal v-bind:modalId="createModalId"/>
    <EditUserModal v-bind:modalId="editModalId" v-bind:userToEdit="editedResource"/>
    <div :id='adminPanelId'></div>
  </div>
</template>


<script>
import { mapGetters, mapActions } from 'vuex';
import { subject } from '@casl/ability';

import { LIST_USERS, DEACTIVATE_USER, FULL_DELETE_USER, LIST_ORGS } from '@/Core/store/action-types';
import { UserRoleMixin, MERCHANT, ADMIN, SUPER_ADMIN, WORKER } from '@/Core/mixins/UserRoleMixin';
import { controlField, onDeleteItem } from '@/Core/helpers/gridUtils';
import GlobalGridMixin from '@/Core/mixins/GlobalGridMixin';
import { RESOURCE_NAME } from '../user.vars';
import RegistrationModal from './RegistrationModal';
import EditUserModal from './EditUserModal';

export default {
  name: 'AdminGrid',
  components: {
    RegistrationModal,
    EditUserModal
  },
  computed: {
    ...mapGetters('user', ['userProfile', 'usersList']),
    ...mapGetters('org', ['orgsList', "getOrgById"])
  },
  mixins: [UserRoleMixin, GlobalGridMixin],
  methods: {
    ...mapActions('user', [LIST_USERS, DEACTIVATE_USER, FULL_DELETE_USER]),
    ...mapActions('org', [LIST_ORGS]),

    getGridFields() {
      var showDetailsDialog = () => {
        window.$(`#${this.createModalId}`).modal('toggle');
      };

      return [
        { name: "email", type: "text", width: "auto", title: "Email" },
        { name: "id", type: "number", visible: false, width: "auto" },
        { type: "select", title: "Role", width: "auto", name: 'role',
          items: this.userRolesFilter, autosearch: true,
          itemTemplate: (val, item) => {
            return `${this.getUserRole(item)}`;
          },
        },
        { name: "organization", type: "select",
          title: "Organization", width: "auto",
          items: this.orgsFilter, autosearch: true,
          valueField: "id", textField: "name",
          itemTemplate: (val, item) => {
            if (item.organization === null) return "";
            let org = this.getOrgById(item.organization);
            if (org) return org.name;
          }},
        { name: "created_by.email", type: "text", width: "auto", title: "Created by" },
        { name: "is_active", type: "checkbox", title: "Active", width: "auto"},
        {
          name: "delete_request",
          type: "checkbox",
          title: "Pending Delete",
          width: "auto",
          itemTemplate: (val) => {
            let isChecked = val === undefined || val === null ? '' : 'checked=checked';
            return `<input type="checkbox" disabled ${isChecked}>`
          }
        },
        controlField(showDetailsDialog, `Register new ${RESOURCE_NAME}`)
      ]
    },

    deactivateUser(item) {
      let hasPermission = this.$ability.can('deactivate',
                                            subject(RESOURCE_NAME, item));
      if (!hasPermission) {
        this.$alertify.notify('Action Forbidden!', 'error', 3);
      } else {
        let confirmMsg = `This action will deactivate ${item.email} ${RESOURCE_NAME}. Are you sure?`;
        this.$alertify.confirm(
          'Please Confirm Your Action',
          confirmMsg,
          () => {
            let successMsg = `${RESOURCE_NAME} successfully deactivated.`;
            var errorMsg = 'Action Forbidden!';
            this[DEACTIVATE_USER](item.id)
              .then(() => this.$alertify.notify(successMsg, 'success', 3))
              .catch(() => this.$alertify.notify(errorMsg, 'error', 3))
          },
          () => {}
        );
      }
    },

    onDelete(args) {
      if (this.getUserRole(args.item) == MERCHANT.name) {
        // perform deactivation
        this.deactivateUser(args.item);
      } else {
        // perform deletion
        onDeleteItem(this.$alertify, this.$ability,
                     this[FULL_DELETE_USER], RESOURCE_NAME, 'email')(args)
      }

      // cancel default deletion to prevent vue state error
      args.cancel = true;
    },

    gridFilter(filter) {
      let params = {};
      if (filter.organization != -1) {
        params['organization'] = filter.organization;
      }
      switch (filter.role) {
        case 1:
          params['merchant'] = 1;
          break;
        case 2:
          params['worker'] = 1;
          break;
        case 3:
          params['superadmin'] = 0;
          params['admin'] = 1;
          break;
        case 4:
          params['superadmin'] = 1;
          params['admin'] = 1;
          break;
      }

      return this[LIST_USERS](params);
    }
  },
  mounted() {
    this[LIST_ORGS]()
      .then(orgs => this.orgsFilter.push(...orgs))
      // merchants doesn't have access to organizations
      .catch(() => this.userRolesFilter = ["ALL"])
      .then(() => {
        this.grid = window.$(`#${this.adminPanelId}`).jsGrid({
          height: "90%",
          width: "100%",
          autoload: true,
          sorting: true,
          paging: true,
          heading: true,
          editing: false,
          filtering: true,
          pageSize: 15,
          loadIndicationDelay: 250,
          confirmDeleting: false,
          data: this[LIST_USERS](),
          onItemDeleting: this.onDelete,
          fields: this.getGridFields(),
          controller: {
            loadData: this.gridFilter
          },
          editItem: (item) => this.onUpdateItem(RESOURCE_NAME,
                                                window.$(`#${this.editModalId}`),
                                                item)
        });
      })
  },
  watch: {
    usersList: {
      handler: function() {
        this.grid.jsGrid("option", "data", this.usersList);
      },
      deep: true
    }
  },
  data() {
    return {
      editedResource: {},
      adminPanelId: "adminPanel",
      createModalId: "createDialog",
      editModalId: "editDialog",
      userRolesFilter: ["ALL", MERCHANT.name, WORKER.name,
                        ADMIN.name, SUPER_ADMIN.name],
      orgsFilter: [{name: "ALL", id: -1}]
    }
  }
}
</script>
