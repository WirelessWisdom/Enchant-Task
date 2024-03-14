# Enchant-Task


https://github.com/WirelessWisdom/Enchant-Task.git
### Репозиторій


docker-compose up
### Для запуску кластеру

docker-compose up -d
### Для запуску кластеру  у детач моді (що б не забирало консоль)


docker-compose down
### Виключити кластер

docker system prune -a
### Видалити все неактивне, тобто і зупинені конетйнери і всі імеджі

### Рекваерменти пишуться у імедж, тому якщо додається пакет - треба зупинити кластер, зробити docker system prune -a і знов зробити docker-compose up