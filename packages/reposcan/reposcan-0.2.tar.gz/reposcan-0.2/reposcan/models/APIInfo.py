class APIInfo:
    def __init__(self, scanType="", project="", domain="", repository="", branch="", filePath="", extension="", language="", framework="", apiType="", baseUrl="", functionName="", lineNumber="", timeStamp="", keywords=[], httpMethods=[], paths=[], pathParameters=[], queryParameters=[], headerParameters=[], bodyParameters=[], contentTypes=[], responseCodes=[]):
        # Properties when cloning repos files: scanType, project, domain, repository, branches
        self.scanType = scanType # Type of Scan (RepoScan, DeploymentScan, LogScan)
        self.project = project  # Name of the project using the API
        self.domain = domain  # Domain of the API belwongs to
        self.repository = repository  # Name of the repository where the API code resides
        self.branch = branch  # Branch name in the repository

        # Properties when reading repos files: filePath, extension, language, framework, apiType, baseUrl, functionName, lineNumber, timeStamp, keywords, httpMethods, paths, pathParameters, queryParameters, headerParameters, bodyParameters, contentTypes, responseCodes
        self.filePath = filePath  # File path where the function/method is defined
        self.extension = extension  # File path where the function/method is defined
        self.language = language  # Language used to implement the API
        self.framework = framework  # Framework used to implement the API
        self.apiType = apiType  # Type of API (e.g., REST, SOAP, GraphQL)
        self.baseUrl = baseUrl  # Base URL of the API
        self.functionName = functionName  # Function or method name in the codebase related to this API
        self.lineNumber = lineNumber  # Line number in the file where the function/method is defined
        self.timeStamp = timeStamp  # Timestamp or date/time when this API information was recorded
        self.keywords = keywords # Keywords in the file
        self.httpMethods = httpMethods # HTTP methods supported by the API (GET, POST, etc.)
        self.paths = paths  # Path provided by the API
        self.pathParameters = pathParameters  # Parameters in the URL path
        self.queryParameters = queryParameters  # Query parameters in the URL
        self.headerParameters = headerParameters  # Headers required or supported by the API
        self.bodyParameters = bodyParameters  # Parameters included in the request body
        self.contentTypes = contentTypes  # Content types supported or returned by the API
        self.responseCodes = responseCodes  # HTTP response codes returned by the API