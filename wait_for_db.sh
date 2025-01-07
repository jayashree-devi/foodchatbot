#!binsh
set -e

host=$1
shift

until mariadb -h $host -u$DB_USER -p$DB_PWD -e SHOW DATABASES;  do
  echo Waiting for database...
  sleep 2
done

exec $@
