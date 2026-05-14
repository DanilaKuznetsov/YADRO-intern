# Раздел 3: Ansible

Playbook устанавливает Docker на целевой Debian/Ubuntu-хост, добавляет пользователя в группу `docker`, запускает службу Docker, копирует файлы первого и второго раздела на целевой хост, собирает образ, запускает контейнер и выводит результат через `docker logs`.

Проверка на локальном Linux-хосте:

```bash
cd 3_раздел
ANSIBLE_CONFIG=ansible.cfg ansible-playbook -i inventory.ini playbook.yml -K -e target_user=$USER
```

Проверка на удаленном хосте:

```ini
[docker_hosts]
server ansible_host=192.168.1.10 ansible_user=ubuntu
```

```bash
cd 3_раздел
ANSIBLE_CONFIG=ansible.cfg ansible-playbook -i inventory.ini playbook.yml -K -e target_user=ubuntu
```

Проверка синтаксиса без запуска задач:

```bash
cd 3_раздел
ANSIBLE_CONFIG=ansible.cfg ansible-playbook -i inventory.ini --syntax-check playbook.yml
```

После выполнения в выводе должны быть `docker_version.stdout`, успешная проверка кода завершения контейнера и строки из `docker logs`.
