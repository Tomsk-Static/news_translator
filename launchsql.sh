#!/bin/bash

exec sudo docker run  --name mysql -d -e MYSQL_ROOT_PASSWORD=mysql1 -e MYSQL_DATABASE=news -e MYSQL_USER=mysql -p 3306:3306 -e MYSQL_PASSWORD=mysql c60d96bd2b77
