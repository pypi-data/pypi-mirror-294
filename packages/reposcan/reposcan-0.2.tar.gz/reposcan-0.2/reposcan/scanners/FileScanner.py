import re, inspect
from datetime import datetime
from abc import ABC, abstractmethod
from ..helpers.Helper import Helper
from ..models.APIInfo import APIInfo

class FileScanner(ABC):
    # Get info from a file path, the result can't be None
    @abstractmethod
    def addAPIInfosAndAPISummaryInfos(self, scanType="", project="", domain="", repository="", branch="", filePath="", extension="", languageDict={}, keywords=[]):
        apiInfos = []
        apiSummaryInfos = {}
        try:
            # Filter out code files only, no need to check null for file path, let isTextFile do that
            if Helper.isTextFile(filePath):
                with open(filePath, "r", encoding="utf-8") as f:
                    text = f.read().rstrip("\n") + "\n"
                    # For each file path, loop all languages, all frameworks
                    for language, frameworkDict in languageDict.items():
                        for framework, apiTypeDict in frameworkDict.items():
                            for apiType, apiTypeFiltersAndPattern in apiTypeDict.items():
                                # Filter out the invalid files by filter for each extension, language, framework, apiType
                                if Helper.containKeywords(text, keywords) and Helper.containKeywords(text, Helper.config["extensions"][extension][language][framework][apiType]["filters"]):
                                    if keywords == None:
                                        keywords = []

                                    # Loop all api matches
                                    apiPattern = apiTypeFiltersAndPattern["pattern"]
                                    apiMatches = re.finditer(apiPattern, text)
                                    apiMatches = [apiMatch for apiMatch in apiMatches if apiMatch.group(0).strip() != ""]
                                    linePatterns = Helper.getLinePatterns(apiPattern)
                                    secondSeparatorParts= [""]
                                    for apiMatch in apiMatches:
                                        apiMatchResult = Helper.getAPIMatchResult(apiMatch, linePatterns, secondSeparatorParts)
                                        if apiMatchResult and any(key in apiMatchResult for key in ["paths", "httpMethods"]):
                                            # Get api infos
                                            apiInfo = {"scanType": scanType, "project": project, "domain": domain, "repository": repository, "branch": branch, "filePath": filePath, "extension": extension, "language": language, "framework": framework, "apiType": apiType, "baseUrl": "", "functionName": "", "lineNumber": "", "timeStamp": "", "keywords": keywords, "httpMethods": [], "paths": [], "pathParameters": [], "queryParameters": [], "headerParameters": [], "bodyParameters": [], "contentTypes": [], "responseCodes": []}
                                            for key, value in apiMatchResult.items():
                                                value = set(str(item) for item in Helper.getElementSetFromObject(value) if item)
                                                if key == "httpMethods":
                                                    if value:
                                                        httpMethods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
                                                        value = [item.upper() for item in value if item.upper() in httpMethods] or ["GET"]
                                                    else:
                                                        value = ["GET"]
                                                if isinstance(apiInfo[key], list):
                                                    apiInfo[key] = list(value)
                                                else:
                                                    apiInfo[key] = ",".join(value)
                                            matchingText = text[:apiMatch.span()[0]]
                                            apiInfo["lineNumber"] = str(len(matchingText) - len(matchingText.replace("\n","")) + 1)
                                            apiInfo["timeStamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                            apiInfos.append(APIInfo(**apiInfo))

                                            # Get api summary infos
                                            apiSummaryInfos["numberOfAPIs"] = apiSummaryInfos.setdefault("numberOfAPIs", 0) + 1
                                            apiSummaryInfos.setdefault("languages", set()).add(language)
                                            apiSummaryInfos.setdefault("frameworks", set()).add(framework)
                                            apiSummaryInfos.setdefault("apiTypes", set()).add(apiType)

                        # Convert api summary info into list from set
                        if all(key in apiSummaryInfos for key in ["numberOfAPIs", "languages", "frameworks", "apiTypes"]):
                            apiSummaryInfos["languages"] = list(apiSummaryInfos["languages"])
                            apiSummaryInfos["frameworks"] = list(apiSummaryInfos["frameworks"])
                            apiSummaryInfos["apiTypes"] = list(apiSummaryInfos["apiTypes"])
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Filepath {filePath} is invalid.")
        except Exception as e:
            apiInfos = []
            apiSummaryInfos = {}
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return apiInfos, apiSummaryInfos