from abc import ABC, abstractmethod

class FileExporter(ABC):
    @abstractmethod
    def extractToFile(self, columns, rows, filePath):
        pass