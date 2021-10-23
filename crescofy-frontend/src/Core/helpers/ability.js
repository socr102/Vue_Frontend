import { AbilityBuilder, Ability } from '@casl/ability';
import { WORKER_GROUP, UserRoleMixin,
         ADMIN, SUPER_ADMIN,
         MERCHANT, WORKER } from '../mixins/UserRoleMixin';


export function defineRulesFor(user) {
  const userRole = UserRoleMixin.methods.getUserRole(user);
  const { can, rules, cannot } = new AbilityBuilder();

  if (userRole == SUPER_ADMIN.name) {
    can(['list', 'update', 'delete',
         'read', 'create', 'deactivate'],
         'User');
    cannot(['deactivate'], 'User', {is_active: false});
    cannot(['deactivate'], 'User', {delete_request: user.id});
  } else if (userRole == ADMIN.name) {
    can(['list', 'read'], 'User');
    can(['update', 'create'], 'User', {is_superuser: false, is_staff: false});
    can(['deactivate'], 'User', { is_superuser: false,
                                  is_staff: false,
                                  delete_request: null,
                                  is_active: true});
  } else if (userRole == WORKER.name) {
    can('read', 'User');
  } else if (userRole == MERCHANT.name) {
    can('read', 'User');
    can(['list', 'update', 'delete',
         'create', 'deactivate'],
         'User', { groups: { $elemMatch: {name: WORKER_GROUP} }}
        );
    cannot(['delete', 'update'], 'User', {id: user.id});
  }

  if ([SUPER_ADMIN.name, ADMIN.name].includes(userRole)) {
    can(['list', 'update', 'delete',
         'read', 'create'], 'Org');

    cannot(['delete', 'update'], 'User', {id: user.id});
    cannot(['create'], 'User', { groups: { $elemMatch: {name: WORKER_GROUP} }});
  }

  if ([SUPER_ADMIN.name, ADMIN.name,
       WORKER.name, MERCHANT.name]
       .includes(userRole)) {
    can(['list', 'delete', 'read', 'create'], 'Offer');
    can(['update'], 'Offer', {is_active: false});

    can(['list', 'delete', 'read',
         'create', 'update'], 'Audience');

    can(['list', 'read', 'create', 'update'], 'Member');
    can(['delete'], 'Member', {is_active: true});

    can(['list', 'delete', 'read', 'create'], 'Campaign');
    can(['update', 'duplicate'], 'Campaign', {is_active: false});
  }
  return rules
}

export const ability = new Ability([]);
