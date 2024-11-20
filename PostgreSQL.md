## PostgreSQL

---

* **SQL** (Structured Query Language) - язык структурированных запросов.

* **Процедурное расширение SQL** - "диалект" (надбавка). PL/pgSQL в PostgreSQL, PL/SQL в Oracle.

* **База данных** (БД) - набор взаимосвязанных данных.

* **Система управления базами данных** (СУБД) - комплекс программных средств для управления данными.

* **СУБД** отвечает за: поддержку языка БД, механизмы хранения и извлечения данных, оптимизацию процессов извлечения.
  данных и тд.

* **Реляционные СУБД** - СУБД, управляющая реляционными базами данных.

* **Реляционная база данных** – это набор данных с предопределенными связями между ними.

---

* **Сущность** – например, клиенты, заказы, поставщики.

* **Таблица** – отношение.

* **Столбец** – атрибут.

* **Строка/запись** – кортеж.

* **Результирующий набор** – результат SQL-запроса.

---

* **string** в одинарных кавычках.

* Среда, где пишем код - **Query Tool**.

* Команды (операторы) по соглашению нужно прописывать с **заглавной** буквы, а названия таблиц, ... с **маленькой**.

* Для того чтобы экранировать внутреннюю кавычку, необходимо добавить перед ней ещё одну - **'something''wasd'**.

---

### Типы СУБД

1. **Файл-серверные**: Microsoft Access.
2. **Клиент-серверные**: MySQL, PostgreSQL, Oracle, ...
3. **Встраиваемые**: SQLite.

---

### Типы SQL-запросов

1. **DDL** (Data Definition Language) - работа с БД / таблицами.
    * `CREATE TABLE` table_name – создать таблицу.
    * `ALTER TABLE` table_name – изменить таблице.
        * `ADD COLUMN` column_name data_type.
        * `RENAME TO` new_table_name.
        * `RENAME` column_name `TO` new_column_name.
        * `ALTER COLUMN` column_name `SET DATA TYPE` data_type.
    * `DROP TABLE` table_name – удалить таблицу.
    * `TRUNCATE TABLE` table_name – удалить все данные и логи, но оставить структуру (нельзя резать таблицы, на которые
      есть
      ссылки, те внешний ключ, в других таблицах).


2. **DML** (Data Manipulation Language) - работа с данными.
    * `SELECT` – выборка данных.
    * `INSERT` – вставка новых данных.
    * `UPDATE` – обновление данных.
    * `DELETE` – удаление данных.
    * `MERGE` – слияние данных.


3. **TCL** (Transaction Control Language) - работа с транзакциями. `COMMIT`, `ROLLBACK`, `AVEPOINT`.
4. **DCL** (Data Control Language) - работа с разрешениями. `GRANT`, `REVOKE`, `DENY`.
5. **ANSI SQL-92** - единый стандарт для всех SQL языков. Благодаря ему большая часть запросов примерно одинаковая.

---

### [Основные типы данных](https://metanit.com/sql/postgresql/2.3.php)

---

### Базовые SQL-запросы

1. Создание БД:
   ```
   CREATE DATABASE db_name
       WITH ...
   ```
2. Удаление БД:
   ```
   DROP DATABASE [IF EXISTS] db_name
   ```
3. Создание таблицы (также можно создать напрямую через pgAdmin):
   ```
   CREATE TABLE table_name
   (
       data_id integer PRIMARY KEY,
       column1 varchar(128) [NOT NULL,...], ...
   )
   ```
4. Удаление таблицы:
   ```
   DROP TABLE [IF EXISTS] table_name [CASCADE]
   ```
5. Вставка данных (n>=1) в таблицу:
   ```
   INSERT INTO table_name
   VALUES
   (data1, data2, ...),
   ```

* Также возможно запись вставки в одну строчку (n=1).  
  `INSERT INTO table_name VALUES (data1, data2, ...);`

---

### Отношение один ко многим (самое популярное)

* **Пример**: издатель - книги.

```
CREATE TABLE publisher
(
    publisher_id integer PRIMARY KEY,
    org_name varchar(128) NOT NULL,
    address text NOT NULL
);

CREATE TABLE book
(
   book_id integer PRIMARY KEY,
   title text NOT NULL,
   isbn varchar(32) NOT NULL
);
```

```
ALTER TABLE book
ADD COLUMN fk_publisher_id int FOREIGN KEY; - добавить в конец

ALTER TABLE book
ADD CONSTRAINT fk_publisher_id - добавить ограничение
FOREIGN KEY(fk_publisher_id) REFERENCES publisher(publisher_id);
```

Или можно задать зависимость при создании таблицы:

```
CREATE TABLE book
(
   book_id integer PRIMARY KEY,
   title text NOT NULL,
   isbn varchar(32) NOT NULL
   fk_publisher_id integer REFERENCES publisher(publisher_id) NOT NULL
);
```

---

### Отношение один к одному

* **Пример**: человек - паспорт.

```
CREATE TABLE person
(
    person_id int PRIMARY KEY,
    first_name varchar(64) NOT NUL,
    last_name varchar(64) NOT NULL
);

CREATE TABLE passport
(
    passport_id int PRIMARY KEY,
    serial_number int NOT NUL,
    fk_person_id int UNIQUE REFERENCES person(person_id) - UNIQUE гарантирует отсутствие дубликатов
);
```

---

### Отношение многие ко многим

* **Пример**: авторы статей - статьи.

```
CREATE TABLE book
(
    book_id int PRIMARY KEY
)

CREATE TABLE author
(
    author_id int PRIMARY KEY
)
```

```
CREATE TABLE book_author
(
    book_id int REFERENCES book(book_id),
    author_id int REFERENCES author(author_id),
    
    CONSTRAINT book_author_pkey PRIMARY KEY (book_id, author_id) - композитный ключ (состояющий из нескольких колонок) - плохо
)
```

* что **PRIMARY KEY**, что **FOREIGN KEY** являются ограничениями (**CONSTRAINT**).

---

### Базовые SELECT-запросы (выборки)

* **SELECT** работает после **FROM** и **WHERE**.

```
SELECT * - полная выборка (все колонки и все строки)
FROM table_name
```

**SELECT** получает строки из множества таблиц.

* `SELECT column1_name, column2_name, ...` - выборка из конкретных столбцов.


* `SELECT column1_name * column2_name` - выборка (столбец) из произведения элементов столбцов.

**DISTINCT** выводит только уникальные строки.

* `SELECT DISTINCT column1_name` - выводит только уникальные элементы.


* `SELECT DISTINCT column1_name, column2_name` - выводит только уникальные строки (сочетания).

**COUNT** выводит количество строк.

* `SELECT COUNT(*)` - посчитает общее количество строк.


* `SELECT COUNT(DISTINCT column1_name)` - посчитает количество уникальных строк в данном столбце.


* `SELECT column1_name || ' ' || column2_name` == `SELECT CONCAT(column1_name,' ',column2_name)` - выведет один столбец
  со значениями через пробел (объединение строк).

---

### Фильтрация WHERE

* Для работы с датами их необходимо заключать в одинарные кавычки `date > '1998-01-01'`.

```
SELECT *
FROM table_name
WHERE column1_name > 123 - условие
```

**WHERE** - оператор фильтрации.

* `WHERE condition1 {AND|OR} condition2`


* `WHERE column_name BETWEEN data1 and data2` - оператор предполагает включение (нестрого).


* `WHERE column_name = data1 OR column_name = data2 OR ...` == `WHERE column_name IN (data1, data2, ...)`


* `WHERE column_name NOT IN (data1, data2, ...)`


* `WHERE column_name IS [NOT] NULL`

---

### Сортировка ORDER BY

* Идёт после **FROM** или после **WHERE**.

```
SELECT *
FROM table_name
ORDER BY column1_name ASC, column2_name DESC, ...
```

**ORDER BY** - оператор сортировки вывода запроса.

* {**ASC**|**DESC**} (Ascending|Descending).
* По умолчанию стоит **ASC**, те по возрастанию.

---

### Агрегатные функции

```
SELECT MIN(column_name) - выведет минимальное из column_name
FROM table_name
```

**Агрегатные функции** вычисляют одно значение над некоторым набором строк.

* Ещё есть `MAX`, `AVG`, `SUM`, ...

---

### Оператор LIKE

**%** - placeholder (заполнитель) означающий 0, 1 и более символов.
**_** - ровно 1 любой символ.

```
SELECT column_name
FROM table_name
WHERE column_name LIKE '%a_'
```

**LIKE** - оператор, который используется для поиска строк, содержащих определённый шаблон символов.

* `LIKE 'U%'` - строки, начинающиеся с U.
* `LIKE '%U'` - строки, оканчивающиеся на U.

---

### Оператор LIMIT

* Идёт всегда последним.

```
SELECT column_name
FROM table_name
LIMIT 15 - выведет первые 15 элементов column_name
```

**LIMIT** - оператор, который выводит указанное число строк запроса.

---

### Группировка GROUP BY

* При наличии **WHERE** и **ORDER BY** стоит между ними.

*

```
SELECT column_name, COUNT(*) AS custom_name - псевдоним (кастомное название) столбца
FROM table_name
GROUP BY column_name
```

**GROUP BY** определяет то, как строки будут группироваться.

**Пример**:

```
SELECT category_id, supplier_id, AVG(unit_price) AS avg_price
FROM products
WHERE units_in_stock > 10
GROUP BY category_id, supplier_id - группировка по двум параметрам
ORDER BY category_id
LIMIT 5
```

---

### Постфильтрация HAVING

```
SELECT column1_name, MIN(column2_name)
FROM table_name
GROUP BY column1_name, column2_name, ... 
HAVING condition - постфильтрация
```

**HAVING** - оператор, который используется в паре с **GROUP BY** и является фильтром для групп.

**Пример**:

```
SELECT category_id, SUM(unit_price * units_in_stock)
FROM products
WHERE discontinued <> 1 - фильтр
GROUP BY category_id
HAVING SUM(unit_price * units_in_stock) > 5000 - постфильтр
ORDER BY SUM(unit_price * units_in_stock) DESC
```

---

### Операции на множествах

```
SELECT column11_name, column12_name - ориентируемся на эти столбцы
FROM table1_name
UNION
SELECT column21_name, column22_name - их количество должно совпадать
FROM table2_name
```

* **UNION** - объединение (удаляет дубликаты).

* **UNION ALL** - объединение (не удаляет дубликаты).


* **INTERSECT** - пересечение (удаляет дубликаты).

* **INTERSECT ALL** - пересечение (не удаляет дубликаты).


* **EXCEPT** - исключение (возвращает первую выборку без второй и удаляет дубликаты).

* **EXCEPT ALL** - **EXCEPT** + разница между количеством единых дубликатов выборок, если в первой их больше (10 в
  первой и 6 во второй, то в конечной будет 4 элемента) + не удаляет дубликаты.

**Пример**:

```
SELECT country
FROM customers
{UNION|INTERSECT|EXCEPT} [ALL]
SELECT country
FROM employees
```

---

### Соединения JOIN

* Если нет соответствия ставится NULL.

```
SELECT *
FROM table1_name
JOIN table2_name ON table1_name.column1_name = table2_name.column2_name
WHERE ...
```

* **INNER JOIN** - пересечение по ключу левой и правой таблицы.

* **LEFT (OUTER) JOIN** - из левой таблицы попадают абсолютно все записи (совместно с правой и без неё).

* **RIGHT (OUTER) JOIN** - из правой таблицы попадают абсолютно все записи (совместно с левой и без неё).

* **FULL (OUTER) JOIN** - объединение по ключу левой и правой таблицы (объединение LEFT JOIN и RIGHT JOIN).

* **CROSS JOIN** (декартово произведение) - каждому элементу из правой соответствует каждый из левой (NxM).

* **NATURAL JOIN** - INNER JOIN, но соединение происходит по всем столбцам с одинаковым названием.

* **SELF JOIN** (рекурсивный) - присоединить таблицу к самой себе (модель, не является отдельным оператором).

---

### INNER JOIN

* **INNER JOIN** == **JOIN**

**Пример**:

```
SELECT product_name, suppliers.company_name, units_in_stock
FROM products
INNER JOIN suppliers ON products.supplier_id = suppliers.supplier_id
```

