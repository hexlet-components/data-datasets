# Примеры к курсу «Apache Airflow»

В файле _orders.csv_ три заказа. DAG из _dags/count_orders.py_ читает этот файл и выводит число заказов в журнал задачи. В курсе используется локальный Airflow 3.4.0. Если преподаватель уже подготовил окружение, начните с ручного запуска в уроке «Запуск задачи».

## Локальный запуск

Для команд понадобятся Git, Python 3.12 и терминал Linux или macOS. Скачайте проект и перейдите в каталог клона.

```bash
git clone https://github.com/hexlet-components/data-datasets.git
cd data-datasets
```

Создайте отдельное окружение и установите Airflow. Пакет graphviz понадобится команде, которая показывает связи между задачами. Совместимые версии пакетов задаёт файл проекта Apache Airflow.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install 'apache-airflow==3.4.0' graphviz --constraint 'https://raw.githubusercontent.com/apache/airflow/constraints-3.4.0/constraints-3.12.txt'
```

Следующие команды указывают Airflow, где искать учебные DAG и куда сохранять служебную базу и журналы. Выполните их из каталога клона в обоих терминалах, в которых будете работать с Airflow.

```bash
source .venv/bin/activate
export AIRFLOW_HOME="$PWD/.airflow"
export AIRFLOW__CORE__DAGS_FOLDER="$PWD/airflow/dags"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
```

В первом терминале запустите Airflow и оставьте его работать.

```bash
airflow standalone
```

Во втором терминале дождитесь появления `count_orders` в выводе `airflow dags list`. Включите DAG командой `airflow dags unpause count_orders`. Теперь можно запускать его вручную. Чтобы завершить работу, нажмите Ctrl+C в первом терминале.
