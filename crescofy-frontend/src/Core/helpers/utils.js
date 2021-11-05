function isDebugMode() {
  return process.env.NODE_ENV !== 'production';
}

function authHeader(token) {
  return {"Authorization": `Bearer ${token}`};
}

const API_URL = process.env.VUE_APP_API_BASE || '';

const DATE_FORMAT = 'DD/MM/YYYY';

const DATE_REGEX = /^(0?[1-9]|[12][0-9]|3[01])[/-](0?[1-9]|1[012])[/-]\d{4}$/;

const PHONE_REGEX = /^(\+{0,})(\d{0,})([(]{1}\d{1,3}[)]{0,}){0,}(\s?\d+|\+\d{2,3}\s{1}\d+|\d+){1}[\s|-]?\d+([\s|-]?\d+){1,2}(\s){0,}$/gm;

export { isDebugMode, authHeader, API_URL, DATE_FORMAT, DATE_REGEX, PHONE_REGEX };