---

### OUTER JOINS

* Если всем ключам есть соответствие, то **LEFT JOIN** == **INNER JOIN**.

**Пример**:

```
SELECT company_name, product_name
FROM suppliers
{LEFT|RIGHT|FULL} [OUTER] JOIN products ON suppliers.supplier_id = products.supplier_id
```

---

### CROSS JOIN

* При **CROSS JOIN** часть с **ON** опускается

```
SELECT column_name
FROM table1_name
CROSS JOIN table2_name
```

---

### NATURAL JOIN

* При **NATURAL JOIN** часть с **ON** опускается

```
SELECT column_name
FROM table1_name
NATURAL JOIN table2_name
```

* **Лучше не использовать**, а вместо этого прописывать все связи в ручную, чтобы избегать ошибок.

### SELF JOIN

* Чаще всего нужен для того, чтобы построить иерархию

**Пример**:

```
CREATE TABLE employee (
employee_id int PRIMARY KEY,
first_name varchar(256) NOT NULL,
last_name varchar(256) NOT NULL,
manager_id int,
FOREIGN KEY (manager_id) REFERENCES employee(employee_id) - указатель на то, что SELF JOIN возможен
);
```

```
INSERT INTO employee
(employee_id, first_name, last_name, manager_id)
VALUES
(1, 'Windy', 'Hays', NULL),
(2, 'Ava', 'Christensen', 1),
(3, 'Anna', 'Reeves', 2);
```

```
SELECT e.first_name || ' ' || e.last_name AS employee,
m.first_name || ' ' || m.last_name AS manager
FROM employee e
LEFT JOIN employee m ON m.employee_id = e.manager_id
ORDER BY manager;
```

* Выведет слева ФИ сотрудника, а справа ФИ его менеджера.

---

### Оператор USING

```
SELECT column_name
FROM table1_name
JOIN table2_name ON table1_name.column_name = table2_name.column_name
```

Или можно написать **так**:

```
SELECT column_name
FROM table1_name
JOIN table2_name USING(column_name)
```

Те внутри ключевого слова **USING** мы пишем название столбца, по которому производим соединение. Он должен одинаково
называться в обеих таблицах.

---

### Псевдонимы Alias

* Псевдонимы используются для присвоения таблице или столбцу временного имени.

```
SELECT column1_name [AS] new_col1, COUNT(DISTINCT column2_name) [AS] new_col2
FROM table1_name [AS] new_tb1
JOIN table2_name [AS] new_tb2 ON new_tb1.id = new_tb2.id
```

Работа в **SELECT**:

* Нельзя использовать в **WHERE** и **HAVING** (работают до **SELECT**).

* Можно использовать в **GROUP BY** и **ORDER BY** (работают после **SELECT**) и при использовании **подзапросов**.

---

### Подзапросы (SubQuery)

**Зачем они нужны?**

* Запросы бывают логически сложными.
* Реализовать запрос в лоб может быть сложно => подзапросы могут помочь.
* Есть задачи, которые без подзапросов не решить.

Выведем все компании, которые находятся там же, где и клиенты:

```
SELECT company_name
FROM suppliers
WHERE country IN (SELECT DISTINCT country FROM customers) - это подзапрос	             
```

Можно заменить **JOIN**ом:

```
SELECT company_name
FROM suppliers
JOIN customers USING(country)
```

НО так работает не всегда. Проще говоря надо смотреть по ситуации - когда-то удобнее **JOIN**, когда-то **подзапрос**.

---

### Оператор EXISTS

**WHERE EXISTS** с подзапросом внутри возвращает **true**, если в подзапросе была возвращена хотя бы одна строка.

```
SELECT company_name, contact_name
FROM costumers
WHERE [NOT] EXISTS (SELECT customer_id FROM orders
              WHERE customer_id = customers.customer_id 
              AND freight BETWEEN 50 AND 100)
```

---

### Операторы ANY | ALL

* Операторы **ANY** и **ALL** используются с фильтрациями **WHERE** и **HAVING**.

* Оператор **ANY** возвращает **true**, если какое-либо из значений подзапроса соответствует условию.

* Оператор **ALL** возвращает **true**, если все значения подзапроса удовлетворяют условию.

```
SELECT DISTINCT company_name
FROM customers
WHERE customer_id = ANY(
   SELECT customer_id
   FROM orders
   JOIN order_details USING(order_id)
   WHERE quantity > 40
   )
```

```
SELECT DISTINCT product_name
FROM products
JOIN order_details USING(product_id)
WHERE quantity > ALL(SELECT AVG(quantity)
   FROM order_details
   GROUP BY product_id
   )
```

---

### DDL (Data Definition Language)

* `CREATE TABLE` table_name – создать таблицу.
* `ALTER TABLE` table_name – изменить таблице.
* `ADD COLUMN` column_name data_type.
* `RENAME TO` new_table_name.
* `RENAME` column_name `TO` new_column_name.
* `ALTER COLUMN` column_name `SET DATA TYPE` data_type.
* `DROP TABLE` table_name – удалить таблицу.
* `TRUNCATE TABLE` table_name – удалить все данные и логи, но оставить структуру (нельзя резать таблицы, на которые есть
  ссылки, те внешний ключ, в других таблицах).

**DDL** (язык описания данных) отвечает за работу с **БД** | **таблицами**.

* Создание таблицы:

```
CREATE TABLE student(
student_id serial NOT NULL,
first_name varchar(128),
last_name varchar(128)
);
```

* Добавление колонки в таблицу:

```
ALTER TABLE student
ADD COLUMN middle_name varchar(128);
```

* Переименовывание таблицы:

```
ALTER TABLE student
RENAME TO student_data;
```

* Переименовывание колонки:

```
ALTER TABLE student_data
RENAME last_name TO new_last_name;
```

* Удаление колонки:

```
ALTER TABLE student_data
DROP COLUMN new_last_name,
DROP COLUMN middle_name;
```

* Изменение типа данных колонки:

```
ALTER TABLE student_data
ALTER COLUMN first_name 
SET DATA TYPE varchar(64);
```

* Удаление таблицы:

```
DROP TABLE [IF EXISTS] student_data [CASCADE];
```

---

### Тип данных serial

* Он представляет автоинкрементирующееся числовое значение.
* Значение данного типа образуется путем автоинкремента значения предыдущей строки (**+1**).
* Поэтому, как правило, данный тип используется для определения **id** строки.

**Автоинкремент** — это функция, которая автоматически генерирует уникальный номер для каждой новой строки, добавленной
в таблицу.

Посмотрим, как работает serial на примере ранее созданной таблицы **student_data**:

* Присвоит **Anna** `student_id = 1` и **Alla** `student_id = 2` автоматически.

```
INSERT INTO student_data (first_name) 
VALUES
('Anna'),
('Alla');
```

* Присвоит **Anna** `student_id = 3` и **Alla** `student_id = 4`.

```
TRUNCATE TABLE student_data; - удаление данных и логов таблицы, но не её структуры.

INSERT INTO student_data (first_name) 
VALUES
('Anna'),
('Alla');
``` 

Так выходит потому что у **TRUNCATE** по умолчанию стоит **CONTINUE IDENTITY** (не сбрасывает нумерацию **id**).

* Для сброса необходимо добавить **RESTART IDENTITY** - `TRUNCATE TABLE student_data RESTART IDENTITY;`.

---

### Ограничение CONSTRAINT

* **CONSTRAINT** используются для (указания правил) ограничения типа данных, которые могут быть помещены в таблицу. Это
  обеспечивает точность и достоверность данных в таблице.

* Если существует какое-либо нарушение между ограничением и действием данных, действие
  прерывается.

* Ограничения могут быть на уровне столбцов и таблиц.

В SQL обычно используются следующие ограничения:

* `NOT NULL` - гарантирует, что столбец не может иметь нулевое значение.
* `UNIQUE` - гарантирует, что все значения в столбце будут разными.
* `PRIMARY KEY` - комбинация NOT NULL и UNIQUE. Уникально идентифицирует каждую строку в таблице.
* `FOREIGN KEY` - однозначно идентифицирует строку/запись в другой таблице.
* `CHECK` - гарантирует, что все значения в столбце удовлетворяют определенному условию.
* `DEFAULT` - задает значение по умолчанию для столбца, если значение не указано.
* `INDEX` - используется для быстрого создания и извлечения данных из базы данных.

Задать ограничение можно при создании и изменении таблицы.

* Способ вывести все ограничения по столбцу `chair_id`:

```
SELECT constraint_name
FROM information_schema.key_column_usage
WHERE table_name = 'chair'
AND table_schema = 'public'
AND column_name = 'chair_id';
```

* Способ удалить ограничение:

```
ALTER TABLE chair
DROP CONSTRAINT chair_chair_id_key - название ограничения.
```

---

### PRIMARY KEY

* Уникально идентифицирует каждую строку в таблице.

В таблице **PK** может быть только один столбец или комбинация столбцов (**композитный ключ**) - **плохо**, в отличие от
**UNIQUE NOT NULL**.

* Задание **PK** при создании:

```
CREATE TABLE chair
(
chair_id serial [CONSTRAINT PK_char_chair_id] PRIMARY KEY, - название ограничения задано автоматически 'chair_chair_id_key'
chair_name varchar
);
```

```
CREATE TABLE chair
(
chair_id serial,
chair_name varchar,

CONSTRAINT PK_char_chair_id PRIMARY KEY(chair_id) - мы сами задали название ограничения 'PK_char_chair_id'
);
```

* Задание **PK** при изменении:

```
ALTER TABLE chair
ADD PRIMARY KEY(chair_id);
```

```
ALTER TABLE chair
ADD CONSTRAINT PK_char_chair_id PRIMARY KEY(chair_id)
```

---

### FOREIGN KEY

* Используется для связи между таблицами.

* Внешний ключ устанавливается для столбца из зависимой таблицы, и указывает на один из столбцов из главной таблицы.

Как правило, внешний ключ указывает на первичный ключ из связанной главной таблицы.

* Задание **FK** при создании:

```
CREATE TABLE book
(
book_id serial PRIMARY KEY,
publisher_id serial [CONSTRAINT FK_books_publisher] REFERENCES publisher(publisher_id)
);
```

```
CREATE TABLE book
(
book_id serial PRIMARY KEY,
publisher_id serial,

CONSTRAINT FK_books_publisher FOREIGN KEY(publisher_id) REFERENCES publisher(publisher_id)
);
```

* Задание **FK** при изменении:

```
ALTER TABLE book
ADD CONSTRAINT FK_books_publisher FOREIGN KEY(publisher_id) REFERENCES publisher(publisher_id);
```

Если при **INSERT** в `book` передать в `publisher_id` не существующий **id**, то будет ошибка.

* Общий синтаксис установки внешнего ключа:

```
REFERENCES ref_table_name(ref_table_column_name)
    [ON DELETE {CASCADE|RESTRICT|...}]
    [ON UPDATE {CASCADE|RESTRICT|...}]
```

* С помощью выражений **ON DELETE** и **ON UPDATE** можно установить действия, которые выполняются соответственно при
  **удалении** и **изменении** связанной строки из главной таблицы.

Для установки подобного действия можно использовать следующие опции:

* **CASCADE**: автоматически удаляет или изменяет строки из зависимой таблицы при удалении или изменении связанных строк
  в главной таблице.

* **RESTRICT**: предотвращает какие-либо действия в зависимой таблице при удалении или изменении связанных строк в
  главной таблице. То есть фактически какие-либо действия отсутствуют.

* **NO ACTION**: действие по умолчанию, предотвращает какие-либо действия в зависимой таблице при удалении или изменении
  связанных строк в главной таблице. И генерирует ошибку. В отличие от **RESTRICT** выполняет проверку на связанность
  между таблицами в конце транзакции.

* **SET NULL**: при удалении связанной строки из главной таблицы устанавливает для столбца внешнего ключа значение
  **NULL**.

* **SET DEFAULT**: при удалении связанной строки из главной таблицы устанавливает для столбца внешнего ключа значение по
  умолчанию, которое задается с помощью атрибуты **DEFAULT**. Если для столбца не задано значение по умолчанию, то в
  качестве него применяется значение **NULL**.

---

### CHECK

