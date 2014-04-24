class Backend(object):
    def get_url_redirect(self, request):
        raise NotImplementedError

    def save_url_redirect(self, request, response):
        raise NotImplementedError

    def delete_next_action(self, request):
        raise NotImplementedError

    def run_next_action(self, request):
        raise NotImplementedError

    def get_next_action(self, request):
        raise NotImplementedError

    def save_next_action(self, request, data):
        raise NotImplementedError
