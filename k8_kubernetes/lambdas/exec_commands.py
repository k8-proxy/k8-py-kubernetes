from osbot_utils.utils.Process import exec_process
def run(event, context=None):
    command = event.get('command')
    params  = event.get('params')
    return exec_process(command, params)