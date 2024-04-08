# Тест SQL

На основе таблиц базы данных, напишите SQL код, который возвращает необходимые результаты
Пример: 

Общее количество товаров
```sql
select count (*) from items
```

## Структура данных

Используемый синтаксис: Oracle SQL или другой

| Сustomer       | Description           |
| -------------- | --------------------- |
| customer\_id   | customer unique id    |
| customer\_name | customer name         |
| country\_code  | country code ISO 3166 |

| Items             | Description       |
| ----------------- | ----------------- |
| item\_id          | item unique id    |
| item\_name        | item name         |
| item\_description | item description  |
| item\_price       | item price in USD |

| Orders       | Description                 |
| ------------ | --------------------------- |
| date\_time   | date and time of the orders |
| item\_id     | item unique id              |
| customer\_id | user unique id              |
| quantity     | number of items in order    |

| Countries     | Description           |
| ------------- | --------------------- |
| country\_code | country code          |
| country\_name | country name          |
| country\_zone | AMER, APJ, LATAM etc. |


| Сonnection\_log         | Description                           |
| ----------------------- | ------------------------------------- |
| customer\_id            | customer unique id                    |
| first\_connection\_time | date and time of the first connection |
| last\_connection\_time  | date and time of the last connection  |

## Задания

### 1) Количество покупателей из Италии и Франции

| **Country_name** | **CustomerCountDistinct** |
| ------------------------- | ----------------------------- |
| France                    | #                             |
| Italy                     | #                             |

```sql
SELECT country_name, COUNT(DISTINCT customer_id) AS CustomerCountDistinct
FROM Customers
WHERE country_code IN ('IT', 'FR')
GROUP BY country_name;
```

### 2) ТОП 10 покупателей по расходам

| **Customer_name** | **Revenue** |
| ---------------------- | ----------- |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |
| #                      | #           |

```sql
SELECT customer_name, SUM(item_price * quantity) AS Revenue
FROM Orders
JOIN Items ON Orders.item_id = Items.item_id
JOIN Customers ON Orders.customer_id = Customers.customer_id
GROUP BY customer_id, customer_name
ORDER BY Revenue DESC
LIMIT 10;
```

### 3) Общая выручка USD по странам, если нет дохода, вернуть NULL

| **Country_name** | **RevenuePerCountry** |
| ------------------------- | --------------------- |
| Italy                     | #                     |
| France                    | NULL                  |
| Mexico                    | #                     |
| Germany                   | #                     |
| Tanzania                  | #                     |

```sql
SELECT country_name,
       CASE
           WHEN SUM(item_price * quantity) IS NULL THEN NULL
           ELSE SUM(item_price * quantity)
       END AS RevenuePerCountry
FROM Orders
JOIN Items ON Orders.item_id = Items.item_id
JOIN Customers ON Orders.customer_id = Customers.customer_id
JOIN Countries ON Customers.country_code = Countries.country_code
GROUP BY country_name;
```

### 4) Самый дорогой товар, купленный одним покупателем

| **Customer\_id** | **Customer\_name** | **MostExpensiveItemName** |
| ---------------- | ------------------ | ------------------------- |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |
| #                | #                  | #                         |

```sql
SELECT customer_id, customer_name, item_name AS MostExpensiveItemName
FROM Orders
JOIN Items ON Orders.item_id = Items.item_id
JOIN Customers ON Orders.customer_id = Customers.customer_id
WHERE (customer_id, item_price) IN (
    SELECT customer_id, MAX(item_price)
    FROM Orders
    JOIN Items ON Orders.item_id = Items.item_id
    JOIN Customers ON Orders.customer_id = Customers.customer_id
    GROUP BY customer_id
);
```

### 5) Ежемесячный доход

| **Month (MM format)** | **Total Revenue** |
| --------------------- | ----------------- |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |

```sql
SELECT TO_CHAR(date_time, 'MM') AS Month, SUM(item_price * quantity) AS TotalRevenue
FROM Orders
JOIN Items ON Orders.item_id = Items.item_id
GROUP BY TO_CHAR(date_time, 'MM')
ORDER BY TO_CHAR(date_time, 'MM');
```

### 6) Найти дубликаты

Во время передачи данных произошел сбой, в таблице orders появилось несколько 
дубликатов (несколько результатов возвращаются для date_time + customer_id + item_id). 
Вы должны их найти и вернуть количество дубликатов.

```sql
SELECT COUNT(*) - COUNT(DISTINCT date_time, customer_id, item_id) AS DuplicateCount
FROM Orders;
```

### 7) Найти "важных" покупателей

Создать запрос, который найдет всех "важных" покупателей,
т.е. тех, кто совершил наибольшее количество покупок после своего первого заказа.

| **Customer\_id** | **Total Orders Count** |
| --------------------- |-------------------------------|
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |
| #                     | #                             |

```sql
SELECT customer_id, COUNT(*) AS TotalOrdersCount
FROM (
    SELECT customer_id, MIN(date_time) AS first_order_date
    FROM Orders
    GROUP BY customer_id
) subquery
JOIN Orders ON subquery.customer_id = Orders.customer_id AND Orders.date_time > subquery.first_order_date
GROUP BY customer_id
ORDER BY TotalOrdersCount DESC;
```

### 8) Найти покупателей с "ростом" за последний месяц

Написать запрос, который найдет всех клиентов,
у которых суммарная выручка за последний месяц
превышает среднюю выручку за все месяцы.

| **Customer\_id** | **Total Revenue** |
| --------------------- |-------------------|
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |
| #                     | #                 |

```sql
SELECT customer_id, SUM(item_price * quantity) AS TotalRevenue
FROM Orders
JOIN Items ON Orders.item_id = Items.item_id
WHERE date_time >= ADD_MONTHS(TRUNC(SYSDATE, 'MM'), -1)
GROUP BY customer_id
HAVING SUM(item_price * quantity) > (
    SELECT AVG(SUM(item_price * quantity))
    FROM Orders
    JOIN Items ON Orders.item_id = Items.item_id
    WHERE date_time < ADD_MONTHS(TRUNC(SYSDATE, 'MM'), -1)
    GROUP BY customer_id
);
```
