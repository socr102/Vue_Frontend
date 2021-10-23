import { subject } from '@casl/ability';

const controlField = (callback, headerText) => ({
  type: "control",
  modeSwitchButton: false,
  editButton: true,
  width: "auto",
  headerTemplate: function() {
    return window.$("<button>")
      .attr("type", "button")
      .addClass('btn btn-info waves-effect waves-light')
      .text(headerText)
      .on("click", function () { callback("Add", {}) });
  }
})

const onDeleteItem = ($alertify, $ability, callback,
                      resourceName, resourceAttr = 'name') => {
  return (args) => {
    let hasPermission = $ability.can('delete',
                                     subject(resourceName, args.item));
    if (!hasPermission) {
      $alertify.notify('Action Forbidden!', 'error', 3);
    } else {
      let confirmMsg = `This action will delete ${args.item[resourceAttr]} ${resourceName}. Are you sure?`;
      $alertify.confirm(
        'Please Confirm Your Action',
        confirmMsg,
        () => {
          callback(args.item.id).then(() =>
            $alertify.notify(`${resourceName} successfully removed.`,
                                  'success',
                                  3));
        },
        () => {}
      );
    }
    // cancel default deletion to prevent vue state error
    args.cancel = true;
  }
}

export { controlField, onDeleteItem };
