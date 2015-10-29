def DeleteQuery(schema, record, table):
    query = "DELETE FROM {} WHERE ".format(table)
    for index, value in enumerate(record):
        if str(value) == 'None':
            continue

        if index > 0:
            query += " AND "
        if 'varchar' in schema[index][1] or 'character' in schema[index][1]:
            queryFormatter = "{}='{}'"
        else:
            queryFormatter = "{}={}"

        query += queryFormatter.format(str(schema[index][0]), str(value))

    query += ";"
    return query

def InsertQuery(schema, values, table):
    query = "INSERT INTO {} ".format(table)
    cols = "("
    vals = "("
    for index, column in enumerate(schema):
        if values[column[0]] is None:
            break
        cols += "{}".format(column[0])
        if type(values[column[0]]) is str:
            vals += "'{}'".format(str(values[column[0]]))
        else:
            vals += "{}".format(values[column[0]])
        cols += ", "
        vals += ", "

    cols = cols[:-2]
    vals = vals[:-2]

    cols += ")"
    vals += ")"
    query = "{}{} VALUES {};".format(query, cols, vals)
    return query
