echo "Enter database name:"
read  dbname

echo "Enter PostgreSQL password:"
read -s  pword

echo 'Writing database name and postgresql password to params.ini ...'

echo "database=$dbname" >> params.ini
echo "password=$pword" >> params.ini

echo 'Successfully written to params.ini'
echo 'Remember to run reset_params.sh at end of session to prevent db name and postgreSQL password from being stored and require a git commit.'

