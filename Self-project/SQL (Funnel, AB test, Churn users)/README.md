# 1. What is a Funnel?
In the world of marketing analysis, “funnel” is a word you will hear time and time again.

A **funnel** is a marketing model which illustrates the theoretical customer journey towards the purchase of a product or service. Oftentimes, we want to track how many users complete a series of steps and know which steps have the most number of users giving up.

Some examples include:

- Answering each part of a 5 question survey on customer satisfaction
- Clicking “Continue” on each step of a set of 5 onboarding modals
- Browsing a selection of products → Viewing a shopping cart → Making a purchase
- Generally, we want to know the total number of users in each step of the funnel, as well as the percent of users who complete each step.

Throughout this project, we will be working with data from a fictional company called Mattresses and More. Using SQL, you can dive into complex funnels and event flow analysis to gain insights into their users’ behavior.
<br />
<br />
![abc](https://content.codecademy.com/courses/sql-intensive/funnels.svg)
<br />
<br />
# 2. Build a Funnel from Multiple Tables
Scenario: Mattresses and More sells bedding essentials from their e-commerce store. Their purchase funnel is:

1. The user browses products and adds them to their cart
2. The user proceeds to the checkout page
3. The user enters credit card information and makes a purchase
4. Three steps! Simple and easy.

As a sales analyst, you want to examine data from the shopping days before Christmas. As Christmas approaches, you suspect that customers become more likely to purchase items in their cart (i.e., they move from window shopping to buying presents).

The data for Mattresses and More is spread across several tables:

```browse``` - each row in this table represents an item that a user has added to his shopping cart
<br />
```checkout``` - each row in this table represents an item in a cart that has been checked out
<br />
```purchase``` - each row in this table represents an item that has been purchased
<br />
## 2.a. Get closer:
```SQL
SELECT *
FROM browse
LIMIT 5;
 
SELECT *
FROM checkout
LIMIT 5;
 
SELECT *
FROM purchase
LIMIT 5;
```
user_id|browse_date|item_id
--|--|--
336f9fdc-aaeb-48a1-a773-e3a935442d45|2017-12-20|3
336f9fdc-aaeb-48a1-a773-e3a935442d45|2017-12-20|22
336f9fdc-aaeb-48a1-a773-e3a935442d45|2017-12-20|25
336f9fdc-aaeb-48a1-a773-e3a935442d45|2017-12-20|24
4596bb1a-7aa9-4ac9-9896-022d871cdcde|2017-12-20|0

user_id|checkout_date|item_id
--|--|--
2fdb3958-ffc9-4b84-a49d-5f9f40e9469e|2017-12-20|26
2fdb3958-ffc9-4b84-a49d-5f9f40e9469e|2017-12-20|24
3a3e5fe6-39a7-4068-8009-3b9f649cb1aa|2017-12-20|7
3a3e5fe6-39a7-4068-8009-3b9f649cb1aa|2017-12-20|6
3a3e5fe6-39a7-4068-8009-3b9f649cb1aa|2017-12-20|12

user_id|purchase_date|item_id
--|--|--
2fdb3958-ffc9-4b84-a49d-5f9f40e9469e|2017-12-20|26
2fdb3958-ffc9-4b84-a49d-5f9f40e9469e|2017-12-20|24
3a3e5fe6-39a7-4068-8009-3b9f649cb1aa|2017-12-20|7
3a3e5fe6-39a7-4068-8009-3b9f649cb1aa|2017-12-20|6
3a3e5fe6-39a7-4068-8009-3b9f649cb1aa|2017-12-20|12

## 2.b. Overall funnels:

```SQL
WITH funnels AS (
  SELECT DISTINCT b.browse_date,
    b.user_id,
    c.user_id IS NOT NULL AS 'is_checkout',
    p.user_id IS NOT NULL AS 'is_purchase'
  FROM browse AS 'b'
  LEFT JOIN checkout AS 'c'
    ON c.user_id = b.user_id
  LEFT JOIN purchase AS 'p'
    ON p.user_id = c.user_id)
SELECT COUNT(*) AS 'num_browse',
   SUM(is_checkout) AS 'num_checkout',
   SUM(is_purchase) AS 'num_purchase',
   1.0 * SUM(is_checkout) / COUNT(user_id) AS 'browse_to_checkout',
   1.0 * SUM(is_purchase) / SUM(is_checkout) AS 'checkout_to_purchase'
FROM funnels;
```
num_browse|num_checkout|num_purchase|browse_to_checkout|checkout_to_purchase
--|--|--|--|--
775|183|163|0.236129032258065|0.890710382513661

The management team suspects that conversion from checkout to purchase changes as the browse_date gets closer to Christmas Day.

## 2.c. How conversion rates change as we get closer to Christmas
```SQL
WITH funnels AS (
  SELECT DISTINCT b.browse_date,
    b.user_id,
    c.user_id IS NOT NULL AS 'is_checkout',
    p.user_id IS NOT NULL AS 'is_purchase'
  FROM browse AS 'b'
  LEFT JOIN checkout AS 'c'
    ON c.user_id = b.user_id
  LEFT JOIN purchase AS 'p'
    ON p.user_id = c.user_id)
SELECT browse_date,COUNT(*) AS 'num_browse',
   SUM(is_checkout) AS 'num_checkout',
   SUM(is_purchase) AS 'num_purchase',
   1.0 * SUM(is_checkout) / COUNT(user_id) AS 'browse_to_checkout',
   1.0 * SUM(is_purchase) / SUM(is_checkout) AS 'checkout_to_purchase'
FROM funnels
GROUP BY browse_date
ORDER BY browse_date;
```
browse_date|num_browse|num_checkout|num_purchase|browse_to_checkout|checkout_to_purchase
--|--|--|--|--|--
2017-12-20|100|20|16|0.2|0.8
2017-12-21|150|33|28|0.22|0.848484848484849
2017-12-22|250|62|55|0.248|0.887096774193548
2017-12-23|275|68|64|0.247272727272727|0.941176470588235

Oh wow, look at the steady increase in sales (increasing ```checkout_to_purchase``` percentage) as we inch closer to Christmas Eve!
