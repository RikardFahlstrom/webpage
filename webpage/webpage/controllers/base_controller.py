#  BaseController handles common layout, features, initialization
import logbook

import webpage.infrastructure.static_cache as static_cache
import pyramid.renderers
import pyramid.httpexceptions as exc
import webpage.infrastructure.cookie_auth as cookie_auth

from webpage.infrastructure.supressor import suppress
from webpage.services.account_service import AccountService


class BaseController:
    def __init__(self, request):
        self.request = request
        self.build_cache_id = static_cache.build_cache_id

        layout_render = pyramid.renderers.get_renderer('webpage:templates/shared/_layout.pt')
        impl = layout_render.implementation()
        self.layout = impl.macros['layout']

        log_name = 'Ctrls/' + type(self).__name__.replace("Controller", "")
        self.log = logbook.Logger(log_name)

    @property
    def is_logged_in(self):
        return False

    # noinspection PyMethodMayBeStatic
    @suppress()
    def redirect(self, to_url, permanent=False):
        if permanent:
            raise exc.HTTPMovedPermanently(to_url)
        raise exc.HTTPFound(to_url)

    @property
    def data_dict(self):
        data = dict()
        data.update(self.request.GET)
        data.update(self.request.POST)
        data.update(self.request.matchdict)

        return data

    @property
    def logged_in_user_id(self):
        return cookie_auth.get_user_id_via_auth_cookie(self.request)

    @property
    def logged_in_user(self):
        uid = self.logged_in_user_id
        if not uid:
            return None

        AccountService.find_account_by_id(uid)