from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
from restaurantmenu import *

# Create DB session and connect to DB.
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
session = DBSession()
DBSession = sessionmaker(bind=engine)

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            output = ""
            output += '<html><body>'
            output += 'Hello!'
            output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                            <h2>What would you like me to say?</h2>
                            <input name='message' type='text'>
                            <input type='submit' value='Submit'>
                        </form>
                        """
            output += '</body></html>'
            self.wfile.write(output)
            print output
            return

        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            output = ""
            output += '<html><body>'
            output += '&#161Hola!<br><br><a href="/hello">Back to hello.</a>'
            output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                            <h2>What would you like me to say?</h2>
                            <input name='message' type='text'>
                            <input type='submit' value='Submit'>
                        </form>
                        """
            output += '</body></html>'
            self.wfile.write(output)
            print output
            return

        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            restaurants = session.query(Restaurant).all()

            output = ""
            output += '<html><body>'
            output += '<h2><a href="/restaurants/new">Add A New Restaurant</a></h2>'
            output += '<br><br>'
            for restaurant in restaurants:
                output += restaurant.name
                output += '<a href="/restaurants/%s/edit">Edit</a>' % restaurant.id
                output += '<a href="/restaurants/%s/delete">Delete</a>' % restaurant.id
                output += '<br>'

            output += '<br>'
            output += '</body></html>'
            self.wfile.write(output)
            print output
            return

        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            restaurants = session.query(Restaurant).all()

            output = ""
            output += '<html><body>'
            output += """<form method='POST' enctype='multipart/form-data'
                        action='restaurants/new'>
                        <input method='POST' type='text'
                        placeholder='New Restaurant Name'
                        name='newRestaurantName'>
                        <input type='submit' value='Create'>
                        </form>
                        """
            output += '<br>'
            output += '</body></html>'
            self.wfile.write(output)
            print output
            return

        if self.path.endswith("/edit"):
            restaurant_id = self.path.split('/')[2]
            rest_query = session.query(Restaurant).filter_by(id = restaurant_id).one()
            if rest_query != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += '<html><body>'
                output += '<h1>Edit Restaurant</h1>'
                output += """<form method='POST' enctype='multipart/form-data'
                            action='restaurants/%s/edit'>
                            <input type='text' value='%s'
                            name='newRestaurantName'>
                            <input type='submit' value='Update'>
                            </form>
                            """ % (restaurant_id, rest_query.name)
                output += '<br>'
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return

        if self.path.endswith("/delete"):
            restaurant_id = self.path.split('/')[2]
            rest_query = session.query(Restaurant).filter_by(id = restaurant_id).one()
            if rest_query != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += '<html><body>'
                output += '<h1>Delete Restaurant</h1>'
                output += """<form method='POST' enctype='multipart/form-data'
                            action='restaurants/%s/delete'>
                            <p>Are you sure you want to delete %s?</p>
                            <input type='submit' value='Delete'>
                            </form>
                            """ % (restaurant_id, rest_query.name)
                output += '<br>'
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return

        else:
            self.send_error(404, "File Not Found %s" % self.path)


    def do_POST(self):

        if self.path.endswith('/hello'):
            try:
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                output = ""
                output += '<html><body>'
                output += '<h2>Okay, how about this:</h2>'
                output += '<h1>%s</h1>' % messagecontent[0]
                output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                                <h2>What would you like me to say?</h2>
                                <input name='message' type='text'>
                                <input type='submit' value='Submit'>
                            </form>
                            """
                output += '</body></html>'
                self.wfile.write(output)
                print output

            except:
                pass

        if self.path.endswith('/restaurants/new'):
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_restaurant = fields.get('newRestaurantName')

            create_restaurant(new_restaurant[0])

            output = ""
            output += '<html><body>'
            output += '<h2>Success!</h2>'
            output += '<p>Your new restaurant was successfully created!</p>'
            output += '<a href="/restaurants">back to Restaurants</a>'
            output += '</body></html>'
            self.wfile.write(output)
            print output

        if self.path.endswith('/edit'):
            restaurant_id = self.path.split('/')[2]
            rest_query = session.query(Restaurant).filter_by(id = restaurant_id).one()

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_name = fields.get('newRestaurantName')

            update_restaurant(rest_query.name,new_name[0])

            output = ""
            output += '<html><body>'
            output += '<h2>Success!</h2>'
            output += '<p>Your new restaurant was successfully renamed!</p>'
            output += '<a href="/restaurants">back to Restaurants</a>'
            output += '</body></html>'
            self.wfile.write(output)
            print output


        if self.path.endswith('/delete'):
            restaurant_id = self.path.split('/')[2]
            rest_query = session.query(Restaurant).filter_by(id = restaurant_id).one()
            session.delete(rest_query)
            session.commit()

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            output = ""
            output += '<html><body>'
            output += '<h2>Success!</h2>'
            output += '<p>%s was successfully deleted!</p>' % rest_query.name
            output += '<a href="/restaurants">back to Restaurants</a>'
            output += '</body></html>'
            self.wfile.write(output)
            print output


def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "\n Stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
