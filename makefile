DB_URL=postgresql://postgres:postgres@localhost:5432/bank_system?sslmode=disable

network:
	docker network create bank-network

postgres:
	docker run --name postgres  -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -d postgres:latest

mysql:
	docker run --name mysql8 -p 3306:3306  -e MYSQL_ROOT_PASSWORD=secret -d mysql:8

createdb:
	docker exec -it postgres createdb --username=root --owner=root bank_system

dropdb:
	docker exec -it postgres dropdb bank_system
