import salt.exceptions

import logging

log = logging.getLogger(__name__)

__virtualname__ = 'pkg_local'


def __virtual__():
    properly_loaded_indicator = 'pkg_local.properly_loaded'
    if properly_loaded_indicator in __salt__:
        return __virtualname__
    return (False, __salt__.missing_fun_string(properly_loaded_indicator))

_MOD_INIT_COMPLETED = True
_MOD_INIT_PENDING = False

def mod_init(low):
    environment_setup = __salt__['pkg_local.environment_setup']()
    if environment_setup:
        return _MOD_INIT_COMPLETED
    __salt__['pkg_local.setup_environment']()
    return _MOD_INIT_COMPLETED


def installed(name, version, archive={}, etc={}):
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
    __salt__['pkg_local.install'](name, version, archive, etc)
    return ret


def hello_world(name):
    ret = {'name': name, 'changes': {}, 'result': False, 'comment': ''}

    ret['result'] = __salt__['pkg_local.environment_setup']()

    ret['changes'] = {
        'cat': {
            'old': 'relaxing in front of the chimney',
            'new': 'running for her life',
        },
        'dog': {
            'old': 'staring at the cat',
            'new': 'hunting the cat',
        }
    }
    ret['comment'] = 'This went really well!'
    return ret


def enforce_custom_thing(name, foo, bar=True):
    """
    Enforce the state of a custom thing

    This state module does a custom thing. It calls out to the execution module
    ``pkg_local`` in order to check the current system and perform any
    needed changes.

    :param name
        The thing to do something to
    :param foo
        A required argument
    :param bar : True
        An argument with a default value
    """
    ret = {'name': name, 'changes': {}, 'result': False, 'comment': ''}

    # Start with basic error-checking. Do all the passed parameters make sense
    # and agree with each-other?
    if bar == True and foo.startswith('Foo'):
        raise salt.exceptions.SaltInvocationError(
                'Argument "foo" cannot start with "Foo" if argument "bar" is True.')

    # Check the current state of the system. Does anything need to change?
    current_state = __salt__['my_custom_module.current_state'](name)

    if current_state == foo:
        ret['result'] = True
        ret['comment'] = 'System already in the correct state'
        return ret

    # The state of the system does need to be changed. Check if we're running
    # in ``test=true`` mode.
    if __opts__['test'] == True:
        ret['comment'] = 'The state of "{0}" will be changed.'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': 'Description, diff, whatever of the new state',
        }

        # Return ``None`` when running with ``test=true``.
        ret['result'] = None

        return ret

    # Finally, make the actual change and return the result.
    new_state = __salt__['my_custom_module.change_state'](name, foo)

    ret['comment'] = 'The state of "{0}" was changed!'.format(name)

    ret['changes'] = {
        'old': current_state,
        'new': new_state,
    }

    ret['result'] = True

    return ret
