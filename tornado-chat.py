import  tornado.web
import tornado.ioloop

class MainHandler(tornado.web.RequestHandler):
    '''
    Handler for basic request and response
    '''
    def get(self):
        self.write('Hello World')

def make_app():
    return tornado.web.Application([
        (r'/',MainHandler)
    ])


if __name__ == "__main__":
    print('starting to run')
    app = make_app()
    app.listen(8888)
    print('listning on port 8888')
    tornado.ioloop.IOLoop.current().start()
