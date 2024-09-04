from ..helpers.Helper import Helper

class RepoInfo:
    def __init__(self, url, username, password=None, repositories=None, branches=None, path="\\repos\\", extensions=None, languages=None, frameworks=None, apiTypes=None, keywords=None):
        self.url = url  # The URL
        self.username = username  # The username
        self.password = password  # The password
        self.repositories = repositories  # The repositories
        self.branches = branches  # The branches

        self.path = path  # The local path where the repositories are downloaded to
        self.extensions = extensions # The file extensions
        self.languages = languages  # The programming languages
        self.frameworks = frameworks  # The frameworks
        self.apiTypes = apiTypes # The api types
        self.keywords = keywords # The keywords

    @classmethod
    def objectsFromCSV(cls, filePath=".\\data\\output.csv"):
        return Helper.objectsFromCSV(cls=cls, filePath=filePath)