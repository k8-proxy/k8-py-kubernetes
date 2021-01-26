def run(event, context=None):
    return 'From lambda code, hello {0}'.format(event.get('name'))