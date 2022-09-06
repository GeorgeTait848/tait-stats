echo 'Removing database name and user password from params.ini ...'

echo '[postgresql]' > params.ini
echo 'host=localhost' >> params.ini
echo 'user=postgres' >> params.ini

echo 'Successfully restored params.ini to original state.'
echo 'If you wish to continue using the database, run setup_params.sh again and enter the database name and your user password for postgreSQL'

