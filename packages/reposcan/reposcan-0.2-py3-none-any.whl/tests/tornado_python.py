import re

from helpers.Helper import Helper

text = """
import json
from tornado.web import RequestHandler, Application, url

class Test1Handler(RequestHandler):
    def get(self, pathParameter1, pathParameter2=None):
        # Query parameters
        queryParameter1 = self.get_query_argument('queryParameter1', None)
        queryParameter2 = self.get_query_argument('queryParameter2', None)

        # Header parameters
        headerParameter1 = self.request.headers.get('headerParameter1')
        headerParameter2 = self.request.headers.get('headerParameter2')

        # Response handling
        content_type = self.request.headers.get('Content-Type')
        if content_type == 'application/xml':
            self.set_header('Content-Type', 'application/xml')
            self.set_status(415)
            self.write("<response><message>XML format</message></response>")
        else:
            self.write(json.dumps({'incomes': 'data'}))  # Replace with actual data

    def post(self, pathParameter1, pathParameter2=None):
        # Query parameters
        queryParameter1 = self.get_query_argument('queryParameter1', None)
        queryParameter2 = self.get_query_argument('queryParameter2', None)

        # Header parameters
        headerParameter1 = self.request.headers.get('headerParameter1')
        headerParameter2 = self.request.headers.get('headerParameter2')

        # Body parameters
        if self.request.body:
            body = json.loads(self.request.body)
            bodyParameter1 = body.get('bodyParameter1')
            bodyParameter2 = body.get('bodyParameter2')

        # Response handling
        content_type = self.request.headers.get('Content-Type')
        if content_type == 'application/xml':
            self.set_header('Content-Type', 'application/xml')
            self.set_status(415)
            self.write("<response><message>XML format</message></response>")
        else:
            self.write(json.dumps({'incomes': 'data'}))  # Replace with actual data

class Test2Handler(RequestHandler):
    def get(self):
        self.set_status(200)
        self.write('')

def make_app():
    return Application([
        url(r"/test1/(.*?)/(.*?)", Test1Handler),
        url(r"/test1/(.*?)", Test1Handler),
        url(r"/test2", Test2Handler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server started at http://localhost:8888")
"""

# Loop all api matches
apiPattern = r'''((?:def (?P<httpMethods>\w+)(?P<pathParameters>\(.*\)):\n)|(?:self.get_query_argument\(\'(?P<queryParameters>.*)\'\n)|(?:self.request.headers.get\(\'(?P<headerParameters>.*)\'\)\n)|(?:json.loads\(self.request.body\).get(?P<bodyParameters>.*)\n)|(?:content_type == (?P<contentTypes>.*)\n)|(?:self.set_status(?P<responseCodes>.*)\n)|.*?\n)*?(?:(?:(?P<firstSeparatorPart>.*\n\n)(?P<secondSeparatorPart>\s*def ))|\Z)'''

apiPattern = "((?:def (?P<httpMethods>\\w+)(?P<pathParameters>\\(.*\\)):\\n)|(?:self.get_query_argument\\(\\'(?P<queryParameters>.*)\\'\\n)|(?:self.request.headers.get\\(\\'(?P<headerParameters>.*)\\'\\)\\n)|(?:json.loads\\(self.request.body\\).get(?P<bodyParameters>.*)\\n)|(?:content_type == (?P<contentTypes>.*)\\n)|(?:self.set_status(?P<responseCodes>.*)\\n)|.*?\\n)*?(?:(?:(?P<firstSeparatorPart>.*\\n\\n)(?P<secondSeparatorPart>\\s*def ))|\\Z)"

# Loop all api matches
apiMatches = re.finditer(apiPattern, text)
apiMatches = [apiMatch for apiMatch in apiMatches if apiMatch.group(0).strip() != ""]
linePatterns = Helper.getLinePatterns(apiPattern)
secondSeparatorParts= [""]
for apiMatch in apiMatches:
    apiMatchResult = Helper.getAPIMatchResult(apiMatch, linePatterns, secondSeparatorParts)
    if apiMatchResult and any(key in apiMatchResult for key in ["paths", "httpMethods"]):
        apiInfo = {}
        for key, value in apiMatchResult.items():
            value = set(str(item) for item in Helper.getElementSetFromObject(value) if item)
            if key == "httpMethods":
                if value:
                    httpMethods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
                    value = [item.upper() for item in value if item.upper() in httpMethods] or ["GET"]
                else:
                    value = ["GET"]
            print(key, value)
        print("==============================================================================================")