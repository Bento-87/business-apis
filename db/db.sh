#!/bin/bash

if [ ! $APP_DB_ENDPOINT ] || [ ! $APP_DB_PASSWORD ] || [ ! $APP_DB_USER ]
then
    echo "Variables not found, try to export APP_DB_ENDPOINT, APP_DB_PASSWORD and APP_DB_USER"
    exit
fi

#------------------- Create Database ---------------------------------
#clients
echo 'create database clients default character set utf8 default collate utf8_general_ci' | mysql -h "$APP_DB_ENDPOINT" -u "$APP_DB_USER" -p"$APP_DB_PASSWORD"

#Products
echo 'create database products default character set utf8 default collate utf8_general_ci' |mysql -h "$APP_DB_ENDPOINT" -u "$APP_DB_USER" -p"$APP_DB_PASSWORD"

#_order
echo 'create database _order default character set utf8 default collate utf8_general_ci' | mysql -h "$APP_DB_ENDPOINT" -u "$APP_DB_USER" -p"$APP_DB_PASSWORD"

#------------------- Tables  -----------------------------------------
#clients
mysql -h "$APP_DB_ENDPOINT" -u "$APP_DB_USER" -p"$APP_DB_PASSWORD" clients < clients.sql

#Products
mysql -h "$APP_DB_ENDPOINT" -u "$APP_DB_USER" -p"$APP_DB_PASSWORD" products < products.sql

#_order
mysql -h "$APP_DB_ENDPOINT" -u "$APP_DB_USER" -p"$APP_DB_PASSWORD" _order < _order.sql

#Commit
echo 'commit;' | echo 'commit;' | mysql -h "$APP_DB_ENDPOINT" -u "$APP_DB_USER" -p"$APP_DB_PASSWORD"

#clear bash_history
history -cw