from .FileScanner import FileScanner

class JavaScanner(FileScanner):
    def addAPIInfosAndAPISummaryInfos(self, scanType="", project="", domain="", repository="", branch="", filePath="", extension="", languageDict={}, keywords=[]):
        return super().addAPIInfosAndAPISummaryInfos(scanType=scanType, project=project, domain=domain, repository=repository, branch=branch, filePath=filePath, extension=extension, languageDict=languageDict, keywords=keywords)