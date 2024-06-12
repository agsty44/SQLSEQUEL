# SQLSEQUEL

## A small project that aims to replicate the functionality of SQL.

### Initialisation Procedure:

From here you can add fields, import an existing table (table.txt), or stop adding fields and proceed to runtime.

#### If you type IMPORTTABLE:

The table provided in table.txt will be imported. You will be given the opportunity to add additional fields. All records will be preserved.

#### If you type STOP:

The software will proceed to the runtime environment.

#### If you type anything else:

That string will be added to database[0] (the index row).

### Runtime environment:

#### MODIFY:

Syntax: MODIFY (field) FROM (record number) (content)

Updates a field in a numbered record to a new value.

#### DROPTABLE:

Syntax: DROPTABLE

Deletes the content of all fields in all records. Keeps number of records and index rows.

#### SELECT:

Syntax: SELECT (field) FROM (record number), or SELECT (field) WHERE (field) (== or !=) (content)

Returns the content of the selected field in the selected record. If * is used in (field), it returns the whole records.

#### ADDRECORD:

Syntax: ADDRECORD

Adds a new record to the end of the table.

#### SEARCH:

Syntax: SEARCH FOR (field) (content)

Returns an array containing the row number of records that contain a field with matching content.