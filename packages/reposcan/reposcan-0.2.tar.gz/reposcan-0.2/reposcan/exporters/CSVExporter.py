from .FileExporter import FileExporter
from ..helpers.Helper import Helper

class CSVExporter(FileExporter):
    def extractToFile(self, columns, apiInfos, filePath):
        return Helper.csvFromObjects(columns=columns, objects=apiInfos, filePath=filePath)