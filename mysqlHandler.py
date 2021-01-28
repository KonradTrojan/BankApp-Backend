from flaskext.mysql import MySQL
from flask import jsonify
mysql = MySQL()

# zwraca listę wszystkich kont przypisanych do danego idCustomer
def getIdsAccountsOfCustomer(idCustomer):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """select idAccounts from owners where idCustomers= %s """
    cursor.execute(sql, [idCustomer])
    data = cursor.fetchall()

    # wpisanie do tablicy id wszystkich kont zalogowanego użytkownika
    accountsIDs = []
    for row in data:
        accountsIDs.append(row[0])

    return accountsIDs


# zwraca listę wszystkich kart przypisanych do danego idAccount
def getIdsCreditCardsOfAccount(idAccount):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """select idCreditCards from credit_cards where idAccounts= %s """
    cursor.execute(sql, [idAccount])
    data = cursor.fetchall()

    # wpisanie do tablicy id wszystkich kont zalogowanego użytkownika
    cardsID = []
    for row in data:
        cardsID.append(row[0])

    return cardsID


# zwraca listę wszystkich transakcji przypisanych do danego idAccount
def getIdsTransferOfAccount(idAccount):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """select idTransactions  from transactions where idAccounts= %s """
    cursor.execute(sql, [idAccount])
    data = cursor.fetchall()

    transactionsID = []
    for row in data:
        transactionsID.append(row[0])

    return transactionsID

# funkcja zwraca True jeśli podane konto należy do zalogowanego użytkownika
def isOwner(identity, idAcounts):
    for id in getIdsAccountsOfCustomer(identity):
        if id == idAcounts:
            return True
    return False

def accountNumToAccountID(accountNum):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = """select idAccounts from accounts where number= %s """
        cursor.execute(sql, [accountNum])
        data = cursor.fetchall()

        return data[0]
    except IndexError:
        return []

def hasMoney(accountsId, amount):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """select balance from accounts where idAccounts = %s """
    cursor.execute(sql, [accountsId])
    data = cursor.fetchone()

    balance = float(data[0])
    if balance - amount >= 0:
        return True
    else:
        return False