import salt.exceptions

import logging

log = logging.getLogger(__name__)


def mod_init(low):
    log.info('initialize state module for \'' + low['fun'] + '\'')

    if low['name'] in ['maven', 'java'] :
        return False # Call mod_init the next time a function is called in this state
    return True


def installed(name, version, archive={}, etc={}):
    # name,result,changes,comment
    ret = {'name': name, 'changes': {}, 'result': True, 'comment': ''}
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
