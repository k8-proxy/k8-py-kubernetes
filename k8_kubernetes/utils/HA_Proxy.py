from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Csv import load_csv_from_url
from osbot_utils.utils.Http import is_port_open
from osbot_utils.utils.Misc import env_vars, list_group_by, list_index_by, list_set, str_to_base64, to_int


class HA_Proxy:

    def __init__(self):
        self.config         = self.config_from_env()
        self.name_delimiter = '-ip-'

    def config_from_env(self):
        vars = env_vars()
        return {'password'  : vars.get('TEST_HAPROXY_PASSWORD' ),
                'port'      : vars.get('TEST_HAPROXY_PORT'     ),
                'schema'    : vars.get('TEST_HAPROXY_SCHEME'   ),
                'server'    : vars.get('TEST_HAPROXY_SERVER'   ),
                'username'  : vars.get('TEST_HAPROXY_USERNAME')}

    def resolve_server_id(self, value):
        for server_id in self.server_list():
            if value in server_id:
                return server_id

    def server_ips(self):
        return self.server_names_and_ips().get('ips')

    def server_online(self):
        config = self.config
        return is_port_open(config.get('server'), to_int(config.get('port')))

    def server_url(self):
        config = self.config
        return f"{config.get('schema')}://{config.get('server')}:{config.get('port')}"

    def server_list(self):
        raw_stats = self.stats()
        pxname    = list_group_by(raw_stats,'# pxname')
        icap_pool = pxname.get('icap_pool')
        servers   = list_index_by(icap_pool, 'svname')
        if servers.get('BACKEND'):
            del servers['BACKEND']                           # this row is the totals
        return list_set(servers)

    def server_names(self):
        return self.server_names_and_ips().get('names')

    def server_names_and_ips(self):
        names = []
        ips   = []
        for server in self.server_list():
            items = server.split(self.name_delimiter)
            if len(items) == 2:                 # when the mapping is correct
                names.append(items[0])
                ips  .append(items[1])
            else:
                names.append(server)     # if name_delimiter is not there, use the value as server_name

        return { 'ips' : ips, 'names': names }

    def server_stats(self, server_address):
        server_id = self.resolve_server_id(server_address)
        return self.stats(index_by='svname').get(server_id)

    @index_by
    @group_by
    def stats(self):
        url     = f'{self.server_url()}/;csv'
        headers = self.request_headers()
        stats   = load_csv_from_url(url, headers)
        return stats

    def request_headers(self):
        source             = f"{self.config.get('username')}:{self.config.get('password')}"
        credentials_base64 = str_to_base64(source)
        return  {'Authorization': f'Basic {credentials_base64}' }



