
def DeleteQuery(schema, record, table):
    query = "DELETE FROM {} WHERE ".format(table)
    for index, value in enumerate(record):
        if str(value) == 'None':
            continue

        if index > 0:
            query += " AND "
        if 'varchar' in schema[index][1]:
            queryFormatter = "{}='{}'"
        else:
            queryFormatter = "{}={}"

        query += queryFormatter.format(str(schema[index][0]), str(value))

    query += ";"
    return query
