import pyramid_handlers
from webpage.controllers.base_controller import BaseController
from webpage.services.albums_service import AlbumsService


class AlbumsController(BaseController):
    @pyramid_handlers.action(renderer='templates/albums/index.pt')
    def index(self):
        #  based on above url, this action gets triggered
        all_albums = AlbumsService.get_albums()

        # each model needs to always return a dictionary
        return {'albums': all_albums}