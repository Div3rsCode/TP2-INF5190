export FLASK_APP=app.py

run:
	raml2html doc.raml > templates/doc.html
	flask run