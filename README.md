# YADRO-intern

Репозиторий содержит решение задания из трех разделов:

- `1_раздел` — Python-скрипт для выполнения HTTP-запросов к `https://httpstat.us`.
- `2_раздел` — Docker-образ на базе `ubuntu:22.04` для запуска скрипта из первого раздела.
- `3_раздел` — Ansible-playbook для установки Docker, сборки образа, запуска контейнера и проверки результата через `docker logs`.

## Раздел 1

Скрипт выполняет 5 запросов к `https://httpstat.us` и обрабатывает ответы по диапазонам HTTP-кодов:

- `1xx`, `2xx`, `3xx` логируются в консоль вместе со статус-кодом и телом ответа.
- `4xx`, `5xx` приводят к генерации `HttpStatusError`; исключение перехватывается и логируется, чтобы скрипт продолжил выполнение остальных запросов.

Запуск из папки первого раздела:

```bash
cd 1_раздел
python3 script.py
```

Для Windows:

```powershell
cd 1_раздел
py .\script.py
```

## Раздел 2

Сборка Docker-образа выполняется из корня репозитория:

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

Если контейнер с таким именем уже существует, его можно удалить перед повторной проверкой:

```bash
docker rm -f yadro-section-2-container
```

## Раздел 3

Playbook устанавливает Docker на целевой Debian/Ubuntu-хост, добавляет пользователя в группу `docker`, запускает службу Docker, копирует файлы первого и второго раздела на целевой хост, собирает образ, запускает контейнер, проверяет код завершения и выводит результат через `docker logs`.

Проверка синтаксиса без запуска задач:

```bash
cd 3_раздел
ANSIBLE_CONFIG=ansible.cfg ansible-playbook -i inventory.ini --syntax-check playbook.yml
```

Полная проверка на локальном Linux-хосте:

```bash
cd 3_раздел
ANSIBLE_CONFIG=ansible.cfg ansible-playbook -i inventory.ini playbook.yml -K -e target_user=$USER
```

При запросе `BECOME password` нужно ввести пароль пользователя с правами sudo.

Проверка на удаленном хосте:

```ini
[docker_hosts]
server ansible_host=192.168.1.10 ansible_user=ubuntu
```

После изменения `3_раздел/inventory.ini`:

```bash
cd 3_раздел
ANSIBLE_CONFIG=ansible.cfg ansible-playbook -i inventory.ini playbook.yml -K -e target_user=ubuntu
```

После успешного выполнения в выводе должны быть:

- версия Docker в `docker_version.stdout`;
- успешная проверка кода завершения контейнера;
- строки из `docker logs`, выведенные задачей Ansible.
