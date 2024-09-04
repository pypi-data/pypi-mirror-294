import re, autopep8
import black

from helpers.Helper import Helper

text = """
    from fastapi import FastAPI, Request, Header, Body
    from typing import Optional
    from fastapi.responses import JSONResponse, PlainTextResponse

    app = FastAPI()

    @app.get("/tag/{pathParameter1}")
    async def test1(pathParameter1: str):
        # Just comment
        return {"message": "OK"}

    @app.route("/tag/{pathParameter1}/page-{pathParameter2}", methods=["GET", "POST"])
    @app.get("/tag/{pathParameter1}/page-{pathParameter2}/xyz")
    async def test1(
        pathParameter1: str,
        pathParameter2: int,
        queryParameter1: Optional[str] = None,
        queryParameter2: Optional[str] = None,
        headerParameter1: Optional[str] = Header(None),
        headerParameter2: Optional[str] = Header(None),
        requestBody: Optional[dict] = Body(None),
        request: Request
    ):
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/xml':
            return PlainTextResponse(content="<response><message>XML format</message></response>", media_type='application/xml', status_code=415)
        else:
            return JSONResponse(content={"incomes": "data"})  # Replace with actual data

    @app.get("/tag")
    async def test2():
        return {"message": "OK"}

"""

apiPattern = r'''((?:@app.(?P<httpMethods>\w+)\(\"(?P<paths>[^\"]*).*\)\n)|(?:async def (?P<functionName>\w+)(?P<pathParameters>\(.*\)):\n)|(?:request.GET.get(?P<queryParameters>.*)\n)|(?:request.headers.get(?P<headerParameters>.*)\n)|(?:json.loads\(request.body\).get(?P<bodyParameters>.*)\n)|(?:content_type == (?P<contentTypes>.*)\n)|(?:return .* status=(?P<responseCodes>\d+).*\n)|.*?\n)*?(?:(?:(?P<firstSeparatorPart>.*\n\n)(?P<secondSeparatorPart>\s*@app))|\Z)'''
Helper.config = Helper.jsonObjectFromJsonFile(r'.\data\config.json')
apiPattern = Helper.config["extensions"][".py"]["Python"]["FastAPI"]["REST"]["pattern"]

print(black.format_str(text, mode=black.FileMode(line_length=120)))
print(autopep8.fix_code(text))

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