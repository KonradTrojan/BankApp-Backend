from flaskext.mysql import MySQL
from flask import jsonify
mysql = MySQL()

# zwraca listę wszystkich kont przypisanych do danego idCustomer
def get_active_idAccounts_Of_Customer(idCustomer):
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

def get_all_idAccounts_of_Customer(idCustomer):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """select idAccounts from allOwners where idCustomers= %s """
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

    # transakcje, w której zalogowany jest nadawcą przelewu
    sql = """select idTransactions  from transactions where idAccounts= %s """
    cursor.execute(sql, [idAccount])
    data = cursor.fetchall()

    transactionsID = []
    for row in data:
        transactionsID.append(row[0])

    # transakcje, w której zalogowany jest odbiorcą przelewu
    sql = """select idTransactions  from transactions where idAccountsOfRecipient= %s """
    cursor.execute(sql, [idAccount])
    data = cursor.fetchall()

    for row in data:
        transactionsID.append(row[0])

    return transactionsID

# funkcja zwraca True jeśli podane konto należy do zalogowanego użytkownika
def isOwner(identity, idAcounts):
    for id in get_active_idAccounts_Of_Customer(identity):
        if id == idAcounts:
            return True
    return False

def accountNumToAccountID(accountNum):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = """select idAccounts from accounts where number= %s """
        cursor.execute(sql, [accountNum])
        data = cursor.fetchone()

        return data[0]
    except IndexError:
        return None

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