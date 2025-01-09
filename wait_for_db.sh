#!/bin/bash

# Wait for MariaDB to be ready
while ! mysqladmin ping --silent; do
    echo "Waiting for MariaDB to start..."
    sleep 2
done

echo "MariaDB is up and running."

# Create database and user
mariadb -h $DB_HOST -u $DB_USER -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"
mariadb -h $DB_HOST -u $DB_USER -e "GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';"
mariadb -h $DB_HOST -u $DB_USER -e "FLUSH PRIVILEGES;"
