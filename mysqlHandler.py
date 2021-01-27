from flaskext.mysql import MySQL

mysql = MySQL()

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