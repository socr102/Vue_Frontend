import { subject } from '@casl/ability';
import * as yup from 'yup';

export const MERCHANT_GROUP = 'merchant';
export const WORKER_GROUP = 'worker';

export const ADMIN = {name: 'ADMIN', obj: subject('User', {is_superuser: false, is_staff: true})};
export const SUPER_ADMIN = {name: 'SUPER ADMIN', obj: subject('User', {is_superuser: true})};
export const MERCHANT = {name: 'MERCHANT', obj: subject('User', {is_superuser: false, is_staff: false})};
export const WORKER = {name: 'WORKER', obj: subject('User', {
                                                    is_superuser: false, is_staff: false,
                                                    groups: [{name: WORKER_GROUP}]}
                                                    )};

export const UserRoleMixin = {
  methods: {
    /**
     * @param {string} userRole one of {ADMIN, SUPER ADMIN, MERCHANT}
     * @return {object} User object
     */
    getUser(userRole) {
      var newUser = {}
      switch(userRole) {
        case(SUPER_ADMIN.name):
          newUser.is_superuser = true;
          newUser.is_staff = true;
          break;
        case(ADMIN.name):
          newUser.is_staff = true;
          newUser.is_superuser = false;
          break;
        case(MERCHANT.name || WORKER.name):
          newUser.is_superuser = false;
          newUser.is_staff = false;
          break;
      }
      return newUser;
    },

    /**
     * @param {object} user raw data
     * @return {string} one of {ADMIN, SUPER ADMIN, MERCHANT, WORKER}
     */
    getUserRole(user) {
      if (user.is_superuser) {
        return SUPER_ADMIN.name;
      }
      if (user.is_staff) {
        return ADMIN.name;
      }
      if (user.groups && user.groups.find(g => g.name == WORKER_GROUP)) {
        return WORKER.name;
      }
      if (user.groups && user.groups.find(g => g.name == MERCHANT_GROUP)) {
        return MERCHANT.name;
      }

      return MERCHANT.name;
    },

    /**
     * @param {object} user raw data
     * @return {boolean} true if user is not a worker
     */
    hasAdminPageAccess(user) {
      return this.getUserRole(user) != WORKER.name;
    },

    /**
     * @param {string} action user permission
     * @return {array} of available user roles
     */
    getAvailableRoles(action) {
      var availableRoles = []
      if (this.$ability.can(action, SUPER_ADMIN.obj)) {
        availableRoles.push(SUPER_ADMIN.name);
      }
      if (this.$ability.can(action, ADMIN.obj)) {
        availableRoles.push(ADMIN.name);
      }
      if (this.$ability.can(action, MERCHANT.obj)) {
        availableRoles.push(MERCHANT.name);
      }

      if (this.$ability.can(action, WORKER.obj)) {
        availableRoles.push(WORKER.name);
      }

      return availableRoles;
    },

    isMerchantSelected() {
      return this.formValues.role == MERCHANT.name;
    },

    /**
     * Role based user role validator
     * @return {yup.Lazy} role validator
     */
    roleValidator() {
      if (!this.userProfile) return;
      if (this.getUserRole(this.userProfile) == MERCHANT.name) {
        return yup.string().matches(WORKER.name)
          .required('Please indicate your role')
      } else {
        return yup.string()
          .oneOf([ADMIN.name, SUPER_ADMIN.name, MERCHANT.name])
          .required('Please indicate your role')
      }
    },

    isAdminForm() {
      return this.formValues ? [MERCHANT.name, WORKER.name]
                                .includes(this.formValues.role) : true;
    },

    /**
     * Role based email validator
     * @return {yup.Lazy} email validator
     */
    emailValidator() {
      return yup.lazy(() => {
        if (this.isAdminForm()) {
          return yup.string().required('Email is required').email('Email is invalid')
        } else {
          return yup.string()
            .required('Email is required')
            .matches('^.+@crescofy.com$',
                     'Email must be in crescofy domain. Example: test@crescofy.com')
            .email('Email is invalid')
        }
      })
    },

    /**
     * Role based organization validator
     * Merchant user requires org name
     * @return {yup.Lazy} org validator
     */
    orgValidator() {
      return yup.lazy(() => {
        if (this.formValues.role == MERCHANT.name) {
          return yup.number()
            .oneOf(this.orgsList.map(o => o.id),
                   'Organization is required')
            .required('Organization is required')
        }
        return yup.number().notRequired();
      })
    }
  }
}
