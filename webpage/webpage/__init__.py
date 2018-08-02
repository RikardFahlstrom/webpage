import datetime
import sys

import pkg_resources
from pyramid.config import Configurator
import os
import webpage
import webpage.controllers.home_controller as home
import webpage.controllers.albums_controller as albums
import webpage.controllers.account_controller as account
import webpage.controllers.admin_controller as admin
import webpage.controllers.newsletter_controller as news
from webpage.data.dbsession import DbSessionFactory
from webpage.email.template_parser import EmailTemplateParser
from webpage.services.email_service import EmailService
from webpage.services.log_service import LogService
from webpage.services.mailinglist_service import MailingListService

dev_mode = False


def main(_, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    init_logging(config)
    init_mode(config)
    init_includes(config)
    init_email_templates(config)
    init_routing(config)
    init_db(config)
    init_mailing_list(config)
    init_smtp_mail(config)

    return config.make_wsgi_app()


def init_logging(config):
    settings = config.get_settings()
    log_level = settings.get('log_level')
    log_filename = settings.get('log_filename')

    LogService.global_init(log_level, log_filename)

    log_package_versions()


def init_db(_):
    top_folder = os.path.dirname(webpage.__file__)  # __file__ refers to current file, dirname gives path
    rel_folder = os.path.join('db', 'webpage.sqlite')  # .join is a "smart" path creator

    db_file = os.path.join(top_folder, rel_folder)
    DbSessionFactory.global_init(db_file)


def init_email_templates(_):
    EmailTemplateParser.global_init()


def init_smtp_mail(config):
    global dev_mode
    unset = 'YOUR VALUE'

    settings = config.get_settings()
    smtp_username = settings.get('smtp_username')
    smtp_password = settings.get('smtp_password')
    smtp_server = settings.get('smtp_server')
    smtp_port = settings.get('smtp_port')

    if smtp_username == unset:
        log = LogService.get_startup_log()
        log.warn("SMTP server values not set in config file. Outbound email will not work.")

    EmailService.global_init(smtp_username, smtp_password, smtp_server, smtp_port, dev_mode)


def init_mailing_list(config):
    unset = 'ADD_YOUR_API_KEY'

    settings = config.get_settings()
    mailchimp_api = settings.get('mailchimp_api')
    mailchimp_list_id = settings.get('mailchimp_list_id')

    if mailchimp_api == unset:
        log = LogService.get_startup_log()
        log.warn("Mailchimp API values not set in config file. Mailing list subscriptions will not work.")

    MailingListService.global_init(mailchimp_api, mailchimp_list_id)


def init_mode(config):
    global dev_mode
    settings = config.get_settings()
    dev_mode = settings.get('mode') == 'dev'
    log = LogService.get_startup_log()
    log.notice("Running in {} mode.".format('dev' if dev_mode else 'prod'))


def init_routing(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_handler('root', '/', handler=home.HomeController, action='index')

    add_controller_routes(config, home.HomeController, 'home')
    add_controller_routes(config, albums.AlbumsController, 'albums')
    add_controller_routes(config, account.AccountController, 'account')
    add_controller_routes(config, admin.AdminController, 'admin')
    add_controller_routes(config, news.NewsLetterController, 'newsletter')

    config.scan()


def add_controller_routes(config, ctrl, prefix):
    config.add_handler(prefix + 'ctrl_index', '/' + prefix, handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl_index/', '/' + prefix + '/', handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl', '/' + prefix + '/{action}', handler=ctrl)
    config.add_handler(prefix + 'ctrl/', '/' + prefix + '/{action}/', handler=ctrl)
    config.add_handler(prefix + 'ctrl_id', '/' + prefix + '/{action}/{id}', handler=ctrl)


def init_includes(config):
    config.include('pyramid_chameleon')
    config.include('pyramid_handlers')
    config.include('rollbar.contrib.pyramid')


def log_package_versions():
    startup_log = LogService.get_startup_log()

    # update from setup.py when changed!
    # This list is the closure of all dependencies,
    # taken from: pip list --format json
    requires = [{"name": "ansible", "version": "2.4.2.0"},
                {"name": "asn1crypto", "version": "0.24.0"},
                {"name": "bcrypt", "version": "3.1.4"}, {"name": "certifi", "version": "2017.11.5"},
                {"name": "cffi", "version": "1.11.4"}, {"name": "Chameleon", "version": "3.2"},
                {"name": "chardet", "version": "3.0.4"}, {"name": "cryptography", "version": "2.1.4"},
                {"name": "docopt", "version": "0.4.0"}, {"name": "html2text", "version": "2018.1.9"},
                {"name": "hupper", "version": "1.0"}, {"name": "idna", "version": "2.6"},
                {"name": "Jinja2", "version": "2.10"}, {"name": "Logbook", "version": "1.2.1"},
                {"name": "mailchimp", "version": "2.0.9"}, {"name": "mailer", "version": "0.8.1"},
                {"name": "Mako", "version": "1.0.7"}, {"name": "MarkupSafe", "version": "1.0"},
                {"name": "paramiko", "version": "2.4.0"}, {"name": "passlib", "version": "1.7.1"},
                {"name": "PasteDeploy", "version": "1.5.2"}, {"name": "pip", "version": "9.0.1"},
                {"name": "plaster", "version": "1.0"}, {"name": "plaster-pastedeploy", "version": "0.4.1"},
                {"name": "pyasn1", "version": "0.4.2"}, {"name": "pycparser", "version": "2.18"},
                {"name": "Pygments", "version": "2.2.0"}, {"name": "PyNaCl", "version": "1.2.1"},
                {"name": "pyramid", "version": "1.9.1"}, {"name": "pyramid-chameleon", "version": "0.3"},
                {"name": "pyramid-debugtoolbar", "version": "4.3"}, {"name": "pyramid-handlers", "version": "0.5"},
                {"name": "pyramid-mako", "version": "1.0.2"}, {"name": "PyYAML", "version": "3.12"},
                {"name": "repoze.lru", "version": "0.7"}, {"name": "requests", "version": "2.18.4"},
                {"name": "setuptools", "version": "36.6.0"}, {"name": "six", "version": "1.11.0"},
                {"name": "SQLAlchemy", "version": "1.1.15"}, {"name": "translationstring", "version": "1.3"},
                {"name": "urllib3", "version": "1.22"}, {"name": "venusian", "version": "1.1.0"},
                {"name": "waitress", "version": "1.1.0"}, {"name": "WebOb", "version": "1.7.3"},
                {"name": "webpage", "version": "0.0"}, {"name": "zope.deprecation", "version": "4.3.0"},
                {"name": "zope.interface", "version": "4.4.3"}]

    requires.sort(key=lambda d: d['name'].lower())
    t0 = datetime.datetime.now()
    startup_log.notice('---------- Python version info ------------------')
    startup_log.notice(sys.version.replace('\n', ' ').replace('  ', ' '))
    startup_log.notice('---------- package version info ------------------')
    for rec in requires:
        try:
            version = pkg_resources.get_distribution(rec['name']).version
            if version:
                startup_log.notice('{} v{}'.format(rec['name'], version))
            else:
                startup_log.notice("WHERE IS IT? {}.".format(rec['name']))
        except Exception as x:
            startup_log.notice('{} UNKNOWN VERSION ({})'.format(rec['name'], x))

    dt = datetime.datetime.now() - t0

    startup_log.notice('Package info gathered in {} sec'.format(dt.total_seconds()))
    startup_log.notice('--------------------------------------------------')