* Используется для ограничения диапазона значений, которые могут быть помещены в столбец.


* Задание **CHECK** при создании:

```
CREATE TABLE book
(
book_id serial PRIMARY KEY,
price decimal [CONSTRAINT CHK_book_price] CHECK (price >= 0)
);
```

```
CREATE TABLE book
(
book_id serial PRIMARY KEY,
price decimal,
    
CONSTRAINT CHK_book_price CHECK (price >= 0)
);
```

* Задание **CHECK** при изменении:

```
ALTER TABLE book
ADD CONSTRAINT CHK_book_price CHECK (price >= 0); - сервер не даст записать данные, если не будет выполнено условие
```

* Внутри скобок может быть любое условие

---

### DEFAULT

* Используется для задания значения по умолчанию столбца.

Никаких **CONSTRAINT** для **DEFAULT** не нужно.

* Задание **DEFAULT** при создании:

```
CREATE TABLE customer
(
customer_id serial,
full_name text,
status char DEFAULT 'r',

CONSTRAINT PK_customer_customer_id PRIMARY KEY(customer_id),
CONSTRAINT CHK_customer_status CHECK(status = 'r' OR status = 'p')
)
```

* Задание **DEFAULT** при изменении:

```
ALTER TABLE customer
ALTER COLUMN status 
SET DEFAULT 'r';
```

* Удаление **DEFAULT** при изменении:

```
ALTER TABLE customer
ALTER COLUMN status 
DROP DEFAULT;
```

---

### Генератор последовательностей SEQUENCE

* Создание последовательности (счетчика):

```
CREATE SEQUENCE seq;
```

* Функции последовательностей:

```
SELECT nextval('seq'); - сначала запускает счетчик со значением старта, а далее делает следующие шаги и возвращает соответствующие значение последовательности.
SELECT currval('seq'); - возвращает текущее значение последовательности.
SELECT lastval(); - не принимает аргумент и возвращает последнее значение, сгенерованное какой-либо из последовательностей данной сессии.
SELECT setval('seq', 16, {true|false}) - устанавливает для последовательности заданное значение поля.
```

При **true** (по умолчанию) - `nextval('seq')` будет следующее число относительно заданного в `setval`.  
При **false** - `nextval('seq')` будет число заданное в `setval`.

* Основные параметры при создании последовательности:

```
CREATE SEQUENCE IF NOT EXISTS giga_seq
INCREMENT 16 - шаг 16
MINVALUE 0 - минимум 0 (при переходе выводит ошибку)
MAXVALUE 160 - максимум 160 (при переходе выводит ошибку)
START WITH 2 - начинает с 2 (по умолчанию стоит 0)
```

* Переименование последовательности:

```
ALTER SEQUENCE seq
RENAME TO new_seq; 
```

* Сброс последовательности:

```
ALTER SEQUENCE seq
RESTART [WITH num];
```

* Удаление последовательности:

```
DROP SEQUENCE seq;
```

---

### Последовательности и таблицы

* Делаем **serial** в домашних условиях:

```
CREATE TABLE book
(
book_id int NOT NULL,
title text NOT NULL,
isbn varchar(32) NOT NULL,
publisher_id int NOT NULL,

CONSTRAINT PK_book_book_id PRIMARY KEY(book_id)
);
```

```
CREATE SEQUENCE IF NOT EXISTS book_book_id_seq
START WITH 1 OWNED BY book.book_id;
```

```
ALTER TABLE book
ALTER COLUMN book_id 
SET DEFAULT nextval('book_book_id_seq'); - установить значения по умолчанию, иначе будет ошикба при INSERT.
```

Но всё не так красочно, ведь тут <u>так же как и у оригинального</u> **serial** существует проблема с ручной добавкой
**book_id**.

В какой-то момент будет ошибка - последовательность упрётся в номер, который мы добавили, тк **PK** по определению
**UNIQUE**.  
Проще говоря, нет синхронизации с реальностью.

* Делаем **serial++**:

```
CREATE TABLE book
(
book_id int GENERATED {ALWAYS или BY DEFAULT} AS IDENTITY (START WITH 1 INCREMENT BY 1 ...) NOT NULL,
title text NOT NULL,
isbn varchar(32) NOT NULL,
publisher_id int NOT NULL,

CONSTRAINT PK_book_book_id PRIMARY KEY(book_id)
);
```

```
INSERT INTO book (title, isbn, publisher_id)
VALUES
('data','data', 1);
```

В данном случае мы просто не сможем добавить в таблицу строку при указывании **book_id** вручную.

* Работает на версиях PostgreSQL >= 10.
* Другие СУБД поддерживают подобный синтаксис.

Ограничение можно обойти так:

```
INSERT INTO book
OVERRIDING SYSTEM VALUE
VALUES (3, 'data', 'data', 1)
```

---

### Оператор INSERT

* Вставляем во все столбцы таблицы.

```
INSERT INTO table_name
VALUES
(data1), 
(data2); - можно вставлять больше 1 строчки данных за раз
```

* Вставляем в конкретные столбцы таблицы.

```
INSERT INTO table_name (column1_name, ...)
VALUES ();
```

* Создаём новую таблицу `best_authors` с данными из `author` при условии `rating > 4`.

```
SELECT *
INTO best_authors
FROM author
WHERE rating > 4
```

* Вставляем данные из `author` в `best_authors` при условии `rating < 4`.

```
INSERT INTO best_authors 
SELECT *
FROM author
WHERE rating < 4
```

---

### Операторы UPDATE, DELETE, RETURNING

* **UPDATE** - обновляет данные таблицы.

```
UPDATE author
SET full_name = 'Big Man', rating = 5 - изменил значения full_name и rating в строке, где author_id = 3.
WHERE author_id = 3;
```

* **DELETE** - удаляет данные из таблицы, но сохраняет логи.

```
DELETE FROM author
WHERE rating < 4.5; - удалили все строки, где rating < 4.5.
```

```
DELETE FROM author; - удалит все строки.
```

* **RETURNING** - выводит данные, с которыми мы работали (вставили, обновили, удалили).

```
INSERT INTO book
VALUES ('data')
RETURNING *; - выведет всё, что мы вставили.
```

```
INSERT INTO book (book_id)
VALUES ('data')
RETURNING book_id; - выведет все book_id, что мы вставили.
```

```
UPDATE author
SET full_name = 'Big Man', rating = 5
WHERE author_id = 3
RETURNING *; - выведет всё, что мы обновили.
```

```
DELETE FROM author
WHERE author_id = 3
RETURNING *; - выведет всё, что мы удалили.
```

---

### Нормализация

* **Нормальная Форма** - свойство отношения, характеризующее его с точки зрения избыточности.

* **Нормализация** - процесс минимизации избыточности отношения (приведение к НФ).

**1 Нормальная форма**

* Нет строк-дубликатов.
* Все поля (атрибуты) простых типов данных (int, varchar, ...). Не массивы.
* Все значения скалярные (одно значение в поле). Не массивы.

**2 Нормальная форма**

* Удовлетворяет **1НФ**.
* Есть первичный ключ (может быть композитным).
* Все поля (атрибуты) описывают первичный ключ целиком, а не лишь его часть:

Таблица `(author_id, book_id, author_name, book_title)` - не подходит, тк `author_name` описывает только
ключ `author_id`, а `book_title` только `book_id`.  
Поэтому надо разбить данную таблицу на 3, `(author_id, author_name)`, `(book_id, book_title)`, `(author_id, book_id)`.

**3 Нормальная форма**

* Удовлетворяет **2НФ**
* Нет зависимостей одних неключевых атрибутов от других (все атрибуты зависят только от первичного или внешнего ключа)

Таблица `(book_id, book_title, publisher_title, publisher_contact)` - не подходит, тк `publisher_title` зависит
от `publisher_contact` и они оба не являются ключевыми.  
Поэтому надо разбить данную таблицу на 2, `(book_id, book_title, publisher_id)`, `(publisher_id, title, contact)`.


---

### Представления VIEW

* **VIEW** - сохранённый запрос (подзапрос) в виде объекта БД (виртуальная таблица).
* Так как **VIEW** объект, то его можно увидеть в Schemas - Public - Views.
* К **VIEW** можно делать обычный **SELECT**.
* **VIEW** можно соединять и тд (**JOIN**,...).
* Производительность такая же, как и у обычной таблицы.
* Позволять делать кеширование с помощью материализации.
* Позволяет сокращать сложные запросы.
* Позволяет подменить реальную таблицы.
* Позволяет создавать виртуальные таблицы, соединяющие несколько таблиц.
* Позволяет скрыть логику агрегации данных при работе через **ORM**.
* Позволяет скрыть информацию(строки/столбцы) от групп пользователей.

**Виды**:

* Временные. +
* Обновляемые. +
* Рекурсивные. -
* Материализуемые. -

```
CREATE VIEW view_name AS
SELECT select_statement - обычный запрос
```

Изменение (`REPLACE`) **VIEW**:

* Можно только добавлять в конец новые столбцы:
    * нельзя удалять существующие
    * нельзя поменять имена столбцов
    * нельзя поменять порядок следования столбцов

```
CREATE OR REPLACE VIEW view_name AS
SELECT select_statement;
```

* Можно переименовать **VIEW**:

```
ALTER VIEW view_name 
RENAME TO new_view_name;
```

* Можно удалить **VIEW**:

```
DROP VIEW [IF EXISTS] view_name;
```

Модифицировать данные (вставлять, удалять, ...) через **VIEW** можно, если:

* Данные только из одной таблицы в **SELECT**.
* Нет **DISTINCT**, **GROUP BY**, **HAVING**, **UNION**, **INTERSECT**, **EXCEPT**, **LIMIT**.
* Нет агрегатных функций **MIN**, **MAX**, **SUM**, **COUNT**, **AVG**, ...
* **WHERE** не под запретом.

```
CREATE VIEW products_suppliers_categories AS
SELECT product_name, quantity_per_unit, unit_price, units_in_stock, 
company_name, contact_name, phone, 
category_name, description
FROM products
JOIN suppliers USING (supplier_id)
JOIN categories USING (category_id);
```

Выведет все строки, где unit_price > 20:

```
SELECT *
FROM products_suppliers_categories
WHERE unit_price > 20;
```

---

### Обновляемые представления

Оригинальная таблица:

```
CREATE OR REPLACE VIEW heavy_orders AS
SELECT order_id, freight
FROM orders
WHERE freight > 50;
```

После выполнения данного кода в `heavy_orders` произойдёт изменение `freight > 100` без каких-либо ошибок:

```
CREATE OR REPLACE VIEW heavy_orders AS
SELECT order_id, freight
FROM orders
WHERE freight > 100;
```

В таком случае будет ошибка:

```
CREATE OR REPLACE VIEW heavy_orders AS
SELECT order_id, ship_via, freight
FROM orders
WHERE freight > 50;
```

Два запроса снизу смогут "обмануть" систему, но придётся **DROP**ать `new_view`:

```
ALTER VIEW heavy_orders RENAME TO new_view;
```

```
CREATE OR REPLACE VIEW heavy_orders AS
SELECT order_id, ship_via, freight
FROM orders
WHERE freight > 50;
```

Можно делать **INSERT** через **VIEW** (вставится в оригинальные таблицы):

```
INSERT INTO heavy_orders
VALUES (1, 1, 50);
```

Можно удалять строки, что есть во **VIEW** (они также удаляются из оригинала):

```
DELETE FROM heavy_orders 
WHERE freight < 100.25;
```

---

### CHECK во VIEW

```
CREATE OR REPLACE VIEW heavy_orders AS
SELECT *
FROM orders
WHERE freight > 100;
```

У нас получится вставить эти неподходящие под фильтр `freight > 100` данные через `heavy_orders`.   
Они попадут в оригинальную таблицу, но в `heavy_orders` их не будет.

```
INSERT INTO heavy_orders
VALUES
(11900, 'FOLIG', 1, '2000-01-01', '2000-01-05', '2000-01-04', 1, 80, 'Folies gourmandes', '184, 
chaussee de Tournai', 'Lille', NULL, 59000, 'FRANCE'); - в данном случае freight = 80
```

Можно модифицировать **VIEW** так, чтобы фильтр во **VIEW** учитывался при вставке:

