import re

from helpers.Helper import Helper

text = """
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/tag/<pathParameter1>')
# Just comment
@app.route('/tag/<pathParameter1>/page-<int:pathParameter2>', methods=['GET', 'POST'])
@app.route('/tag/<pathParameter1>/page-<int:pathParameter2>/xyz', methods=['GET'])
def test1(pathParameter1, pathParameter2):
    # Query parameters
    queryParameter1 = request.args.get('queryParameter1')
    queryParameter2 = request.args.get('queryParameter2')

    # Header parameters
    headerParameter1 = request.headers.get('headerParameter1')
    headerParameter2 = request.headers.get('headerParameter2')

    # Body parameters
    bodyParameter1 = request.get_json().get('bodyParameter1')
    bodyParameter2 = request.get_json().get('bodyParameter2')

    # Content types and response codes
    if request.content_type == 'application/xml':
        return "<response><message>XML format</message></response>", 415  # Return XML response
    elif request.content_type == 'application/html':
        return "<response><message>XML format</message></response>", 200  # Return XML response        
    else:
        return jsonify(incomes='data', 200)  # Replace with actual data

@app.route('/tag')
def test2():
    return '', 200

if __name__ == '__main__':
    app.run()

"""
text1 = """
from flask_python import Flask, jsonify, request

from cashman.model.expense import Expense, ExpenseSchema
from cashman.model.income import Income, IncomeSchema
from cashman.model.transaction_type import TransactionType

app = Flask(__name__)

transactions = [
    Income('Salary', 5000),
    Income('Dividends', 200),
    Expense('pizza', 50),
    Expense('Rock Concert', 100)
]


@app.route('/incomes')
def get_incomes():
    schema = IncomeSchema(many=True)
    incomes = schema.dump(
        filter(lambda t: t.type == TransactionType.INCOME, transactions)
    )
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    income = IncomeSchema().load(request.get_json())
    transactions.append(income)
    return "", 204


@app.route('/expenses')
def get_expenses():
    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
    )
    return jsonify(expenses)


@app.route('/expenses', methods=['POST'])
def add_expense():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense)
    return "", 204


if __name__ == "__main__":
    app.run()

"""
apiPattern = r'''((?:@app\.route\(['"](?P<paths>[^'"]+)['"](.*?, methods=(?P<httpMethods>\[.*\]))?.*\)\n)|(?:def (?P<functionName>\w+) (?P<pathParameters>\(.*\)):\n)|(?:request.args.get(?P<queryParameters>.*)\n)|(?:request.headers.get(?P<headerParameters>.*)\n)|(?:request.get_json\(\).get(?P<bodyParameters>.*)\n)|(?:request.content_type == (?P<contentTypes>.*)\n)|(?:return .*, (?P<responseCodes>\d+).*\n)|.*?\n)*?(?:(?:(?P<firstSeparatorPart>.*\n\n)(?P<secondSeparatorPart>@app\.route))|\Z)'''

# Loop all api matches
apiMatches = re.finditer(apiPattern, text)
apiMatches = [apiMatch for apiMatch in apiMatches if apiMatch.group(0).strip() != ""]
linePatterns = Helper.getLinePatterns(apiPattern)
secondSeparatorParts= [""]
for apiMatch in apiMatches:
    apiMatchResult = Helper.getAPIMatchResult(apiMatch, linePatterns, secondSeparatorParts)
    if apiMatchResult and ("paths" in apiMatchResult or "httpMethods" in apiMatchResult):
        print(apiMatchResult)
