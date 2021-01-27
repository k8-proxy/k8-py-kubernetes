from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda


class K8_Lambda(Deploy_Lambda):                # todo: add support for running kubernetes API from lambda

    def deploy(self):
        #self.add_osbot_utils()
        #self.add_osbot_aws()
        return self.update()
