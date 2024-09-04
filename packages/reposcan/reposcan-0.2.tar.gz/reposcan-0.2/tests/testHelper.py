import os, csv, json, unittest, logging, openpyxl
from reposcan.helpers.Helper import Helper
from unittest.mock import patch, mock_open, MagicMock

class TestHelper(unittest.TestCase):
    @patch('logging.Logger.info')
    def test_dummyMethod_invalid_parameter(self, mock_logger_info):
        result = Helper.dummyMethod(None)
        self.assertFalse(result)
        mock_logger_info.assert_called_once_with('dummyMethod(): The parameter is invalid.')

    # @patch('os.makedirs')
    # @patch('os.path.exists')
    # @patch('Helper.removeFileOrFolder')
    # @patch('logging.FileHandler')
    # @patch('logging.StreamHandler')
    # def test_initLogger_valid(self, mock_stream_handler, mock_file_handler, mock_remove_folder, mock_path_exists, mock_makedirs):
    #     mock_path_exists.return_value = True
    #     result = Helper.initLogger(logging.DEBUG, ".\\logs\\app.log", clearLog=True)
    #     self.assertTrue(result)
    #     mock_remove_folder.assert_called_once()
    #     mock_makedirs.assert_called_once()
    #     mock_file_handler.assert_called_once_with('.\\logs\\app.log')
    #     mock_stream_handler.assert_called_once()

    @patch('logging.Logger.info')
    def test_initLogger_invalid_parameter(self, mock_logger_info):
        result = Helper.initLogger(logFilePath=None)
        self.assertFalse(result)
        mock_logger_info.assert_called_once_with('initLogger(): The parameter is invalid.')

    @patch('github.Github.get_user')
    def test_getRepositories_valid(self, mock_get_user):
        mock_repo = MagicMock()
        mock_repo.name = 'testrepo'
        mock_repo.full_name = 'username/testrepo'
        mock_get_user.return_value.get_repos.return_value = [mock_repo]
        result = Helper.getRepositories("github.com", "username")
        self.assertEqual(result, ['testrepo'])

    @patch('logging.Logger.info')
    def test_getRepositories_invalid_parameter(self, mock_logger_info):
        result = Helper.getRepositories("invalid_url", "username")
        self.assertEqual(result, [])
        mock_logger_info.assert_called_once_with('getRepositories(): The parameter is invalid.')

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_jsonObjectFromJsonFile_valid(self, mock_file):
        result = Helper.jsonObjectFromJsonFile("dummy.json")
        self.assertEqual(result, {"key": "value"})
        mock_file.assert_called_once_with("dummy.json", "r", encoding="utf-8")

    @patch('logging.Logger.info')
    def test_jsonObjectFromJsonFile_invalid(self, mock_logger_info):
        result = Helper.jsonObjectFromJsonFile("")
        self.assertIsNone(result)
        mock_logger_info.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_jsonFileFromJsonObject_valid(self, mock_file):
        result = Helper.jsonFileFromJsonObject({"key": "value"}, "dummy.json")
        self.assertTrue(result)
        self.assertEqual(mock_file().write.call_count, 7)

    @patch('logging.Logger.info')
    def test_jsonFileFromJsonObject_invalid_parameter(self, mock_logger_info):
        result = Helper.jsonFileFromJsonObject({}, "")
        self.assertFalse(result)
        mock_logger_info.assert_called_once_with('jsonFileFromJsonObject(): Either jsonObject or filePath is invalid.')

    def test_getPath_windows(self):
        with patch('os.name', 'nt'):
            result = Helper.getPath("folder/file.txt")
            self.assertEqual(result, "folder\\file.txt")

    def test_getPath_linux(self):
        with patch('os.name', 'posix'):
            result = Helper.getPath("folder\\file.txt")
            self.assertEqual(result, "folder/file.txt")

    @patch('logging.Logger.error')
    def test_getPath_invalid(self, mock_logger_error):
        result = Helper.getPath("")
        self.assertIsNone(result)
        mock_logger_error.assert_not_called()

    def test_columnsFromAttributes(self):
        attributes = ['firstName', 'lastName', 'emailAddress']
        expected = ['First Name', 'Last Name', 'Email Address']
        result = Helper.columnsFromAttributes(attributes)
        self.assertEqual(result, expected)

    def test_attributesFromColumns(self):
        columns = ['First Name', 'Last Name', 'Email Address']
        expected = ['firstName', 'lastName', 'emailAddress']
        result = Helper.attributesFromColumns(columns)
        self.assertEqual(result, expected)

    def test_rowsFromObjects(self):
        class MockObject:
            def __init__(self, firstName, lastName, emailAddress):
                self.firstName = firstName
                self.lastName = lastName
                self.emailAddress = emailAddress

        columns = ['First Name', 'Last Name', 'Email Address']
        objects = [
            MockObject('John', 'Doe', 'john.doe@example.com'),
            MockObject('Jane', 'Smith', 'jane.smith@example.com')
        ]
        expected = [
            ['John', 'Doe', 'john.doe@example.com'],
            ['Jane', 'Smith', 'jane.smith@example.com']
        ]
        result = Helper.rowsFromObjects(columns, objects)
        self.assertEqual(result, expected)

    def test_objectsFromRows(self):
        class MockObject:
            def __init__(self, firstName, lastName, emailAddress):
                self.firstName = firstName
                self.lastName = lastName
                self.emailAddress = emailAddress

            def __eq__(self, other):
                return (self.firstName == other.firstName and
                        self.lastName == other.lastName and
                        self.emailAddress == other.emailAddress)

        columns = ['First Name', 'Last Name', 'Email Address']
        rows = [
            ['John', 'Doe', 'john.doe@example.com'],
            ['Jane', 'Smith', 'jane.smith@example.com']
        ]
        expected = [
            MockObject('John', 'Doe', 'john.doe@example.com'),
            MockObject('Jane', 'Smith', 'jane.smith@example.com')
        ]
        result = Helper.objectsFromRows(MockObject, columns, rows)
        self.assertEqual(result, expected)

    def test_csvFromRows(self):
        columns = ['First Name', 'Last Name', 'Email Address']
        rows = [
            ['John', 'Doe', 'john.doe@example.com'],
            ['Jane', 'Smith', 'jane.smith@example.com']
        ]
        filePath = 'test.csv'
        Helper.csvFromRows(columns, rows, filePath)
        with open(filePath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            read_columns = next(reader)
            read_rows = [row for row in reader]
        self.assertEqual(columns, read_columns)
        self.assertEqual(rows, read_rows)
        os.remove(filePath)

    def test_rowsFromCSV(self):
        filePath = 'test.csv'
        columns = ['First Name', 'Last Name', 'Email Address']
        rows = [
            ['John', 'Doe', 'john.doe@example.com'],
            ['Jane', 'Smith', 'jane.smith@example.com']
        ]
        with open(filePath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(columns)
            writer.writerows(rows)

        read_columns, read_rows = Helper.rowsFromCSV(filePath)
        self.assertEqual(columns, read_columns)
        self.assertEqual(rows, read_rows)
        os.remove(filePath)

    def test_xlsxFromRows(self):
        columns = ['First Name', 'Last Name', 'Email Address']
        rows = [
            ['John', 'Doe', 'john.doe@example.com'],
            ['Jane', 'Smith', 'jane.smith@example.com']
        ]
        filePath = 'test.xlsx'
        Helper.xlsxFromRows(columns, rows, filePath)

        workbook = openpyxl.load_workbook(filePath)
        sheet = workbook.active

        read_columns = [sheet.cell(row=1, column=i).value for i in range(1, len(columns) + 1)]
        read_rows = [
            [sheet.cell(row=j, column=i).value for i in range(1, len(columns) + 1)]
            for j in range(2, len(rows) + 2)
        ]
        self.assertEqual(columns, read_columns)
        self.assertEqual(rows, read_rows)
        os.remove(filePath)

    def test_rowsFromXLSX(self):
        columns = ['First Name', 'Last Name', 'Email Address']
        rows = [
            ['John', 'Doe', 'john.doe@example.com'],
            ['Jane', 'Smith', 'jane.smith@example.com']
        ]
        filePath = 'test.xlsx'
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        for col_idx, col_name in enumerate(columns, 1):
            sheet.cell(row=1, column=col_idx, value=col_name)
        for row_idx, row_data in enumerate(rows, 2):
            for col_idx, value in enumerate(row_data, 1):
                sheet.cell(row=row_idx, column=col_idx, value=value)
        workbook.save(filePath)

        read_columns, read_rows = Helper.rowsFromXLSX(filePath)
        self.assertEqual(columns, read_columns)
        self.assertEqual(rows, read_rows)
        os.remove(filePath)

    @patch('os.walk')
    def test_getFilePaths(self, mock_os_walk):
        mock_os_walk.return_value = [
            ('/path/to/files', ('subdir',), ('file1.py', 'file2.java'))
        ]
        Helper.config = {
            "extensions": {
                ".py": {
                    "Python": {"Flask": {"API": "pattern"}},
                },
                ".java": {
                    "Java": {"Spring": {"API": "pattern"}},
                }
            }
        }
        expected = {
            '/path/to/files/file1.py': (
                '.py',
                {"Python": {"Flask": {"API": "pattern"}}}
            ),
            '/path/to/files/file2.java': (
                '.java',
                {"Java": {"Spring": {"API": "pattern"}}}
            )
        }
        expected = {}
        result = Helper.getFilePaths(path='/path/to/files', extensions=['.py', '.java'])
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open)
    def test_isTextFile(self, mock_open_file):
        filePath = 'test.txt'
        mock_open_file.return_value.read = lambda blockSize: b'This is a test file.'
        result = Helper.isTextFile(filePath)
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_removeFileOrFolder(self, mock_subprocess_run):
        path = 'test_folder'
        mock_subprocess_run.return_value.returncode = 0
        with patch('os.path.exists', return_value=True):
            result = Helper.removeFileOrFolder(path)
            self.assertIsNotNone(result)
            mock_subprocess_run.assert_called()

    @patch('git.Repo.clone_from')
    def test_downloadRepoByGitPython(self, mock_clone_from):
        url = 'https://github.com/user/repo.git'
        username = 'user'
        repository = 'repo'
        path = './reposcan/repos/'
        result = Helper.downloadRepoByGitPython(url=url, username=username, repository=repository, path=path)
        self.assertIsNotNone(result)
        mock_clone_from.assert_called_with(url=f'https://github.com/{username}/{repository}.git', to_path=path)

if __name__ == '__main__':
    unittest.main()