```
CREATE OR REPLACE VIEW heavy_orders AS
SELECT *
FROM orders
WHERE freight > 100
WITH {LOCAL|CASCADE} CHECK OPTION;
```

* **LOCAL** - сервер будет проверять соответствие вставляемых данных фильтру **VIEW**.

* **CASCADE** - **LOCAL** + проверка будет и для подлежащих **VIEW** (детей).

---

### Условное выражение CASE WHEN

* Представляет собой общее условное выражение, напоминающее операторы **if/else** в других языках программирования:

**Синтаксис**:

```
CASE 
    WHEN condition_1 THEN result_1 - if
    WHEN condition_2 THEN result_2 - elif
    [WHEN...]
    [ELSE result_n]
END
```

* **condition** - условие, возвращающее **bool**.
* **result** - результат или действие в случае с **PL** \ **pgSQL**.

В данном случае будет дополнительный столбец `amount` со значениями, соответствующими условиям:

```
SELECT product_name, unit_price, units_in_stock,
    CASE 
        WHEN units_in_stock >= 100 THEN 'lots of'
        WHEN units_in_stock >= 50 THEN 'average'
        WHEN units_in_stock < 50 THEN 'low number'
        ELSE 'unknown'
    END AS amount
FROM products;
```

---

### Условные выражения COALESCE и NULLIF

* **COALESCE**(`arg1`, `arg2`, ...); - принимает N аргументов одного типа и возвращает первый **!=NULL элемент**.   
  В случае, если все аргументы **NULL**, вернёт **NULL**.

```
SELECT order_id, order_date, COALESCE(ship_region, 'unknown') AS ship_region - если ship_region == NULL, будет выведено 'unknown'.
FROM orders
LIMIT 10;
```

* **NULLIF**(`arg1`, `arg2`) - сравнивает 2 аргумента и если они равны возвращает **NULL**.
  В случае, если они не равны, то вернёт `arg1`.

```
SELECT contact_name, COALESCE(NULLIF(city, ''), 'Unknown') as city - Если city == '', то будет 'Unknown', иначе будет city.
FROM customers;
```

---

### Функции в SQL

* **Функции** - объект БД, принимающий аргументы и возвращающий результат.

* **Функции** (хранимые процедуры) - компилируемы и хранятся на стороне БД, поэтому их вызов стоит дёшево.

* Возможно управлять безопасностью через регулирования доступа к **функциям**.


* Могут содержать **CRUD** (CREATE READ UPDATE DELETE) операции, как **SELECT**, **INSERT**, **UPDATE**, **DELETE**, ...

* Не могут содержать **COMMIT**, **SAVEPOINT** (TCL), **VACUUM** (utility).

**Делятся на**:

* SQL-функции.
* Процедурные (PL/pgSQL).
* Серверные функции (написанные на С) - редко.
* Собственные С-функции - редко.

**Синтаксис**:

```
CREATE [OR REPLACE] FUNCTION func_name(arg1 data_type, arg2 data_type,...) RETURNS data_type AS $$ 	 
    --logic
$$ LANGUAGE sql
```

* `$$` - открывают и закрывают тело функции (до 8 версии использовали кавычки).

* Изменение `REPLACE` **функции** имеет примерно такие же ограничения, что и **VIEW**:

**Вызов функции**:

```
SELECT func_name(arg1, arg2) AS something;
```

**Пример**:

```
CREATE FUNCTION fix_customer_region() RETURNS void AS $$ - void == не выводит ничего
    UPDATE orders
    SET ship_region = COALESCE(NULLIF(ship_region, NULL),'unknown')
$$ LANGUAGE sql;

SELECT fix_customer_region();
```

**Примеры функций**:

* `date_part('month', data_date);` - выведет номер месяца из `data_date`.

* `to_char();` - переводит всё в строку (смотреть документацию).

---

### Скалярные функции в SQL

* Функции, которые выводят единственное значение (**varchar**, **bigint**, ...).

```
CREATE FUNCTION get_total_number_of_goods() RETURNS bigint AS $$   
    SELECT SUM(units_in_stock)
    FROM products
$$ LANGUAGE sql;

SELECT get_total_number_of_goods() AS goods_cnt;
```

---

### Аргументы функции в SQL

* **IN** - входящие аргументы.
* **OUT** - исходящие аргументы.
* **INOUT** - и входящий, и исходящий аргумент.
* **DEFAULT** value - значение по умолчанию.
* **VARIADIC** - массив входящих параметров.

**IN**:

```
CREATE OR REPLACE FUNCTION get_product_price_by_name([IN] prod_name varchar) RETURNS real AS $$
    SELECT unit_price
    FROM products
    WHERE product_name = prod_name
$$ LANGUAGE sql;

SELECT get_product_price_by_name('Chocolade'); - выведет цену за товар под названием Chocolade.
```

**OUT**:

```
CREATE OR REPLACE FUNCTION get_price_boundaries(OUT max_price real, OUT min_price real) AS $$
    SELECT MAX(unit_price), MIN(unit_price) - записываются в указанные аргументы по порядку.
    FROM products
$$ LANGUAGE sql;

SELECT get_price_boundaries(); - выведет информацию в формате (data1, data2), где data1 = max_price и data2 = min_price.

SELECT * FROM get_price_boundaries(); - разобьёт данные по колонкам с соответствующими названиями.
```

**DEFAULT**:

```
CREATE OR REPLACE FUNCTION get_price_boundaries_by_discontinuity(IN is_discontinued int DEFAULT 1, OUT max_price real, OUT min_price real) AS $$
    SELECT MAX(unit_price), MIN(unit_price)
    FROM products
    WHERE discontinued = is_discontinued
$$ LANGUAGE sql;

SELECT get_price_boundaries_by_discontinuity([1]);
```

---

### Функции, возвращающие множество строк

* **RETURNS SETOF data_type** - возврат n-значений типа `data_type` (1 столбец).


* **RETURNS SETOF RECORD** - позволяет возвращать строки с несколькими столбцами разных типов.


* **RETURNS SETOF table_name** - если нужно вернуть все столбцы из таблицы или пользовательского типа.


* **RETURNS TABLE (column1_name data_type, ...)** - то же, что и **SETOF table_name**, но есть возможность явно указать
  возвращаемые столбцы.


* Возврат через **OUT-параметры**.

**RETURNS SETOF data_type**:

```
CREATE OR REPLACE FUNCTION get_average_prices_by_product_categories() RETURNS SETOF double precision AS $$
    SELECT AVG(unit_price)
    FROM products
    GROUP BY category_id
$$ LANGUAGE sql;

SELECT * FROM get_average_prices_by_product_categories()
```

**RETURNS SETOF RECORD**:

```
CREATE OR REPLACE FUNCTION get_average_prices_by_product_categories(OUT sum_price real, OUT avg_price float) RETURNS SETOF RECORD AS $$
    SELECT SUM(unit_price), AVG(unit_price)
    FROM products
    GROUP BY category_id
$$ LANGUAGE sql;

SELECT * FROM get_average_prices_by_product_categories(); - выведет все столбцы, что мы указалаи в аргументах, как OUT.

SELECT sum_price FROM get_average_prices_by_product_categories(); - выведет только столбец sum_price.
```

**RETURNS SETOF RECORD (случай без OUT)**:

```
CREATE OR REPLACE FUNCTION get_average_prices_by_product_categories() RETURNS SETOF RECORD AS $$
    SELECT SUM(unit_price), AVG(unit_price)
    FROM products
    GROUP BY category_id
$$ LANGUAGE sql;
                                                         
SELECT * FROM get_average_prices_by_product_categories() AS (sum_price real, avg_price float8); - рабочий, но не очень удобный способ.
                                                         ^ Так необходимо делать обязательно ^
```

**RETURNS SETOF table_name**:

```
CREATE OR REPLACE FUNCTION get_customers_by_country(customer_country varchar) RETURNS SETOF customers AS $$
    SELECT * - нужно выбрать все столбцы, иначе работать не будет
    FROM customers
    WHERE country = customer_country
$$ LANGUAGE sql;

SELECT * FROM get_customers_by_country('USA');

SELECT contact_name FROM get_customers_by_country('USA');
```

**RETURNS TABLE**:

```
CREATE OR REPLACE FUNCTION get_customers_by_country(customer_country varchar) RETURNS TABLE(char_code char, company_name varchar) AS $$
    SELECT customer_id, company_name - выводим то, что указали ранее.
    FROM customers
    WHERE country = customer_country
$$ LANGUAGE sql;

SELECT * FROM get_customers_by_country('USA'); - выведет таблицу из двух столбцов char_code и company_name.
```

---

### Функции PL/pgSQL (Procedural Language/PostgreSQL)

**Преимущество над функциями в SQL**:

* Можно создавать переменные.

* Можно создавать циклы.

* Возврат значения через **RETURN** (вместо **SELECT**) или **RETURN QUERY** (в дополнение к **SELECT**).

**Синтаксис**:

```
CREATE [OR REPLACE] FUNCTION func_name(arg1 data_type, arg2 data_type,...) RETURNS data_type AS $$ 
BEGIN 
    --logic
END[;]
$$ LANGUAGE plpgsql
```

* **BEGIN** / **END** - тело метода (дело не в транзакциях).

**Скалярные функции в PL/pgSQL**:

* Функции, которые выводят единственное значение (**varchar**, **bigint**, ...).

```
CREATE OR REPLACE FUNCTION get_total_number_of_goods() RETURNS bigint AS $$
BEGIN   
    RETURN SUM(units_in_stock)
    FROM products;
END;
$$ LANGUAGE plpgsql;

SELECT get_total_number_of_goods();
```

**Аргументы функции в PL/pgSQL**:

* Работа с аргументами почти вся аналогична обычным **SQL-функциям**.

**IN**:

```
CREATE OR REPLACE FUNCTION get_sum([IN] x int, [IN] y int, OUT result int) AS $$
BEGIN
    result := x + y;
    RETURN; - используется, чтобы досрочо выйти из функции.
END;
$$ LANGUAGE plpgsql;

SELECT get_sum(2,3);
```

* `:=` - то же самое, что и `=`, но `=` ещё работает как сравнение (`==`), что может запутать.

**OUT**:

```
CREATE OR REPLACE FUNCTION get_price_boundaries(OUT max_price real, OUT min_price real) AS $$
BEGIN      
    max_price := MAX(unit_price) FROM products; 
    min_price := MIN(unit_price) FROM products;     
ИЛИ 
    SELECT MAX(unit_price), MIN(unit_price)
    INTO max_price, min_price
    FROM products;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_price_boundaries();
```

**Возврат наборов данных**:

**RETURNS SETOF**:

```
CREATE OR REPLACE FUNCTION get_customers_by_country(IN customer_country varchar) RETURNS SETOF customers AS $$
BEGIN
    RETURN QUERY
    SELECT * 
    FROM customers
    WHERE country = customer_country;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_customers_by_country('USA'); 
```

---

### Декларация переменных в функциях PL/pgSQL

Одно из благ **PL/pgSQL** это возможность декларировать переменные внутри функций.

**Синтаксис**:

```
CREATE [OR REPLACE] FUNCTION func_name(arg1 data_type, arg2 data_type,...) RETURNS data_type AS $$ 
DECLARE
    var_name data_type;
BEGIN 
    --logic
END[;]
$$ LANGUAGE plpgsql
```

**Примеры**:

```
CREATE OR REPLACE FUNCTION get_triangle_square(ab real, bc real, ac real) RETURNS real AS $$
DECLARE
    perimetr_half real;
BEGIN
    perimetr_half := (ab + bc + ac) / 2;
    RETURN sqrt(perimetr_half * (perimetr_half - ab) * (perimetr_half - bc) * (perimetr_half - ac));
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_triangle_square(3, 4, 5);
```

```
CREATE OR REPLACE FUNCTION calc_middle_price() RETURNS SETOF products AS $$
DECLARE
    avg_price real;
    low_price real;
    high_price real;
BEGIN
    SELECT AVG(unit_price)
    INTO avg_price
    FROM products;
    
    low_price = 0.75 * avg_price;
    high_price = 1.25 * avg_price;
    
    RETURN QUERY
    SELECT *
    FROM products
    WHERE unit_price BETWEEN low_price AND high_price;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM calc_middle_price();
```

