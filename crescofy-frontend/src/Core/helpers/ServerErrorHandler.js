// use this field to show server errors that
// not corresponds to any of form fields
const SERVER_ERROR_FIELD = 'detail';
const DEFAULT_ERROR_TEXT = 'Server error ocurred';

function setErrors(actions, data) {
  for (let [field, err] of Object.entries(data)) {
    if (Array.isArray(err)) err = err.join(" ")

    actions.setFieldError(field, err);
  }
}

export default function ServerErrorHandler(actions, serverResponse) {
  switch (serverResponse.status) {
    case 401:
    case 403:
    case 500:
      actions.setFieldError(SERVER_ERROR_FIELD, serverResponse.data[SERVER_ERROR_FIELD]);
      break;
    case 400:
      setErrors(actions, serverResponse.data);
      break;
    default:
      actions.setFieldError(SERVER_ERROR_FIELD, DEFAULT_ERROR_TEXT);
      break;
  }
}
