from github import Github, Auth
import re, os, ast, csv, git, json, subprocess, logging, inspect, openpyxl

class Helper:
    # Get info and error logs
    LOGGER = logging.getLogger(__name__)

    # Dummy method
    @staticmethod
    def dummyMethod(parameter):
        result = False
        try:
            if parameter:
                pass
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): The parameter is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")                
        return result

    ### LOGGING API
    # Setup log, the result is either False or True, but it can't be None
    @staticmethod
    def initLogger(logLevel=logging.INFO, logFilePath=".\\logs\\app.log", clearLog = False):
        result = False
        try:
            if logLevel and logFilePath and clearLog != None:
                # Remove old log folder if needed, create log folder if not existing yet
                logFolder = os.path.dirname(logFilePath)
                if clearLog and os.path.exists(logFolder):
                    Helper.removeFileOrFolder(logFolder)
                os.makedirs(logFolder, exist_ok=True)

                # Set log level, log format, log output locations
                logging.basicConfig(level=logLevel, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s", handlers=[logging.FileHandler(logFilePath), logging.StreamHandler()])
                result = True
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): The parameter is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")                
        return result
        
    ### GITHUB API
    # Get repos list from a url and a username, result is either empty list or not empty list but can't be None
    @staticmethod
    def getRepositories(url, username, password=None):
        result = []
        try:
            if url and username:
                if url == "github.com":
                    g = Github(login_or_token=username, password=password)
                    result = [repo.name for repo in g.get_user().get_repos() if repo.full_name.startswith(username)]
                else:
                    Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): The parameter is invalid.")
        except Exception as e:
            try:
                if url and username:
                    if url == "github.com":
                        g = Github(password=password)
                        result = [repo.name for repo in g.get_user(login=username).get_repos() if repo.full_name.startswith(username)]
                    else:
                        Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): The parameter is invalid.")
            except Exception as e:
                Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Get repos list from a url and a username, result contains objects, they can be None
    @staticmethod
    def getRepository(url, username, password=None, repository=None):
        result = (None, None, None, None)
        try:
            if url and username and repository:
                if url == "github.com":
                    github = Github(login_or_token=username, password=password)
                    repo = github.get_repo(f"{username}/{repository}")
                    project = repo.description
                    domain = "_".join(repo.topics)
                    branches = [branch.name for branch in repo.get_branches()]
                    result = (project, domain, branches)
                else:
                    Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): The parameter is invalid.")
        except Exception as e:
            try:
                if url and username:
                    if url == "github.com":
                        github = Github(password=password)
                        repo = github.get_repo(f"{username}/{repository}")
                        project = repo.description
                        domain = "_".join(repo.topics)
                        branches = [branch.name for branch in repo.get_branches()]
                        result = (project, domain, branches)
                    else:
                        Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): The parameter is invalid.")
            except Exception as e:
                Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    ### JSON API
    # Convert json object to json file and vice verse, result is object so it can be None, if result is boolean so it can be None
    @staticmethod
    def jsonObjectFromJsonFile(filePath):
        result = None
        try:
            if filePath:
                with open(filePath, "r", encoding="utf-8") as f:
                    result = json.load(f)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): The filePath is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")                
        return result

    @staticmethod
    def jsonFileFromJsonObject(jsonObject, filePath):
        result = False
        try:
            if jsonObject and filePath:
                with open(filePath, "w", encoding="utf-8") as f:
                    json.dump(jsonObject, f, indent=4)
                    result = True
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Either jsonObject or filePath is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")                
        return result

    # Convert json object to json string and vice verse
    @staticmethod
    def jsonObjectFromJsonString(jsonString):
        result = None
        try:
            if jsonString:
                result = json.loads(jsonString)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): The jsonString is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")                
        return result

    @staticmethod
    def jsonStringFromJsonObject(jsonObject):
        result = None
        try:
            if jsonObject:
                result = json.dumps(jsonObject)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): The jsonObject is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")                
        return result

    # Convert json string to json file and vice verse
    @staticmethod
    def jsonFileFromJsonString(jsonString, jsonFile):
        result = None
        try:
            if jsonString and jsonFile:
                with open(jsonFile, "w", encoding="utf-8") as f:
                    f.write(jsonString)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Either jsonString or jsonFile is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")                
        return result

    @staticmethod
    def jsonStringFromJsonFile(jsonFile):
        result = None
        try:
            if jsonFile:
                with open(jsonFile, "r", encoding="utf-8") as f:
                    result = f.read(jsonFile)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): JsonFile is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")                
        return result

    ### STRING API
    # Get the correct path from a path based on the operating system
    @staticmethod
    def getPath(path):
        result = None
        try:
            if path:
                if os.name == "nt": # Windows
                    result = path.replace("/", "\\")
                else:  # Linux/Unix/MacOS
                    result = path.replace("\\", "/")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")                
        return result

    # Get groups from pattern, the result can't be None
    @staticmethod
    def getGroups(pattern):
        stack = []
        current = []
        try:
            if pattern:
                i = 0
                while i < len(pattern):
                    char = pattern[i]
                    if char == '(':
                        stack.append(current)
                        current = []
                        i += 1
                    elif char == ')':
                        if stack:
                            last = stack.pop()
                            last.append(current)
                            current = last
                        i += 1
                    elif char == ',':
                        i += 1
                    else:
                        start = i
                        while i < len(pattern) and pattern[i] not in '(),':
                            if pattern[i] == '\\':
                                i += 1
                            i += 1
                        value = pattern[start:i]
                        if value:
                            current.append(value)
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return current[0]

    # Get pattern from groups
    @staticmethod
    def getPattern(groups):
        result = None
        try:
            if groups:
                if isinstance(groups, str):
                    result = groups
                elif isinstance(groups, list):
                    elements = [Helper.getPattern(e) for e in groups]
                    result = f"({''.join(elements)})"
        except Exception as e:
            result = None
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Get line patterns from apiPattern, result can't be None
    @staticmethod
    def getLinePatterns(apiPattern):
        result = []
        try:
            if apiPattern:
                groupPattern = r'\)(?=\|)'
                matches = re.finditer(groupPattern, apiPattern)
                for match in matches:
                    endIndex = match.start()
                    balance = 1
                    i = endIndex - 1
                    while i >= 0:
                        if apiPattern[i] == ')' and apiPattern[i - 1] != '\\':
                            balance += 1
                        elif apiPattern[i] == '(' and apiPattern[i - 1] != '\\':
                            balance -= 1
                            if balance == 0:
                                startIndex = i
                                substring = apiPattern[startIndex:endIndex+1]
                                result.append(substring)
                                break
                        i -= 1
        except Exception as e:
            result = []
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Get group patterns from a line pattern, result can't be None
    @staticmethod
    def getGroupPatterns(linePattern):
        result = {}
        try:
            if linePattern:
                matches = re.finditer(r'\(\?P<(\w+)>', linePattern)
                for match in matches:
                    startIndex = match.start()
                    lastIndex = match.start()
                    opennedBrackets = 0
                    closedBrackets = 0
                    while lastIndex < len(linePattern) and closedBrackets < opennedBrackets or opennedBrackets == 0:
                        if linePattern[lastIndex] == "(":
                            opennedBrackets += 1
                        elif linePattern[lastIndex] == ")":
                            closedBrackets += 1
                        lastIndex += 1
                    result[match.group(1)] = linePattern[startIndex:lastIndex]
        except Exception as e:
            result = {}
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Get captured group indexes by name, the result can't be None
    @staticmethod
    def getCapturedGroupIndexesByName(linePattern):
        result = {}
        try:
            if linePattern:
                result = dict(re.compile(linePattern).groupindex.items())
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Get captured group patterns by index
    @staticmethod
    def getCapturedGroupPatternsByIndex(linePattern):
        result = {}
        try:
            if linePattern:
                groups = []
                groupStack = []
                index = 1
                escaped = False
                for endPosition, character in enumerate(linePattern):
                    if character == '\\':
                        escaped = True
                    elif character == '(' and not escaped and linePattern[endPosition + 1:endPosition + 3] != "?:":
                        groupStack.append((index, endPosition))
                        index += 1
                    elif character == ')' and not escaped:
                        if groupStack:
                            startIndex, startPosition = groupStack.pop()
                            groups.append((startIndex, startPosition, endPosition))
                    else:
                        escaped = False
                result = {group[0]:linePattern[group[1]: group[2] + 1] for group in groups}
        except Exception as e:
            result = {}
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Get captured groups by name
    @staticmethod
    def getCapturedGroupsByName(linePattern):
        result = {}
        try:
            if linePattern:
                capturedGroupPatternsByIndex = Helper.getCapturedGroupPatternsByIndex(linePattern)
                groupNameMatches = re.finditer(r'\(\?P<(\w+)>', linePattern)
                for groupNameMatch in groupNameMatches: 
                    # Sort groups so it can be inferred the group level by group length
                    groupName = groupNameMatch.group(1)
                    groups = [(groupIndex, groupPattern) for groupIndex, groupPattern in capturedGroupPatternsByIndex.items() if f"?P<{groupName}>" in groupPattern]
                    groups = sorted(groups, key=lambda item: len(item[1]))
                    isRepeatedGroup = False
                    if groups:
                        for (groupIndex, groupPattern) in groups:
                            if groupPattern.endswith("*?)"):
                                isRepeatedGroup = True
                                capturedGroupIndex = groupIndex
                                capturedGroupPattern = groups[1][1][1:-1] if len(groups) >= 2 else groups[0][1][1:-1]
                                if capturedGroupPattern.startswith("?:"):
                                    capturedGroupPattern = f"({capturedGroupPattern})"
                                result[groupName] = (capturedGroupIndex, isRepeatedGroup, capturedGroupPattern)
                                break
                        if groupName not in result:
                            isRepeatedGroup = False
                            capturedGroupIndex = groups[0][0]
                            capturedGroupPattern = groups[0][1]
                            result[groupName] = (capturedGroupIndex, isRepeatedGroup, capturedGroupPattern)
        except Exception as e:
            result = {}
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result
    
    # Check whether a file is a text file or not with given extensions, the result can't be None
    @staticmethod
    def containKeywords(text, keywords=None):
        result = False
        try:
            if text:
                if keywords != None:
                    result = all(keyword in text for keyword in keywords)
                else:
                    result = True
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Text is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    ### DICTIONARY, LIST, TUPLE API
    # Get intersected list of two lists, the result can't be None
    @staticmethod
    def getIntersectedList(filteredList=None, allList=None):
        result = []
        try:
            result = [] if filteredList == None and allList == None else allList if filteredList == None else [] if allList == None else [item for item in filteredList if item in allList]
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")                
        return result

    # Get unioned dictionary, the result can't be None
    @staticmethod
    def unionedDictionary(dictionaries=None):
        result = {}
        try:
            for key in set().union(*(dictionary for dictionary in dictionaries if dictionary)):
                unionedDictionary = {element for dictionary in dictionaries if dictionary and key in dictionary for element in Helper.getElementSetFromObject(dictionary[key])}
                result[key] = list(unionedDictionary)
        except Exception as e:
            result = {}
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")                
        return result
    
    # Get dictionary from parameter string, return text if not able to get dictionary
    @staticmethod
    def getDictionaryFromParameterString(text=None):
        result = {}
        try:
            if text != None and text.startswith('(') and text.endswith(')'):
                text = text[1:-1]  # Remove surrounding parentheses
                pattern = re.compile(r'(\w+)\s*(?:=\s*(\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}|[^,]+))?')
                for match in pattern.finditer(text):
                    key = match.group(1)
                    value = match.group(2)
                    if value != None and value.strip() == "":
                        value = None
                    else:
                        try:
                            value = ast.literal_eval(value)
                        except (ValueError, SyntaxError):
                            value = None
                    result[key] = value
        except Exception as e:
            result = {}
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")

        # Return the input string if the result is invalid.
        if not result:
            result = text
        return result

    # Get native object from a string, the result can be None
    @staticmethod
    def getNativeObjectFromString(string):
        result = None
        try:
            result = ast.literal_eval(string) # None, boolean True, string "abc123", number 123, bytes b"abc123", tuple(), list[], dict{key:value}, set{}
        except (ValueError, SyntaxError):
            globals = {
                "__builtins__": None,
                "safe_id": lambda x: x,
            }
            try:
                result = eval(string, globals)
            except Exception as e:
                result = Helper.getDictionaryFromParameterString(string) # dict {key:value}, string "abc123", bytes b"abc123"
        return result

    # Get element set from a string: None, boolean True, string "abc123", number 123, bytes b"abc123", tuple(), list[], dict{key:value}, set{}, frozenset(), range()
    @staticmethod
    def getElementSetFromObject(object):
        result = set() # The result can't be None
        try:
            # Convert object to other object types if object is string
            if isinstance(object, str):
                object = Helper.getNativeObjectFromString(object.strip("':."))
            # If object is dict, list, tuple, set, frozenset, range
            if isinstance(object, dict):
                result.update(Helper.getElementSetFromObject(list(object.keys())))
            elif isinstance(object, (list, tuple, set, frozenset, range)):
                for element in object:
                    result.update(Helper.getElementSetFromObject(object=element))
            else: # If object is string, bytes
                result.add(object)
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    ### CONVERT CSV/XLSX
    # Convert attributes to columns and vice verse, the result can't be None
    @staticmethod
    def columnsFromAttributes(attributes):
        result = []
        try:
            if attributes:
                for attribute in attributes:
                    words = []
                    startIndex = 0
                    # Iterate through characters of the camelCase string
                    for i in range(1, len(attribute)):
                        # Check for uppercase letters
                        if attribute[i].isupper():
                            # Extract the word from start_index to i and convert to lowercase
                            words.append(attribute[startIndex:i].capitalize())
                            startIndex = i
                    # Add the last word to the list
                    words.append(attribute[startIndex:].capitalize())
                    # Join words with a space and add to result
                    result.append(" ".join(words))
        except Exception as e:
            result = []
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    @staticmethod
    def attributesFromColumns(columns):
        result = []
        try:
            if columns:
                for words in columns:
                    # Split words by space and convert each word to lowercase except the first one
                    parts = words.split()
                    attribute = parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])
                    result.append(attribute)
        except Exception as e:
            result = []
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Convert rows to objects and vice verse
    @staticmethod
    def rowsFromObjects(columns, objects):
        result = []
        try:
            if objects and columns:
                attributes = Helper.attributesFromColumns(columns)
                for object in objects:
                    row = ["[" + ','.join(getattr(object, attributes[index])) + "]" if isinstance(getattr(object, attributes[index]), list) else getattr(object, attributes[index])
                        for index, column in enumerate(columns)]
                    result.append(row)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Either objects or columns or filePath is invalid.")
        except Exception as e:
            result = []
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    @staticmethod
    def objectsFromRows(cls, columns, rows):
        result = []
        try:
            if cls and columns and rows:
                attributes = Helper.attributesFromColumns(columns)
                for row in rows:
                    cells = {
                        attribute: (
                            None if row[index].strip() == "*"
                            else [value.strip() for value in row[index].strip("[]").split(',')] if row[index].startswith("[") and row[index].endswith("]")
                            else row[index].strip())
                        for index, attribute in enumerate(attributes)
                    }
                    object = cls(**cells)
                    result.append(object)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Either columns or rows is invalid.")
        except Exception as e:
            result = []
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Convert csv to rows and vice verse
    @staticmethod
    def csvFromRows(columns, rows, filePath):
        result = False
        try:
            if columns and rows and filePath:
                with open(filePath, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file, delimiter="\t")
                    writer.writerow(columns)
                    for row in rows:
                        writer.writerow(row)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Either columns or rows or filePath is invalid.")
            result = True
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    @staticmethod
    def rowsFromCSV(filePath):
        columns = []
        rows = []
        try:
            if filePath:
                with open(filePath, mode="r", newline="", encoding="utf-8") as file:
                    reader = csv.reader(file, delimiter="\t")
                    columns = next(reader)
                    for row in reader:
                        rows.append(row)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): FilePath is invalid.")
        except Exception as e:
            columns = []
            rows = []
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return columns, rows

    # Convert objects to csv and vice verse
    @staticmethod
    def objectsFromCSV(cls, filePath):
        columns, rows = Helper.rowsFromCSV(filePath)
        return Helper.objectsFromRows(cls=cls, columns=columns, rows=rows)

    @staticmethod
    def csvFromObjects(columns, objects, filePath):
        rows = Helper.rowsFromObjects(columns=columns, objects=objects)
        return Helper.csvFromRows(columns=columns, rows=rows, filePath=filePath)

    # Convert between xlsx <=> rows
    @staticmethod
    def xlsxFromRows(columns, rows, filePath):
        result = False
        try:
            if columns and rows and filePath:
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                sheet.title = "Data"
                for columnIndex, column in enumerate(columns, start=1):
                    sheet.cell(row=1, column=columnIndex, value=column)
                for rowIndex, row in enumerate(rows, start=2):
                    for columnIndex, cell in enumerate(row, start=1):
                        sheet.cell(row=rowIndex, column=columnIndex, value=cell)
                workbook.save(filePath)
                result = True
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Either columns or rows or filePath is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    @staticmethod
    def rowsFromXLSX(filePath):
        columns = []
        rows = []
        try:
            if filePath:
                workbook = openpyxl.load_workbook(filePath)
                sheet = workbook.active
                columns = [sheet.cell(row=1, column=columnIndex).value for columnIndex in range(1, sheet.max_column + 1)]
                for row_index in range(2, sheet.max_row + 1):
                    row = [sheet.cell(row=row_index, column=columnIndex).value for columnIndex in range(1, sheet.max_column + 1)]
                    rows.append(row)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): FilePath is invalid.")
        except Exception as e:
            columns = []
            rows = []
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return columns, rows

    # Convert between xlsx <=> rows
    @staticmethod
    def objectsFromXLSX(cls, filePath):
        columns, rows = Helper.rowsFromXLSX(filePath)
        return Helper.objectsFromRows(cls=cls, columns=columns, rows=rows)

    @staticmethod
    def XLSXFromObjects(columns, objects, filePath):
        rows = Helper.rowsFromObjects(columns=columns, objects=objects)
        return Helper.xlsxFromRows(columns=columns, rows=rows, filePath=filePath)

    ### FILE API
    # Get all file paths from a path and file extensions recursively
    @staticmethod
    def getFilePaths(path=".\\repos\\", extensions=None, languages=None, frameworks=None, apiTypes=None):
        result = {}
        try:
            if path and os.path.exists(path):
                # Get intersected extensions
                allExtensions = list(Helper.config["extensions"].keys())
                intersectedExtensions = set(Helper.getIntersectedList(filteredList=extensions, allList=allExtensions))

                for root, dirs, files in os.walk(path):
                    for file in files:
                        # If the file extension is valid
                        extension = "." + file.split('.')[-1]
                        if extension in intersectedExtensions:
                            languageDictBackup = Helper.config["extensions"][extension]
                            languageDict = dict(languageDictBackup)
                            for language, frameworkDict in languageDictBackup.items():
                                if languages == None or language in languages:
                                    for framework, apiTypeDict in frameworkDict.items():
                                        if frameworks == None or framework in frameworks:
                                            for apiType, pattern in apiTypeDict.items():
                                                if apiTypes == None or apiType in apiTypes:
                                                    pass
                                                else:
                                                    languageDict[language][framework].pop(apiType, None)
                                        else:
                                            languageDict[language].pop(framework, None)
                                else:
                                    languageDict.pop(language, None)
                            filePath = os.path.join(root, file)
                            result[filePath] = (extension, languageDict)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Path {path} is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Check whether a file is a text file or not with given extensions
    @staticmethod
    def isTextFile(filePath, blockSize=512):
        result = False
        try:
            if filePath and blockSize and os.path.exists(filePath):
                with open(filePath, "rb") as file:
                    chunk = file.read(blockSize)
                    if chunk:
                        textCharacters = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
                        result = all(b in textCharacters for b in chunk)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Either filePath or Blocksize is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Change files permissions
    @staticmethod
    def chmodFileFolder(path, mode):
        result = False
        try:
            if path and mode:
                for root, dirs, files in os.walk(path):
                    for dir in dirs:
                        dirPath = os.path.join(root, dir)
                        os.chmod(dirPath, mode)
                    for file in files:
                        filePath = os.path.join(root, file)
                        os.chmod(filePath, mode)
                result = True
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Either path or mode is invalid")
        except subprocess.CalledProcessError as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Remove files recursively
    @staticmethod
    def removeFileOrFolder(path):
        result = None
        try:
            if path and os.path.exists(path):
                Helper.chmodFileFolder(path, 0o777)
                if os.name == "nt":
                    result = subprocess.run(['rmdir', '/S', '/Q', path], check=True, shell=True)
                else:
                    result = subprocess.run(['rm', '-rf', path], check=True)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Path {path} is invalid.")
        except subprocess.CalledProcessError as e:
            result = None
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Download repo with (username, repo, branch) by GitPython to a local path, vincentsingularity is a private organizer or collaborator
    @staticmethod
    def downloadRepoByGitPython(url, username, password=None, repository=None, branches=None, path=".\\reposcan\\repos\\", downloadNew = True):
        result = None
        try:
            # Load git locally first if download new is False
            try:
                if not downloadNew:
                    result = git.Repo(path=path)
            except Exception as e:
                result = None

            if url and username:
                # Load git remotely if loading locally is False
                if not result:
                    # Remove repo folder
                    Helper.removeFileOrFolder(path=path)

                    # Clone branches
                    if password:
                        repoUrl = f'https://{username}:{password}@github.com/{username}/{repository}.git'
                    else:
                        repoUrl = f'https://github.com/{username}/{repository}.git'
                    result = git.Repo.clone_from(url=repoUrl, to_path=path)

                    # Fetch branches
                    if branches == None:
                        result.remotes.origin.fetch()
                    else:
                        for branch in branches:
                            result.remotes.origin.fetch(branch)
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): All files from repository '{username}/{repository}' (branch: {branches}) downloaded to: {path}")
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Either url or username or repo is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    ### FILE SCANNER
    # Get all file paths from a path and file extensions recursively
    @staticmethod
    def getAPIMatchResult(apiMatch, linePatterns, secondSeparatorParts):
        result = {}
        try:
            if apiMatch and linePatterns and secondSeparatorParts:
                # Extract apiText by separators
                secondSeparatorPartLength = len(apiMatch.groupdict()["secondSeparatorPart"]) if apiMatch.groupdict()["secondSeparatorPart"] else 0
                apiText = secondSeparatorParts[0] + apiMatch.group(0)[:len(apiMatch.group(0)) - secondSeparatorPartLength]
                secondSeparatorParts[:] = [apiMatch.groupdict()["secondSeparatorPart"]]

                # Loop all line patterns, skip the last separator line
                for linePattern in linePatterns[:-1]:
                    # Get all line matches
                    lineMatches = re.findall(linePattern, apiText)
                    capturePatternGroupsByName = Helper.getCapturedGroupsByName(linePattern)

                    # Loop all line matches
                    for lineMatch in lineMatches:
                        # Convert lineMatch to a list when it is an element
                        if not isinstance(lineMatch, (list, tuple, set, frozenset, range)):
                            lineMatch = [lineMatch]

                        # Loop all groups
                        for groupName, (groupIndex, isRepeatedGroup, groupPattern) in capturePatternGroupsByName.items():
                            # Replace the number if group name ends with a number such as: 
                            groupName = re.sub(r'\d+$', '', groupName)

                            # Two cases of a group: repeated and not repeated
                            if isRepeatedGroup:
                                groups = list({
                                            item if isinstance(group, (list, tuple, set, frozenset, range)) else group
                                            for group in re.findall(groupPattern, lineMatch[groupIndex - 1])
                                            for item in (group if isinstance(group, (list, tuple, set, frozenset, range)) else [group])
                                            if item
                                            })
                                if groupName not in result:
                                    result[groupName] = groups
                                else:
                                    result[groupName].extend(groups)
                            else:
                                if lineMatch[groupIndex - 1]:
                                    if groupName not in result:
                                        result[groupName] = [lineMatch[groupIndex - 1]]
                                    else:
                                        result[groupName].append(lineMatch[groupIndex - 1])
        except Exception as e:
            result = {}
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result