---

### Логические ветвления (IF/ELSE) в функциях PL/pgSQL

**Синтаксис**:

```
IF expression1 THEN
    -- logic
ELS[E]IF expression2 THEN
    -- logic
ELSE
    -- logic
END IF;
```

**Пример**:

```
CREATE OR REPLACE FUNCTION temp_convert(IN temperature real, to_celsius bool DEFAULT true) RETURNS real AS $$
DECLARE
	converted_temp real;
BEGIN
	IF to_celsius THEN
		converted_temp := (5.0/9.0) * (temperature - 32);
	ELSE
		converted_temp := temperature * (9.0/5.0) + 32;
	END IF;
	RETURN converted_temp;
END;
$$ LANGUAGE plpgsql;
```

---

### Циклы в функциях PL/pgSQL

* **WHILE**:

```
WHILE expression
LOOP
    --logic
END LOOP;
```

**Пример**:

```
CREATE OR REPLACE FUNCTION fib_num(IN num int) RETURNS int AS $$
DECLARE
    counter int = 0; - задание значения по умолчанию.
    i int = 1;
    j int = 1;
BEGIN
    IF num < 1 THEN
        RETURN 0;
    ELSE
        WHILE counter < num - 1
        LOOP
			counter = counter + 1;
        	SELECT j, i+j
        	INTO i, j; 
        END LOOP;
        RETURN i;
	END IF;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM fib_num(3);
```

* **EXIT WHEN**:

```
LOOP
    EXIT WHEN expression;
    --logic
END LOOP;
```

**Пример**:

```
CREATE OR REPLACE FUNCTION fib_num(IN num int) RETURNS int AS $$
DECLARE
    counter int = 0;
    i int = 1;
    j int = 1;
BEGIN
    IF num < 1 THEN
        RETURN 0;
    ELSE
        LOOP
			EXIT WHEN counter >= num - 1;
			counter = counter + 1;
        	SELECT j, i+j
        	INTO i, j; 
        END LOOP;
        RETURN i;
	END IF;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM fib_num(2);
```

* **FOR**:

```
FOR counter IN [REVERSE] a..b [BY step_num]
LOOP
    --logic
END LOOP;
```

**Пример**:

```
CREATE OR REPLACE FUNCTION fib_num(IN num int) RETURNS int AS $$
DECLARE
    i int = 1;
    j int = 1;
BEGIN
    IF num < 1 THEN
        RETURN 0;
    ELSE    
        FOR counter in 0..num-2 [BY 1]
        LOOP
        	SELECT j, i+j, counter+1 
        	INTO i, j, counter; 
        END LOOP;
        RETURN i;
	END IF;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM fib_num(3);
```

* **Внутренние функции**:

`EXIT [WHEN expression]` - досрочный выход из цикла (**break**) при условии.

`CONTINUE WHEN expression` - переход на следующую итерацию цикла (**continue**) при условии.

---

### Анонимный блок кода DO

* Блок кода воспринимается, как если бы это было тело функции, которая **не имеет параметров** и **возвращает void**.

* Этот код разбирается и выполняется **один раз**.

* Есть часть **PL/pgSQL**.

```
DO $$
BEGIN
    --logic
END $$;
```

**Пример**:

```
DO $$
BEGIN
    FOR counter IN 1..5 BY 2
    LOOP
        RAISE NOTICE 'Counter:  %', counter; - вывод сообщение в Messages.
    END LOOP;
END $$;
```

---

### RETURN NEXT в функциях PL/pgSQL

* Является чем-то наподобие **yield** в **python**, те добавляет данные в результирующий набор (выводит в случае с
  **python**), а после продолжает работу функции.

* По большому счету дерьмо из-за производительности и почти нигде не используется.

**Примеры**:

```
CREATE OR REPLACE FUNCTION return_ints() RETURNS SETOF int AS $$
BEGIN
    RETURN NEXT 1;
    RETURN NEXT 2;
    RETURN NEXT 3;
END;
$$ LANGUAGE plpgsql;

SELECT return_ints(); - будет выведен столбец с 3 записями (строками).
```

```
CREATE OR REPLACE FUNCTION after_christmas_sale() RETURNS SETOF products AS $$
DECLARE
    product record; - record == запись (строчка).
BEGIN
    FOR product IN SELECT * FROM products - product является копией строчки из products.
    LOOP
        IF product.category_id IN (1, 4, 8) THEN
            product.unit_price = product.unit_price * 0.8;
        ELSEIF product.category_id IN (2, 3, 7) THEN
            product.unit_price = product.unit_price * 0.75;
        ELSE
            product.unit_price = product.unit_price * 1.1;     
        END IF;
        RETURN NEXT product;               
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM after_christmas_sale();
```

---

### Обработка ошибок EXCEPTION

* Для выбрасывания сообщений (в **Messages**) используется **RAISE**.

