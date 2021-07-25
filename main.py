from app import api, app
from flask_restful import Resource, reqparse
from bs4 import BeautifulSoup
from send_email import get_contacts_list, EmailThread
import werkzeug

# ALLOWED_EXTENSIONS = set(['csv', 'html', 'txt', 'doc'])

# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_htmlfile(file_html):
	return BeautifulSoup(file_html, 'html.parser').prettify(formatter=None)

class sendMail(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('email', type=str, required=True)
		parser.add_argument('password', type=str, required=True)
		parser.add_argument('title', type=str, required=True)
		parser.add_argument('html_file', type=werkzeug.datastructures.FileStorage, location='files', required=True)
		parser.add_argument('csv_file', type=werkzeug.datastructures.FileStorage, location='files', required=True)
		
		args = parser.parse_args()

		template = '''{}'''.format(read_htmlfile(args['html_file'])).replace('\\', '')
		print(template[:300])
		contacts_list = get_contacts_list(args['csv_file'])

		thread1 = EmailThread(args['email'], args['password'], args['title'], contacts_list, template)
		thread1.start()

		return {'message' : 'Sent {} mails successfully.'.format(len(contacts_list))}, 200

api.add_resource(sendMail, '/send_mail')

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)