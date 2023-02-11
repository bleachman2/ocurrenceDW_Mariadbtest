Using some of the open data from dados.gov
Crimes registados n pelas autoridades policiais - https://dados.gov.pt/pt/datasets/r/51d09405-bc96-4bd4-80dd-5160d9f0e111


## Utilization
install mariadb
`mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql`
start it
`systemctl start mariadb.service`
create a db called ocurrDW


## Todo
load more data -> maybe freguesias https://dados.gov.pt/pt/datasets/r/ec6ef805-c278-4b4d-ba9b-3116264f68b4

load existing data into mariadb

format data into DW compatability

frontend

add type hint