* Для обработки ошибок (поимки исключений) используется хэндлер **EXCEPTION**. Он доступен только в **PL**/**pgSQL**
  функциях.

**Синтаксис**:

```
RAISE {LEVEL} 'message %', arg_name; - выбрасывание сообщения, соответствующего уровня.
```

```
EXCEPTION WHEN {SQLSTATE 'num'|OTHERS} THEN handling_logic; - обработка ошибки.
```

**Уровни**:

* **LEVEL** - уровень серьёзности сообщения:
    * `DEBUG` - отладка.
    * `LOG` - лог.
    * `INFO` - информация.
    * `NOTICE` - замечание.
    * `WARNING` - потенциальная опасность.
    * `EXCEPTION` - исключение / ошибка (абортирует текущую транзакцию).


* В этом блоке мы работаем с `EXCEPTION`.

**Параметры сервера**:

* **log_min_messages** регулирует уровень сообщений, которые будут писать в лог сервера (**WARNING** - по умолчанию).

* **client_min_messages** регулирует уровень сообщений, которые будут передаваться вызывающей стороне (**NOTICE** - по
  умолчанию).

**Параметры RAISE**:

* **HINT** - подсказка для решения проблемы.

* **ERRCODE** - особый номер ошибки (от `'00000'` до `'99999'`).

* Параметры присоединяются с помощью **USING**:

```
RAISE EXCEPTION 'Invalid billing number: %', number USING HINT = 'Check out the billing number', ERRCODE='12881';
```

**Примеры**:

* Отправка исключения

```
CREATE OR REPLACE FUNCTION get_season(month_number int) RETURNS text AS $$
BEGIN
    IF month_number > 12 OR month_number < 1 THEN 
        RAISE EXCEPTION 'Invalid month. You passed: (%)', month_number 
        USING HINT = 'Allowed from 1 to 12', ERRCODE='12881'; - выбрасываем ошибки с параметрами.
	END IF;
	
    IF month_number BETWEEN 3 AND 5 THEN
        RETURN 'Spring';
    ELSIF month_number BETWEEN 6 AND 8 THEN
        RETURN 'Summer';
    ELSIF month_number BETWEEN 9 AND 11 THEN
        RETURN 'Autumn';
    ELSE
        RETURN 'Winter';
    END IF;
END;
$$ LANGUAGE plpgsql;

SELECT get_season(13);
```

* Поимка и обработка исключения:

```
CREATE OR REPLACE FUNCTION get_season_caller(month_number int) RETURNS text AS $$
BEGIN
	RETURN get_season(month_number); - эта строчка может выбросить EXCEPTION, поэтому сделаем обработчик.
	EXCEPTION 
	WHEN SQLSTATE '12881' THEN
		RAISE INFO 'A problem, nothing special.';
		RAISE INFO 'Error msg: %', SQLERRM;
		RAISE INFO 'Error code: %', SQLSTATE;
		RETURN NULL;
	WHEN OTHERS THEN - обработка всех остальных исключений.
	    RAISE INFO 'All other exceptions.';
	    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

SELECT get_season_caller(13);
```

* Вывод дополнительных данных ошибки при помощи **GET STACKED DIAGNOSTICS**:

```
CREATE OR REPLACE FUNCTION get_season_caller(month_number int) RETURNS text AS $$
DECLARE
	err_ctx text;
	err_msg text;
	err_details text;
	err_code text;
BEGIN
	RETURN get_season(month_number); - эта строчка потенциально может выбросить EXCEPTION, поэтому сделаем обработчик.
	EXCEPTION 
	WHEN SQLSTATE '12881' THEN
		GET STACKED DIAGNOSTICS
			err_ctx = PG_EXCEPTION_CONTEXT,
			err_msg = MESSAGE_TEXT,
			err_details	= PG_EXCEPTION_DETAIL,
			err_code = RETURNED_SQLSTATE;
			
		RAISE INFO 'My custome handler:';
		RAISE INFO 'Error msg: %', err_msg;
		RAISE INFO 'Error details: %', err_details;
		RAISE INFO 'Error code: %', err_code;
		RAISE INFO 'Error ctx: %', err_ctx;
		RETURN NULL;
END;
$$ LANGUAGE plpgsql;

SELECT get_season_caller(13);
```

### Приведение типов данных

**Безопасность типов**:

* **SQL** - строго **типизированный** язык.

* Разрешена **перегрузка** функций (одно название, разные типы аргументов).

* Если типы между собой совместимы - интерпретатор старается произвести неявное преобразование (автоматическое
  преобразование данных одного типа в данные другого типа на основе встроенного набора правил преобразования).

* Для **неявного** преобразования от нас ничего не требуется.

* Для **явного** преобразования используется:
    * `CAST(expression AS target_type)` - совместимо с **SQL-стандартом**.
    * `expression::target_type` - несовместимо с **SQL-стандартом**.

**Пример**:

```
CREATE OR REPLACE FUNCTION type_testing(number int) RETURNS void AS $$
BEGIN
    RAISE NOTICE 'zaza number is %', number;
END;
$$ LANGUAGE plpgsql;

SELECT type_testing(CAST(1.9 AS int));
SELECT type_testing('3'::int); - перевод строки c целым числом в целое число.
SELECT type_testing('1.5'::numeric::int); - перевод строки c вещественным числом в целое число.
```

### Индексы

* Это структура данных, ускоряющая выборку из таблицы за счет дополнительных операций записи и пространства на диске,
  используемых для хранения структуры данных и поддержания её в актуальном состоянии.

* Гарантий, что будет использован именно индексный поиск нет. Всё зависит от запроса.


* **Индекс** - объект БД, который можно создавать и удалять.

* Позволяет искать значения без полного перебора.

* По **PRIMARY KEY** и **UNIQUE** столбцам индекс создаётся автоматически.

**Методы сканирования**:

* Индексное (**index scan**)

* Исключительно индексное сканирование (**index only scan**)

* Сканирование по битовой карте (**bitmap scan**)

* Последовательное сканирование (**sequential scan**)


* Метод сканирование выбирается системой автоматически

* Индексное сканирование будет применяться к запросу, где не много данных, что нельзя сказать про последовательное
  (проход по всем).

**Виды индексов**:

```
SELECT amname FROM pg_am; - выведет список всех доступных видов индексов на сервере
```

* **B-tree** (сбалансированное дерево)

* **HASH**

* **GiST** (обобщенное дерево поиска)

* **GIN** (обобщенный обратный)

* **SP-GiST** (GiST с двоичным разбиением пространства)

* **BRIN** (блочно-диапазонный)

**B-tree**:

* Создаётся по умолчанию `CREATE INDEX index_name ON table_name (column_name);`.

* Поддерживает операции **<**, **>**, **<=**, **>=**, **=**.

* Поддерживает `LIKE 'abc%'` (но не `'%abc'`).

* Индексирует **NULL**.

* Сложность поиска **O(logN)**.

**HASH**:

* `CREATE INDEX index_name ON table_name USING HASH (column_name);`.

* Поддерживает только операцию **=**.

* Не рекомендуется к применению (в общем и целом).

* Сложность поиска **O(1)**.

**EXPLAIN**:

* Если есть проблемы с производительностью надо понять "откуда растут ноги".

* `EXPLAIN query` позволяет посмотреть на план выполнения запроса.

* `EXPLAIN ANALYZE query` выполняет запрос, показывает план и реальность.

**ANALYZE**:

* Собирает статистику по данным таблицы.

* Планировщик смотрит на статистику при построении плана.

* `ANALYZE [table_name[(column1_name, column2_name, ...)]]` - сбор статистики.

**Примеры**:

* Создаём таблицу с рандомными данными:

```
DROP TABLE IF EXISTS test;

CREATE TABLE test
(
	id int,
	reason text,
	annotation text 
);

INSERT INTO test(id, reason, annotation)
SELECT s.id, md5(random()::text), UPPER(md5(random()::text)) - хеш в верхнем регистре от рандомного числа между 0 и 1.
FROM generate_series(1,10000000) AS s(id); - присваиваем послед-ти generate_series псевдоним s с названием столбца id.
```

* **INDEX** по одному столбцу:

```
EXPLAIN ANALYZE
SELECT *
FROM test
WHERE id = 3100000;

CREATE INDEX idx_test_id ON test(id); - ускорит запрос с 790мс до 53мс (поменяется метод сканирования).
```

* **INDEX** по двум столбцам:

```
EXPLAIN ANALYZE
SELECT *
FROM test
WHERE reason LIKE 'ac3%' AND annotation LIKE 'AC2%';

CREATE INDEX idx_test_reason_annotation ON test(reason, annotation); - этот INDEX будет работать ещё для выборок по первыму из столбцов.
```

* **INDEX** по выражениям:

```
EXPLAIN ANALYZE
SELECT *
FROM test
WHERE LOWER(annotation) LIKE 'ac23b%';

CREATE INDEX idx_test_annotation_lower ON test(LOWER(annotation));
```

* **INDEX** для поиска по тексту:

```
EXPLAIN ANALYZE
SELECT *
FROM test
WHERE reason LIKE '%bca%';

CREATE EXTENSION pg_trgm; - подключение расширения

CREATE INDEX trgm_idx_test_reason ON test USING GIN (reason gin_trgm_ops); 
```

---

### Массивы

* Массив - коллекция данных одного типа.

* Столбцы и переменные могут объявляться как массив.

* Массивы могут быть многомерными.

**Задание массивов**:

* SQL-стандарт:
    * `array_name int ARRAY;`
    * `array_name int ARRAY[size_num];`


* Postgres:
    * `array_name int[];`
    * `array_name int[size_num];`


* Явно указанный размер ни на что не влияет.  
  Он чисто для документации.

**Инициализация массивов**:

* `'{"a", "b", "c"}'` или `ARRAY['a', 'b', 'c']`.


* `'{1, 2, 3}'` или `ARRAY[1, 2, 3]`.


* `'{{1, 2, 3}, {1, 2, 3}, {1, 2, 3}}'` или `ARRAY[[1,2,3], [1,2,3], [1,2,3]]`.

**Обращение к массивам**:

* `array_name[index]` - взятие элемента по индексу (от 1).


* `array_dims(array_name)` - возвращает размерность массива.


* `array_length(array_name, array_dim)` - возвращает длину массива.


* Слайсинг (срезы):
    * `array_name[1:3]` - с 1 по 3 элемент.
    * `array_name[:4]` - с 1 по 4 элемент.
    * `array_name[2:]` - со 2 по последний элемент.

Массивы - это не множества; необходимость поиска определенных элементов в массиве может быть признаком неудачно
сконструированной базы данных. Возможно, вместо массива лучше использовать отдельную таблицу, строки которой будут
содержать данные элементов массива. Это может быть лучше и для поиска, и для работы с большим количеством элементов.

**Примеры**:

* Создание таблицы:

```
DROP TABLE IF EXISTS chess_game;

CREATE TABLE chess_game (
	white_player text,
	black_player text,
	moves text[],
	final_state text[][]
);

INSERT INTO chess_game (white_player, black_player, moves, final_state)
VALUES ('Svyatoslav', 'Nina', '{"d4", "d5", "c4", "c6"}', ARRAY[
           ['Ra8', 'Qe8', 'x', 'x', 'x', 'x', 'x', 'x'],
           ['a7', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
           ['Kb5', 'Bc5', 'd5', 'x', 'x', 'x', 'x', 'x']]);
		   
SELECT moves[3:]
FROM chess_game;

SELECT array_dims(moves), array_dims(final_state)
FROM chess_game;

SELECT array_length(moves, 1), array_length(final_state, 1), array_length(final_state, 2)
FROM chess_game;
```

* **UPDATE** в массивах:

```
UPDATE chess_game
SET moves = '{"e4", "d6", "d4", "kf6"}'; - замена всего массива.

UPDATE chess_game
SET moves[2] = 'g6'; - замена элемента массива.
```

* **Поиск** в массивах:

```
SELECT *
FROM chess_game
WHERE 'g6' = ANY(moves);
```

**Операторы в массивах**:

* Операторы сравнения:
    * **=** `true` если совпадают значения и их последовательность.
    * **>** `true` если в первой неравной паре, элемент слева больше.
    * **<** `true` если в первой неравной паре, элемент слева меньше.

* Containment-операторы:
    * **@>** `true` если правый массив включает все элементы левого.
    * **@<** `true` если левый массив включает все элементы правого.

* Оператор пересечения:
    * **&&** `true` если массивах хотя бы один одинаковый элемент.

```
SELECT *
FROM chess_game
WHERE moves && ARRAY['g6'];
```

---

### VARIADIC (*args)

* Чтобы передавать n параметров (одного типа) в функцию, нужно объявить аргумент как **VARIADIC**:  
  `VARIADIC arg_name data_type[]`

**Примеры**:

* Функция, которая принимает числа и выводит только четные:

```
CREATE OR REPLACE FUNCTION filter_even(VARIADIC numbers int[]) RETURNS SETOF int AS $$
BEGIN
    FOR counter IN 1..array_length(numbers, 1)
    LOOP
        IF numbers[counter] % 2 = 0 THEN
            RETURN NEXT numbers[counter];
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT filter_even(1, 6, 3, 5, 12);
```

* Вместо стандартного **FOR** можно использовать **FOREACH**:

```
CREATE OR REPLACE FUNCTION filter_even(VARIADIC numbers int[]) RETURNS SETOF int AS $$
DECLARE
    iter int;
BEGIN
    FOREACH iter in ARRAY numbers
    LOOP
        CONTINUE WHEN iter % 2 = 1;
        RETURN NEXT iter;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT filter_even(1, 6, 3, 5, 12);
```

* Чтобы передать массив в **VARIADIC-аргумент**, надо перед массивом прописать ключевое слово **VARIADIC**.

```
SELECT filter_even(VARIADIC {1, 6, 3, 5, 12});
```

--- 

### Пользовательские типы данных

* **Домен** - пользовательский тип данных с ограничением.

* **Составной тип** - тип, объединяющий логически взаимосвязанные данные без создания полноценной таблицы.

* **Перечисление** - позволяет эмулировать простейшие справочные таблицы.

---

### Домен

* Пользовательский тип данных с ограничениями.

**Создание домена**:

```
CREATE DOMAIN domain_name AS data_type CONSTRAINTS;
```

**Изменение домена**:

```
ALTER DOMAIN domain_name ADD CONSTRAINT new_constraint [NOT VALID];
```

* **NOT VALID** - позволит добавить ограничение даже если существующие значения в таблице под него не подходят.

```
ALTER DOMAIN domain_name VALIDATE CONSTRAINT new_constraint; - сервер проверяет, все ли данные нашего типа не нарушают ограничение.
```

**Удаление домена**:

```
DROP DOMAIN [IF EXISTS] domain_name;
```

**Примеры**:

* Создание домена с ограничением через регулярное выражение:

```
CREATE DOMAIN text_no_space_null AS text NOT NULL CHECK (value ~ '^(?!\s*$).+');

CREATE TABLE agent(
	first_name text_no_space_null,
	last_name text_no_space_null
);

INSERT INTO agent
VALUES ('bob', 'taylor');
```

* `^(?!\s*$).+` - гарантирует, что строка не состоит только из пробелов или пуста, и содержит хотя бы один символ.

```
INSERT INTO agent
VALUES ('1234567', '1234567');

ALTER DOMAIN text_no_space_null ADD CONSTRAINT text_no_space_null_length6 CHECK(length(value) <= 6) NOT VALID;

ALTER DOMAIN text_no_space_null VALIDATE CONSTRAINT text_no_space_null_length6;
```

* **VALIDATE** выдаст ошибку, тк есть данные типа нашего домена, которые не подходят под ограничение.

---

### Составной тип данных (композитный)

* Тип данных, состоящий из нескольких полей имеющих свой тип.

* Нельзя задавать ограничения **CONSTRAINT**. Поэтому не так часто используются в таблицах.

* Зато часто используются для возврата данных из функций.

* Чаще всего не нужен составной тип. Как правило, таблицы лучше.

**Создание составного типа**:

```
CREATE TYPE type_name AS (
    field1 type,
    field2 type
);
```

**Создание экземпляра соответствующего типа**:

```
'(1, 2, "text")' 
```

Или так:

```
ROW(1, 2, 'text')
```

**Удаление типа**:

```
DROP TYPE [IF EXISTS] type_name [CASCADE];
```

**Примеры**:

* Вывод составных данных из функции:

```
CREATE TYPE price_bounds AS (
	max_price real,
	min_proce real
);

CREATE OR REPLACE FUNCTION get_price_boundaries() RETURNS price_bounds AS $$
	SELECT max(unit_price), min(unit_price)
	FROM products;
$$ LANGUAGE sql;

SELECT * FROM get_price_boundaries();
```

* Вставка составных данных в таблицу:

```
CREATE TYPE complex AS (
    real_part real,
    imaginary_part real
);


CREATE TABLE complex_numbers(
	number_id serial PRIMARY KEY,
	value complex
);

INSERT INTO complex_numbers (value)
VALUES
(ROW(12, 1)),
('(2, -1)' );
```

* **SELECT** составных данных:

```
SELECT *
FROM complex_numbers;
```

```
SELECT ([complex_number.]value).real_part - вывод конкретного столбца колонки составного типа.
FROM complex_numbers;
```

```
SELECT ([complex_number.]value).* - вывод всех полей колонки составного типа.
FROM complex_numbers;
```

* **UPDATE** составных данных:

```
UPDATE complex_numbers
SET value = ROW(1, 2) - изменение всего значения составного типа.
WHERE number_id = 1;    
```

```
UPDATE complex_numbers
SET value.real_part = 3 - изменение конкретного поля значения составного типа.
WHERE number_id = 1;    
```

```
UPDATE complex_numbers
SET value.real_part = (value).real_part + 3
WHERE number_id = 1;    
```

---

### Перечисление (ENUM)

* Служит заменой элементарной справочной таблицы.

* Между собой **ENUM** сравнивать нельзя.

* Значения регистрозависимы.

* Накладывает ограничение (в этом смысл перечисления) на добавление в колонку типа перечисления значения, отсутствующего
  в перечислении.

**Синтаксис**:

```
CREATE TYPE type_name AS ENUM 
(value1, 'value2', ...);
```

**Примеры**:

* **Создание перечисления**:

```
CREATE TYPE chess_title AS ENUM 
('Candidate Master',
'FIDE Master',
'International Master');
```

* **Добавление значений**:

```
ALTER TYPE chess_title
ADD VALUE 'Grand Master' [{AFTER|BEFORE} 'International Master'];
```

* **Вывод всех значений перечисления**:

```
SELECT enum_range(null::chess_title);
```

* **Использование перечисления в таблице**:

```
CREATE TABLE chess_player(
	player_id serial PRIMARY KEY,
	first_name text,
	last_name text,
	title_id int chess_title
);

INSERT INTO chess_player(first_name, last_name, title_id)
VALUES
('Wesley', 'So', 'Grand Master'), - пройдёт.
('Vlad', 'Kramnik', 'Zaza Boss'); - не выйдет, тк значения нет в chess_title. 
```

---

### Продвинутая группировка

* **GROUP BY** даёт возможность делать простые группировки

* Но как для отчётности сформировать **подытоги и общие итоги**?

* Для решения этих задач есть **GROUPING SETS**, **ROLLUP** и **CUBE**.

---

### GROUPING SETS

* Набор столбцов в **GROUP BY** - есть **GROUPING SET**.

**Синтаксис**:

```
GROUP BY GROUPING SETS ((col_a), (col_a, col_b)) - вернёт объединение группировок по (col_a), (col_a, col_b).
```

* Возможны любые комбинации столбцов.

**Пример**:

```
SELECT supplier_id, category_id, SUM(units_in_stock)
FROM products
GROUP BY GROUPING SETS ((supplier_id), (supplier_id, category_id))
ORDER BY supplier_id, category_id NULLS FIRST;
```

* Будет выведен список, где для каждого **supplier_id** сначала идёт общее значение, а далее разбитые по
  **category_id**.

---

### ROLLUP

* Генерирует агрегированный набор для иерархии значений в столбцах указанных в скобках (в порядке следования).

**Синтаксис**:

```
ROLLUP (coll_a, coll_b, coll_c); == GROUP BY GROUPING SETS ((col_a), (col_a, col_b), (col_a, col_b, col_c));
```

**Пример**:

```
SELECT supplier_id, category_id, SUM(units_in_stock)
FROM products
GROUP BY ROLLUP (supplier_id, category_id)
ORDER BY supplier_id, category_id NULLS FIRST;
```

* Выйдет то же самое, что и в примере для **GROUPING SETS**.

---

### CUBE

* Генерирует агрегированный набор для всех комбинаций значений в столбцах указанных в скобках.

**Синтаксис**:

```
ROLLUP (coll_a, coll_b, coll_c); == GROUP BY GROUPING SETS ((col_a), (col_a, col_b), (col_a, col_b, col_c));
```

**Пример**:

```
SELECT supplier_id, category_id, SUM(units_in_stock)
FROM products
GROUP BY CUBE (supplier_id, category_id)
ORDER BY supplier_id, category_id NULLS FIRST;
```

* Выйдет то же самое, что и в примере для **GROUPING SETS** и **ROLL UP** + группировка по `category_id`.

--- 

### Клиент psql

* **psql** - клиентское консольное приложение.


* Можно либо:
    * Добавить путь к папке **psql** в **PATH** (`C:\Program Files\PostgreSQL\16\bin`) и работать через консоль.

    * Либо запустить **psql Shell** установленный в системе.

**Основные команды**:

* `\?` - список команд psql.


* `\q` - выйти из psql.


* `\l` - список БД.


* `\dn` - список схем.


* `\dt` - все таблицы в текущей БД.


* `\dv` - все представления БД.


* `\df` - все функции в БД.


* `\du` - все роли на экземпляре кластера.


* `\c db_name` - переключиться на БД.


* `\d table_name` - описание таблицы.


* `\i file_name` - выполнить команды из файла.

**Подключение к серверу**:

```
psql --host=localhost --port=5432 [--dbname=postgres] --username=postgres - консоль.
```

В **psql Shell** просто следовать инструкции.

* Для полноценной работы лучше использовать **psql Shell**.

* Запросы нужно просто отправлять обычным текстом в консоль (обязательно `;` на конце).

---

### Импорт данных

* [Сайт с дата-сетами](https://www.kaggle.com/datasets).


* **.csv** - лучший формат для работы с данными.


1. Создаём **БД** и **таблицу** с полями, типы данных которые должны соответствовать колонкам **.csv-файла**.


2. Открываем **psql** и заходим в нужную нам **БД**.


3. `\copy table_name(fields) FROM 'csv_file_path' DELIMITER ',' [CSV HEADER];` - копируем данные в созданную таблицу.

* В некоторых **.csv-файлах** есть заголовок с названиями столбцов.
  **CSV HEADER** - даёт серверу понять, что первую строчку копировать не надо.

---

### Common Table Expressions (CTE)

* Позволяют строить временные таблицы (или представления) в рамках большого запроса.

* Присваивая имя такой временной таблице (подзапросу), мы можем её переиспользовать.

* Внутри подзапроса можно использовать **INSERT**, **UPDATE**, **DELETE**.

* **CTE** выполняется единожды, результат кешируется (не всегда, см план выполнения).

* Длинные и сложные запросы можно отрефакторить в **CTE**, повышая чистоту и читабельность кода.

**Синтаксис**:

```
WITH name AS (
    SELECT clause
)
SELECT ...;
```

**Примеры**:

```
WITH customer_countries AS 
(
	SELECT country FROM customers
)
SELECT company_name
FROM suppliers
WHERE country IN (SELECT * FROM customer_countries);
```

* Использование нескольких **CTE**

```
WITH name1 AS 
(...),
name2 AS
(...),
...
```

**Рекурсивный CTE**:

* Создаём таблицу и вставляем данные:

```
CREATE TABLE employee (
	employee_id int PRIMARY KEY,
	first_name varchar NOT NULL,
	last_name varchar NOT NULL,
	manager_id int,
	FOREIGN KEY (manager_id) REFERENCES employee(employee_id)
);

INSERT INTO employee
(employee_id, first_name, last_name, manager_id)
VALUES
(1, 'Windy', 'Hays', NULL),
(2, 'Ava', 'Christensen', 1),
(3, 'Anna', 'Reeves', 2);
```

* Иерархический вывод сотрудников с помощью [рекурсивного **CTE**](https://eax.me/postgresql-recursive-queries/):

```
WITH RECURSIVE submission(sub_line, employee_id) AS - задаём рекурсию с 2 столбами.
(
	SELECT last_name, employee_id FROM employee WHERE manager_id IS NULL - начальная часть.
	UNION ALL - после этого идёт рекурсивная часть.
	SELECT sub_line || ' -> ' || e.last_name, e.employee_id
	FROM submission s
	JOIN employee e ON e.manager_id = s.employee_id
)
SELECT * FROM submission;
```

---

### Оконные функции

* Позволяют обрабатывать группы строк без образования группировок в результирующем наборе.

* Очень крутая возможность современного **SQL**.


* Отрабатывают после **JOIN**, **WHERE**, **GROUP BY**, **HAVING**, но после **ORDER BY**.

* Делятся на:
    * Агрегатные функции - **MIN**, **MAX**, **COUNT**, **SUM**, **AVG**.
    * Функции ранжирования - **ROW_NUMBER**, **RANK**, **LAG**, **LEAD**.

**Синтаксис**:

```
function OVER ([expression])
```

* **OVER()** - одна большая группа, состоящая из всех строк таблицы.

```
function OVER ([PARTITION BY expression], [ORDER BY expression])
```

* **PARTITION BY** ~ **GROUP BY**.

* **ORDER BY** используется для определения порядка, в котором строки будут обрабатываться для нарастающего итога.

**Примеры**:

* Сравнение цен продукта со средней в его категории (обычный **GROUP BY** не справится):

```
SELECT category_id, category_name, product_name, 
unit_price, AVG(unit_price) OVER (PARTITION BY category_id) AS avg_price
FROM products
JOIN categories USING(category_id);
```

* Вывод нарастающего итога по продуктам заказов:

```
SELECT order_id, order_date, product_id, customer_id, unit_price AS sub_total,
		SUM(unit_price) OVER (PARTITION BY order_id ORDER BY product_id)
FROM orders
JOIN order_details USING(order_id)
ORDER BY order_id;
```

* Вывод общего нарастающего итога

```
SELECT order_id, order_date, product_id, customer_id, unit_price AS sub_total,
		SUM(unit_price) OVER (ORDER BY row_id) - делаем нарастающий итог по номерам строк
FROM (
	SELECT order_id, order_date, product_id, customer_id, unit_price,
		ROW_NUMBER() OVER() AS row_id - делаем колонку с номера строк
	FROM orders
	JOIN order_details USING(order_id)
) subquery
ORDER BY order_id;
```

* Вывод N записей с условием на оконную функцию:

```
SELECT *
FROM (SELECT product_id, product_name, category_id, unit_price, units_in_stock,
	 ROW_NUMBER() OVER(ORDER BY unit_price) AS nth
	 FROM products
	 ) AS sorted_prices
WHERE nth < 10
ORDER BY unit_price;
```

---

### Функции ранжирования

* **ROW_NUMBER** - присвоение уникального значения строке.

* **RANK** - (с пропусками) присвоение ранга (веса) строкам.

* **DENSE_RANK** - (без пропусков) присвоение ранга (веса) строкам.

* **LAG** - присвоение значения текущей строке, основанное на значении в предыдущей.

* **LEAD** - присвоение значения текущей строке, основанное на значении следующей.


* В **LEAD** и **LAG** можно передавать смешение **OFFSET**.

**RANK**:

* Присвоение ранга по уникальности `units_in_stock`:

```
SELECT product_name, units_in_stock, 
	RANK() OVER(ORDER BY units_in_stock)
FROM products;
```

* Вывод N записей с условием на оконную функцию:

```
SELECT *
FROM
(
    SELECT order_id, product_id, unit_price, quantity,
        RANK() OVER(PARTITION BY order_id ORDER BY quantity) AS rank_quant
    FROM orders
    JOIN order_details USING(order_id)
) AS subquery
WHERE rank_quant <= 5;
```

**DENSE_RANK**:

* Присвоение ранга по уникальности `units_in_stock`:

```
SELECT product_name, units_in_stock, 
	DENSE_RANK() OVER(ORDER BY units_in_stock)
FROM products;
``` 

* Присвоение ранга по правилу:

```
SELECT product_name, units_in_stock, 
	DENSE_RANK() OVER(
	    ORDER BY 
	        CASE
	            WHEN units_in_stock > 80 THEN 1
	            WHEN units_in_stock BETWEEN 31 AND 79 THEN 2
	            ELSE 3
	        END)
FROM products;
``` 

**LAG**:

* Присвоение значения по разнице цены с предыдущей строкой:

```
SELECT product_name, unit_price, 
	LAG(unit_price) OVER(ORDER BY unit_price) - unit_price AS price_lag
FROM products
ORDER BY unit_price;
``` 

**LEAD**:

* Присвоение значения по разнице цены с последующей строкой:

```
SELECT product_name, unit_price, 
	LEAD(unit_price) OVER(ORDER BY unit_price) - unit_price AS price_lag
FROM products
ORDER BY unit_price;
``` 

* Присвоение значения по разнице цены с последующей строкой и использовании **OFFSET** (пропуск N строк):

```
SELECT product_name, unit_price, 
	LEAD(unit_price, 3) OVER(ORDER BY unit_price) - unit_price AS price_lag
FROM products
ORDER BY unit_price;
``` 

---

### Введение в транзакции

* Логическая группа операций.

* Транзакция может быть выполнена **только целиком**.

* Транзакция заканчивается на **COMMIT**.

* Обязательно смотреть на [**Stepik**](https://stepik.org/lesson/530553/?unit=523369).


* Классический пример - **банковская транзакция**:
    * прочесть баланс на счету X
    * уменьшить баланс на Z денежных средств
    * сохранить новый баланс счета X
    * прочесть баланс на счету Y
    * увеличить баланс на Z денежных средств
    * сохранить новый баланс счета Y

**Набор требований к транзакционной системе** (**ACID**):

* **Atomicity** (атомарность) - всё или ничего. В случае неполного завершения транзакции необходим откат **ROLLBACK**.

* **Consistency** (согласованность) - система не может провести несогласованные операции. Одновременно гореть зелёный и
  красный сигнал светофора не могут.

* **Isolation** (изолированность) - параллельные транзакции ждут пока завершится нынешняя. Когда списали с одного счета,
  но ещё не зачислили на другой, работа с ними извне запрещена.

* **Durability** (долговечность) - если транзакция уже выполнилась, то никакие сбои не вызовут отката действий.


* **TCL** - Transaction Control Language

**SQL синтаксис**:

```
BEGIN [TRANSACTION];
-logic
COMMIT; 
```

**PL/pgSQL синтаксис**:

```
START TRANSACTION;
-logic
END [TRANSACTION];
```

* Все операции обёрнуты в транзакции в любом случае.


* Если по ходу транзакции что-то пошло не так, её можно полностью откатить с помощью **ROLLBACK**:
    * `ROLLBACK;`

* Внутри транзакции можно делать 'засечки' в важных местах с помощью **SAVEPOINT**:
    * `SAVEPOINT savepoint_name`

* Если по ходу транзакции что-то пошло не так, её можно откатить к точке с помощью **ROLLBACK TO**:
    * `ROLLBACK TO savepoint_name`

**Транзакции и функции**:

* Нельзя создавать транзакции в функциях

* Хотя функции неявно исполняются в рамках транзакции

* Чтобы прервать транзакцию изнутри функции - **RAISE EXCEPTION**.

* Если хотим откатить только часть - можно "имитировать" **SAVEPOINT** с помощью **BEGIN** и **EXCEPTION WHEN**.

* Концепция подразумевает, что уровнем изоляции и откатами управляет внешний код (SQL-скрипт или код приложения верхнего
  уровня)

---

### Изоляция транзакций

* Данные обрабатываемые одной транзакцией изолируются от других на некоторое время, пока первая не завершится.

**Проблемы параллельности**:

* **Грязное чтение** - чтение частичных (uncommitted) изменений.

* **Неповторяемое чтение** - повторное чтение показывает, что данные были изменены после первого чтения.

* **Фантомное чтение** - повторное чтение показывает другой результирующий набор.

* **Аномалия сериализации** - результат параллельно выполняемых транзакций может не согласовываться с результатом этих
  же транзакций, выполняемых по очереди.

**[Уровни изоляции](https://postgrespro.ru/docs/postgrespro/9.5/transaction-iso#xact-read-committed)**:

* **READ COMMITTED** - уровень изоляции гарантирует, что транзакция видит только те изменения, которые уже были
  зафиксированы (**COMMIT**) другими транзакциями. Стоит по умолчанию.

* **REPEATABLE READ** - видны только те данные, которые были зафиксированы до начала транзакции, но не видны
  незафиксированные данные и изменения, произведённые другими транзакциями в процессе выполнения данной транзакции.

* **SERIALIZABLE** - наивысший уровень изоляции. Транзакции в этом режиме полностью изолированы друг от друга, что
  исключает фантомные чтения и неподтвержденные чтения.

Не исключают само возникновение конфликтов, а просто ловят их, генерируют ошибку и откатывают транзакцию, которая
наткнулась на конфликтные изменения.

**Синтаксис**:

* В начале транзакции:

```
{BEGIN|START TRANSACTION} ISOLATION LEVEL level;
```

* Внутри транзакции:

```
SET TRANSACTION ISOLATION LEVEL level;
```

---

### Транзакции на практике

* Элементарная транзакция:

```
BEGIN;

WITH prod_updates AS (
	UPDATE products
	SET discontinued = 1
	WHERE units_in_stock < 10
	RETURNING product_id
)
SELECT * INTO last_orders_on_discountinued
FROM order_details
WHERE product_id IN (SELECT product_id FROM prod_updates);

COMMIT; 

SELECT * FROM last_orders_on_discountinued;
```

* Пример прерывания транзакции:

```
BEGIN;

WITH prod_updates AS (
	UPDATE products
	SET discontinued = 1
	WHERE units_in_stock < 10
	RETURNING product_id
)
SELECT * INTO last_orders_on_discountinued
FROM order_details
WHERE product_id IN (SELECT product_id FROM prod_updates);

DROP TABLE zaza; - это прерывает транзакцию, тк возникает ошибка

COMMIT; - есди выделить и вызвать, то в случае прерывания транзакции произойдёт ROLLBACK.
```

* Пример с **SAVEPOINT** и заданием уровня изоляции:

```
START TRANSACTION ISOLATION LEVEL SERIALIZABLE;

DROP TABLE IF EXISTS last_orders_on_discountinued;

WITH prod_updates AS (
	UPDATE products
	SET discontinued = 1
	WHERE units_in_stock < 10
	RETURNING product_id
)
SELECT * INTO last_orders_on_discountinued
FROM order_details
WHERE product_id IN (SELECT product_id FROM prod_updates);

SAVEPOINT backup;

DELETE FROM order_details - этот блок был пропущен из-за ROLLBACK
WHERE product_id IN (SELECT product_id FROM last_orders_on_discountinued);

ROLLBACK TO backup;

UPDATE order_details - а этот блок выполнился
SET quantity = 0 
WHERE product_id IN (SELECT product_id FROM last_orders_on_discountinued);

END TRANSACTION;
```

---

### Триггеры

* Объекты, которые назначают действия на какие-нибудь события.


* Триггеры могут реагировать как на построчное изменение (множественное срабатывание), так и единожды на все изменения
  сразу.

* Сценарии использования триггеров:
    * Аудит таблиц - проверка данных
    * Дополнительные действия в ответ на изменения

**Синтаксис**:

* Создание построчного триггера:

```
CREATE TRIGGER trigger_name {BEFORE|AFTER} {INSERT|UPDATE|DELETE} ON table_name
FOR EACH ROW EXECUTE PROCEDURE function_name();
```

Условие может включать в себя ещё, например, **OR**:
`BEFORE INSERT OR UPDATE`

* Создание триггера на утверждения (по всей операции):

```
CREATE TRIGGER trigger_name {BEFORE|AFTER} {INSERT|UPDATE|DELETE} ON table_name
REFERENCING {NEW|OLD} TABLE AS ref_table_name - референсную таблицу необходимо задекларировать
FOR EACH STATEMENT EXECUTE PROCEDURE function_name();
```

* Удаление триггера:

```
DROP TRIGGER [IF EXISTS] trigger_name;
```

* Переименование триггера:

```
ALTER TRIGGER trigger_name ON table_name
RENAME TO new_trigger_name;
```

* Отключение триггера:

```
ALTER TABLE table_name
DISABLE TRIGGER trigger_name;
```

* Отключение всех триггеров на таблице:

```
ALTER TABLE table_name
DISABLE TRIGGER ALL;
```

**Функции, привязанные к триггеру**:

* Возвращает либо **NULL**, либо запись, соответствующую структуре таблице, на которую будет вешаться триггер.

* Через аргумент **NEW** есть доступ к вставленным и модифицированным строкам (**INSERT**/**UPDATE** триггеры).

