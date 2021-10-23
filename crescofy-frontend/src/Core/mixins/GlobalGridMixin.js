import { subject } from '@casl/ability';

export default {
  methods: {
    onUpdateItem( resourceName, $modal, item) {
      let hasPermission = this.$ability.can('update', subject(resourceName, item));
      if (hasPermission) {
        this.editedResource = item;
        $modal.modal('toggle');
      } else {
        this.$alertify.notify('Action Forbidden!', 'error', 3);
      }
    }
  }
}
