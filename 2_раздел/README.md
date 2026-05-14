# Раздел 2: Docker

Сборка образа выполняется из корня репозитория:

```bash
docker build -f 2_раздел/Dockerfile -t yadro-section-2 .
```

Запуск контейнера:

```bash
docker run --name yadro-section-2-container yadro-section-2
```

Проверка результата через логи:

```bash
docker logs yadro-section-2-container
```