* Через аргумент **OLD** есть доступ к вставленным и удаленным строкам (**UPDATE**/**DELETE** триггеры).


* Создание такой функции:

```
CREATE [OR REPLACE] func_name() RETURNS trigger AS $$
BEGIN
--logic
END;
$$ LANGUAGE plpgsql;
```

В функции доступна переменная **TG_OP**, хранящая тип операции (**INSERT**, **UPDATE**, **DELETE**).

**Возврат из триггеров**:

* Если **BEFORE-триггер** возвращает **NULL**, то сама операция и **AFTER-триггеры** будут отменены.


* **BEFORE-триггер** может изменить строку (**INSERT**, **UPDATE**) через **NEW** и тогда операция и **AFTER-триггеры**
  будут работать с измененной строкой.


* Если **BEFORE-триггер** "не хочет" изменять строку, то надо просто вернуть **NEW**.


* В случае **BEFORE-триггера** реагирующего на **DELETE**, возврат не имеет значения (кроме **NULL**: отменяет
  **DELETE**).


* **NEW** = **null** при **DELETE**, так что если **BEFORE-триггер** хочет дать ход **DELETE**, надо вернуть **OLD**.


* Возвращаемое значение из построчного **AFTER-триггера** (или и из **BEFORE**, и из **AFTER** триггеров на утверждения)
  игнорируется => можно возвращать **NULL**.


* Если построчный **AFTER-триггер** или триггер на утверждение хочет отменить операцию => **RAISE EXCEPTION**.

**Примеры построчных триггеров**:

```
ALTER TABLE customers
ADD COLUMN last_updated timestamp;

CREATE OR REPLACE FUNCTION track_changes_on_customers() RETURNS trigger AS $$
BEGIN
	NEW.last_updated = now();
	RETURN NEW;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS customers_timestamp ON customers;
CREATE TRIGGER customers_timestamp BEFORE INSERT OR UPDATE ON customers
FOR EACH ROW EXECUTE PROCEDURE track_changes_on_customers();
```

```
ALTER TABLE employees
ADD COLUMN user_changed text;

CREATE OR REPLACE FUNCTION track_changes_on_employees() RETURNS trigger AS $$
BEGIN
	NEW.user_changed = session_user;
	RETURN NEW;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS employee_user_change ON employees;
CREATE TRIGGER employee_user_change BEFORE INSERT OR UPDATE ON employees
FOR EACH ROW EXECUTE PROCEDURE track_changes_on_employees();
```

**Примеры триггеров на утверждения**:

```
DROP TABLE IF EXISTS products_audit;

CREATE TABLE products_audit
(	
	op char(1) NOT NULL,
	user_changed text NOT NULL,
	time_stamp timestamp NOT NULL,
	
    product_id smallint NOT NULL,
    product_name varchar(40) NOT NULL,
    supplier_id smallint,
    categoty_id smallint,
    quantuty_perf_unit varchar(20),
    unit_price real,
    units_in_stock smallint,
    units_on_order smallint,
    reorder_level smallint,
    discontinued integer NOT NULL
);

CREATE OR REPLACE FUNCTION build_audit_products() RETURNS trigger AS $$
BEGIN
	IF TG_OP = 'INSERT' THEN
		INSERT INTO products_audit
		SELECT 'I', session_user, now(), * 
		FROM new_table;
	ELSEIF TG_OP = 'UPDATE' THEN
		INSERT INTO products_audit
		SELECT 'U', session_user, now(), * 
		FROM new_table;
	ELSEIF TG_OP = 'DELETE' THEN
		INSERT INTO products_audit
		SELECT 'D', session_user, now(), * 
		FROM old_table;
	END IF;
	RETURN NULL;
END
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS audit_products_insert ON products;

CREATE TRIGGER audit_products_insert AFTER INSERT ON products
REFERENCING NEW TABLE AS new_table
FOR EACH STATEMENT EXECUTE PROCEDURE build_audit_products();

DROP TRIGGER IF EXISTS audit_products_update ON products;

CREATE TRIGGER audit_products_update AFTER UPDATE ON products
REFERENCING NEW TABLE AS new_table
FOR EACH STATEMENT EXECUTE PROCEDURE build_audit_products();

DROP TRIGGER IF EXISTS audit_products_delete ON products;

CREATE TRIGGER audit_products_delete AFTER DELETE ON products
REFERENCING OLD TABLE AS old_table
FOR EACH STATEMENT EXECUTE PROCEDURE build_audit_products();
```

---

### Безопасность

* **Роль** (группа) - совокупность разрешений и запретов на доступ к БД и её объектам. Создаются на уровне экземпляра
  сервера.

* В **PostgreSQL** пользователь - роль с паролем => на роль с паролем назначают роль с доступами.

* **postgres** - роль, создаваемая по умолчанию, и единственная имеющая привилегии **SUPERUSER**.

* Обязательно смотреть на [**Stepik**](https://stepik.org/lesson/530605/step/1?unit=523421).

**Уровни безопасности**:

1. **Экземпляра** - аутентификация, создание БД, управление безопасностью, ...

2. **Базы данных** - подключение к БД, создание в ней ролей, ...

3. **Схемы** - управление схемами (создание, удаление).

4. **Таблицы** - CRUD-операции (**CREATE** **READ** **UPDATE** **DELETE**) над таблицами.

5. **Колонки** - операции над конкретной колонкой конкретной таблицы.

6. **Строки** - операции над строками.

**Создание роли и серверные привилегии**:

* Вывод всех ролей на инстанции сервере:

```
SELECT role_name
FROM pg_roles;
```

* Создание роли:

```
CREATE ROLE role_name [[NO]{LOGIN|SUPERUSER|CREATEDB|CREATEROLE|REPLICATION}];
```

По умолчанию у всех привилегий стоит **NO** и роль является бесправной.

* Создание пользователя:

```
CREATE USER user_name; - без пароля
```

```
CREATE USER user_name WITH PASSWORD *****; - с паролем
```

* Доступ к таблице:

```
GRANT {SELECT|INSERT|UPDATE|DELETE|TRUNCATE|REFERENCES|TRIGGER} ON table_name TO role; - к конкретной таблице
```

```
GRANT {SELECT|INSERT|UPDATE|DELETE|TRUNCATE|REFERENCES|TRIGGER} ON ALL TABLES IN SCHEMA schema_name TO role; - ко всем таблицам схемы
```

* Доступ к колонкам:

```
GRANT {SELECT|INSERT|UPDATE|REFERENCES} (columns) ON table_name TO role;
```

* Удаление роли:

```
DROP ROLE [IF EXISTS] role_name;
```

---