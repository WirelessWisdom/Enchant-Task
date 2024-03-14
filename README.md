# Enchant-Task

Репозиторій:
https://github.com/WirelessWisdom/Enchant-Task.git


Для запуску кластеру:
docker-compose up

Для запуску кластеру  у детач моді (що б не забирало консоль):
docker-compose up -d

Виключити кластер:
docker-compose down

Видалити все неактивне, тобто і зупинені конетйнери і всі імеджі
docker system prune -a

- Рекваерменти пишуться у імедж, тому якщо додається пакет - треба зупинити кластер, зробити docker system prune -a і знов зробити docker-compose up