import os, sys, inspect
from time import time
from .helpers.Helper import Helper
from .models.RepoInfo import RepoInfo
from .exporters.CSVExporter import CSVExporter
from .exporters.XLSXExporter import XLSXExporter
from .scanners.CSharpScanner import CSharpScanner
from .scanners.JavaScanner import JavaScanner
from .scanners.PythonScanner import PythonScanner

SCANNERSBYEXTENSION = {
    '.cs' : CSharpScanner(),
    '.java': JavaScanner(),
    '.py' : PythonScanner()
}
EXPORTERSBYEXTENSION = {
    '.csv' : CSVExporter(),
    '.xlsx': XLSXExporter()
}
class RepoScan:
    def __init__(self):
        try:
            # Init default properties
            self.apiInfos = []
            self.apiSummaryInfos = {}
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")

    # Get api info from a repo url by GitPython
    def addAPIInfoFromRepoUrlByGitPython(self, url, username, password=None, repositories=None, branches=None, path=".\\repos\\", extensions=None, languages=None, frameworks=None, apiTypes=None, keywords=None):
        try:
            if url and username:
                # Get intersect repositories
                allRepositories = Helper.getRepositories(url=url, username=username, password=password)
                intersectedRepositories = set(Helper.getIntersectedList(filteredList=repositories, allList=allRepositories))
                for repository in intersectedRepositories:
                    repoPath = os.path.join(path, repository)
                    gitRepo = Helper.downloadRepoByGitPython(url=url, username=username, password=password, repository=repository, branches=branches, path=repoPath, downloadNew=False)
                    if gitRepo:
                        # Get intersected branches
                        (project, domain, allBranches) = Helper.getRepository(url=url, username=username, password=password, repository=repository)
                        intersectedBranches = set(Helper.getIntersectedList(filteredList=branches, allList=allBranches))
                        for branch in intersectedBranches:
                            gitRepo.git.checkout(branch)
                            self.addAPIInfoFromLocalPath(scanType="RepoScan", project=project, domain=domain, repository=repository, branch=branch, path=repoPath, extensions=extensions, languages=languages, frameworks=frameworks, apiTypes=apiTypes, keywords=keywords)
                    else:
                        Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Either url={url} username={username} repository={repository} username={username} password={password} is invalid.")
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Either url or username or repo is invalid.")                        
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return self.apiInfos, self.apiSummaryInfos

    # Get api info from a local path
    def addAPIInfoFromLocalPath(self, scanType=None, project=None, domain=None, repository=None, branch=None, path=".\\repos\\", extensions = None, languages = None, frameworks = None, apiTypes = None, keywords = None):
        try:
            if path:
                filePaths = Helper.getFilePaths(path=path, extensions=extensions, languages=languages, frameworks=frameworks, apiTypes=apiTypes)
                for filePath, (extension, languageDict) in filePaths.items():
                    apiInfos, apiSummaryInfos = SCANNERSBYEXTENSION[extension].addAPIInfosAndAPISummaryInfos(scanType=scanType, project=project, domain=domain, repository=repository, branch=branch, filePath=filePath, extension=extension, languageDict=languageDict, keywords=keywords)
                    self.apiInfos.extend(apiInfos)
                    if apiSummaryInfos:
                        self.apiSummaryInfos[filePath] = apiSummaryInfos
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Path {path} is invalid.") 
        except Exception as e:
            self.apiInfos = None
            self.apiSummaryInfos = None
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return self.apiInfos, self.apiSummaryInfos

    # Get api infos from repo list in an input file
    def addAPIInfosFromRepoUrls(self, repoFilePath="\\data\\repos.csv"):
        try:
            repos = RepoInfo.objectsFromCSV(filePath=repoFilePath)
            if repos:
                for repo in repos:
                    self.addAPIInfoFromRepoUrlByGitPython(url=repo.url, username=repo.username, password=repo.password, repositories=repo.repositories, branches=repo.branches, path=repo.path, languages=repo.languages, extensions=repo.extensions, apiTypes=repo.apiTypes, keywords=repo.keywords)
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Repos is invalid.")
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return self.apiInfos, self.apiSummaryInfos

    # Extract api info to an output file
    def exportFile(self, apiFilePath='.\\data\\output.csv'):
        result = False
        try:
            if apiFilePath:
                fileExtension = "." + apiFilePath.split('.')[-1]
                exporter = EXPORTERSBYEXTENSION[fileExtension]
                if exporter:
                    exporter.extractToFile(columns=Helper.config["exporterColumns"], apiInfos=self.apiInfos, filePath=apiFilePath)
                    result = True
            else:
                Helper.LOGGER.info(f"{inspect.currentframe().f_code.co_name}(): Filepath is invalid.") 
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

    # Get api infos from repo list in a repo file then extract api infos to an api file
    def repoScan(self, configFilePath=".\\data\\config.json", repoFilePath=".\\data\\repo.csv", apiFilePath=".\\data\\api.csv", apiSummaryFilePath=".\\data\\summaryapi.csv"):
        result = False
        try:
            Helper.config = Helper.jsonObjectFromJsonFile(configFilePath)
            Helper.initLogger(logLevel=Helper.config["logLevel"], logFilePath=Helper.config["logFilePath"], clearLog=True)
            self.addAPIInfosFromRepoUrls(repoFilePath)
            self.exportFile(apiFilePath)
            Helper.jsonFileFromJsonObject(jsonObject=self.apiSummaryInfos, filePath=apiSummaryFilePath)
            result = True
        except Exception as e:
            Helper.LOGGER.error(f"{inspect.currentframe().f_code.co_name}(): {e}.")
        return result

# Main function
if __name__ == "__main__":
    t0 = time()
    print(r"==================================================================================================================")
    print(r"Command usage: reposcan.py <configFilePath> <repoFilePath> <apiFilePath> <apiSummaryFilePath>")
    print(r"1. Windows example: reposcan.py .\data\config.json .\data\repo.csv .\data\api.csv .\data\apisummary.json")
    print(r"2. Linux example: reposcan.py ./data/config.json ./data/repo.csv ./data/api.csv ./data/apisummary.json")

    numberOfParameters = len(sys.argv) - 1
    # Default parameter values
    configFilePath = None
    repoFilePath = None
    apiFilePath = None
    apiSummaryFilePath = None
    if numberOfParameters < 4:
        configFilePath = ".\\data\\config.json"
        repoFilePath = ".\\data\\repo.csv"
        apiFilePath = ".\\data\\api.csv"
        apiSummaryFilePath = ".\\data\\apisummary.json"
    else:
        configFilePath = sys.argv[1]
        repoFilePath = sys.argv[2]
        apiFilePath = sys.argv[3]
        apiSummaryFilePath = sys.argv[4]

    # Convert to the correct paths
    configFilePath = Helper.getPath(configFilePath)
    repoFilePath = Helper.getPath(repoFilePath)
    apiFilePath = Helper.getPath(apiFilePath)
    apiSummaryFilePath = Helper.getPath(apiSummaryFilePath)

    # Execute the app
    print(f"Executed command: reposcan.py {configFilePath} {repoFilePath} {apiFilePath} {apiSummaryFilePath}\n")
    repoScan = RepoScan()
    repoScan.repoScan(configFilePath=configFilePath, repoFilePath=repoFilePath, apiFilePath=apiFilePath, apiSummaryFilePath=apiSummaryFilePath)
    t1 = time()
    Helper.LOGGER.info(f"It takes {t1 - t0:.2f}s to execute")
    print(r"==================================================================================================================")
