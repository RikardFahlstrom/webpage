import pyramid_handlers
from webpage.controllers.base_controller import BaseController
from webpage.services.mailinglist_service import MailingListService


class NewsLetterController(BaseController):
    # POST /newsletter/add_subscriber
    @pyramid_handlers.action(request_method='POST')
    def add_subscriber(self):
        email = self.data_dict.get('email')

        if MailingListService.add_subscriber(email):
            self.redirect('/newsletter/subscribed')

        self.redirect('/newsletter/failed')

    @pyramid_handlers.action(renderer='templates/newsletter/subscribed.pt')
    def subscribed(self):
        return {}

    @pyramid_handlers.action(renderer='templates/newsletter/failed.pt')
    def failed(self):
        return {}