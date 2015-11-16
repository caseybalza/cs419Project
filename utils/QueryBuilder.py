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
            continue
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

def UpdateQuery(schema, values, record, table):
    query = "UPDATE {} SET ".format(table)

    for index, column in enumerate(schema):
        if type(record[index]) is str:
            queryFormatter = "{}='{}', "
        else:
            queryFormatter = "{}={}, "

        if values[column[0]] is None:
            if record[index] is not None:
                query += queryFormatter.format(str(column[0]), str(record[index]))
        else:
            query += queryFormatter.format(str(column[0]), str(values[column[0]]))

    query = query[:-2]
    query += " WHERE "

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

def CreateTable(db, name, columns):
	query = 'CREATE TABLE '+db+'.`'+name+'` ( '
	
	if isinstance(columns[0], str):
		query += '`'+columns[0]+'` '	#add name of column
		query +=columns[1]			#add type of column
		query +='( '+columns[2]+' ) '	#add size of column
		if columns[4] !='':
			query +=columns[4]		#add attributes of column
		if columns[3] !='':
			query +=' COLLATE '+columns[3]	#add collation of column
		if columns[5]:				#add NULL or NOT NULL to column
			query +=' NULL'
		else:
			query +=' NOT NULL'
		if columns[7]:
			query += ' AUTO_INCREMENT'
		if columns[6] != '':
			query += ' DEFAULT \''+columns[6]+'\''
		if columns[8] is not 'NONE':			#add special characteristic of column
			query += ' '+columns[8]
		query +=', '
		query = query[:-2]#remove last comma from list of columns
	else:
		for i in columns:
			query += '`'+i[0]+'` '	#add name of column
			query +=i[1]			#add type of column
			query +='( '+i[2]+' ) '	#add size of column
			if i[4] !='':
				query +=i[4]		#add attributes of column
			if i[3] !='':
				query +=' COLLATE '+i[3]	#add collation of column
			if i[5]:				#add NULL or NOT NULL to column
				query +=' NULL'
			else:
				query +=' NOT NULL'
			if i[7]:
				query += ' AUTO_INCREMENT'
			if i[6] != '':
				query += ' DEFAULT \''+i[6]+'\''
			if i[8] is not 'NONE':			#add special characteristic of column
				query += ' '+i[8]
			query +=', '
		query = query[:-2]#remove last comma from list of columns
	
	query += ' ) ENGINE = INNODB'
	return query
