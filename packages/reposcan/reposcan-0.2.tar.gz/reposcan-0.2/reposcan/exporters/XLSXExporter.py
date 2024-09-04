from .FileExporter import FileExporter
from ..helpers.Helper import Helper

class XLSXExporter(FileExporter):
    def extractToFile(self, columns, apiInfos, filePath):
        return Helper.XLSXFromObjects(columns=columns, objects=apiInfos, filePath=filePath)