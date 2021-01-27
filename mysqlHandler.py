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