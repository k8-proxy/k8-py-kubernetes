
def run(event, context=None):

    from osbot_utils.utils.Misc import to_string
    from osbot_utils.utils.Process import exec_process
    command         = event.get('command')
    params          = event.get('params')
    result          = exec_process(command, params)
    result['error'] = to_string(result.get('error'))
    return result