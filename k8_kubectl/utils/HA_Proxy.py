from k8_kubectl.helpers.to_add_to_sbot.OSBot_Utils__Local import str_to_base64, load_csv_from_url, env_vars


class HA_Proxy:

    def __init__(self):
        self.config = self.config_from_env()

    def config_from_env(self):
        vars = env_vars()
        return {'password'  : vars.get('TEST_HAPROXY_PASSWORD' ),
                'port'      : vars.get('TEST_HAPROXY_PORT'     ),
                'schema'    : vars.get('TEST_HAPROXY_SCHEME'   ),
                'server'    : vars.get('TEST_HAPROXY_SERVER'   ),
                'username'  : vars.get('TEST_HAPROXY_USERNAME')}

    def server_url(self):
        config = self.config
        return f"{config.get('schema')}://{config.get('server')}:{config.get('port')}"

    def request_headers(self):
        source             = f"{self.config.get('username')}:{self.config.get('password')}"
        credentials_base64 = str_to_base64(source)
        return  {'Authorization': f'Basic {credentials_base64}' }

    def stats(self):
        url     = f'{self.server_url()}/;csv'
        headers = self.request_headers()
        return load_csv_from_url(url, headers)

