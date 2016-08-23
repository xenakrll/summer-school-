WEBHOOK_HOST = '159.93.208.18'
WEBHOOK_PORT = 80
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = '/home/xenakrll/Documents/tgbot/main/webhook_cert.pem'
WEBHOOK_SSL_PRIV = '/home/xenakrll/Documents/tgbot/main/webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

bot = telebot.TeleBot(config.token)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)
