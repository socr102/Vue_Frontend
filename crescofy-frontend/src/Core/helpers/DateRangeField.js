import { DATE_FORMAT } from './utils';

var DateRangeField = function(config) {
	window.jsGrid.Field.call(this, config);
};

DateRangeField.prototype = new window.jsGrid.Field({
  sorter: function(date1, date2) {
    return new Date(date1) - new Date(date2);
  },

  itemTemplate: (val, item) => {
    return `${item.start_date} - ${item.end_date}`;
  },

  filterTemplate: function() {
    this.picker = window.$("<input>").daterangepicker({
      autoUpdateInput: false,
      locale: { cancelLabel: 'Clear' }
    }).on('cancel.daterangepicker', () => {
      this.picker.val('');
      this.date_range = undefined;
    }).on('apply.daterangepicker', (ev, picker) => {
      this.date_range = {
        start_date: picker.startDate.format(DATE_FORMAT),
        end_date: picker.endDate.format(DATE_FORMAT)
      }
      this.picker.val(`${this.date_range.start_date} - ${this.date_range.end_date}`);
    });

    return this.picker;
  },

  filterValue: function() {
    if (!this.picker.val()) {
      this.date_range = undefined;
    }
    return this.date_range;
  }
});

window.jsGrid.fields.daterange = DateRangeField;

export default DateRangeField;
