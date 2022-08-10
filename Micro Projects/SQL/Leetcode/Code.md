[185. Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries/)
```
with tb1 as (
select
d.name,
salary,
dense_rank() over(partition by d.name order by salary desc) as rnk
from employee e
join department d
on e.departmentid = d.id
),

tb2 as (
select
name as department,
salary
from tb1
where rnk <= 3)

select
d.name as Department,
e.name as Employee,
e.salary as Salary
from employee e
join department d
on e.departmentid = d.id
where (d.name,e.salary) in (select * from tb2)
```
[262. Trips and Users](https://leetcode.com/problems/trips-and-users/)
```
with tb1 as (
select
t.client_id,
t.driver_id,
t.status,
t.request_at
from trips t
join (select users_id from users where role = 'client' and banned = 'No') tb
on t.client_id = tb.users_id
join (select users_id from users where role = 'driver' and banned = 'No') tbb
on t.driver_id = tbb.users_id
)


select
request_at as Day,
round(sum(case when left(status,3) = 'can' then 1 else 0 end)/count(status),2) as 'Cancellation Rate'
from tb1
where request_at between '2013-10-01' and '2013-10-03'
group by request_at
```
[262. 1384. Total Sales Amount by Year](https://leetcode.com/problems/total-sales-amount-by-year/)
```
with recursive tb1 as (
select min(period_start) as dt
from sales
union 
select date_add(dt,interval 1 day) as dt
from tb1
where date_add(dt,interval 1 day) <= (select max(period_end) from sales)
)

select 
s.product_id, 
p.product_name,
left(tb1.dt,4) as report_year,
average_daily_sales * count(tb1.dt) as total_amount
from sales s
join product p 
on s.product_id = p.product_id
join tb1 
on tb1.dt between s.period_start and s.period_end
group by 1,2,3
order by 1,2
```
[2004. The Number of Seniors and Juniors to Join the Company](https://leetcode.com/problems/the-number-of-seniors-and-juniors-to-join-the-company/)
```
with tb1 as (
select
employee_id,
experience,
salary,
sum(salary) over(partition by experience order by salary,employee_id asc) as cum_sum
from candidates
)

select
'Senior' as experience,
count(employee_id) as accepted_candidates
from tb1
where experience = 'senior' and cum_sum <= 70000


union

select
'Junior' as experience,
count(employee_id) as accepted_candidates
from tb1
where experience = 'junior' and cum_sum <= (select 70000 - ifnull(max(cum_sum),0) from tb1 where experience = 'senior' and cum_sum <= 70000)
```
[1194. Tournament Winners](https://leetcode.com/problems/tournament-winners/)
```
with tb1 as (
select 
first_player as player, first_score as score
from matches
union all
select 
second_player as player, second_score as score
from matches
),

tb2 as (
select
player, sum(score) as score
from tb1
group by player
),

tb3 as (
select
group_id,
player_id,
row_number() over(partition by group_id order by score desc, player_id asc) as rnk
from players p
join tb2
on p.player_id = tb2.player)

select
group_id, player_id
from tb3
where rnk = 1
```
[2173. Longest Winning Streak](https://leetcode.com/problems/longest-winning-streak/)
```
with tb1 as (
select
player_id, match_day,result,
row_number() over(partition by player_id order by match_day) as rnk
from matches
),

tb2 as (
select
player_id,
rnk - row_number() over(partition by player_id order by match_day) as group_id
from tb1
where result = 'win')

select
tb3.player_id, ifnull(max(tb4.cnt),0) as longest_streak
from (select distinct player_id from matches) tb3
left join (select player_id, group_id, count(*) as cnt from tb2 group by 1,2) tb4
on tb3.player_id = tb4.player_id
group by tb3.player_id
```
[569. Median Employee Salary](https://leetcode.com/problems/median-employee-salary/)
```
with tb1 as (
select
id,company,salary,
row_number() over(partition by company order by salary desc, id desc) as rnkd,
row_number() over(partition by company order by salary asc, id asc) as rnka
from employee )

select
id,company,salary
from tb1
where rnka between rnkd - 1 and rnkd + 1
```
[601. Human Traffic of Stadium](https://leetcode.com/problems/human-traffic-of-stadium/)
```
with tb1 as (
select
id, visit_date, people
from stadium
where people >= 100
),

tb2 as (
select
id,
visit_date,
people,
row_number() over(order by id) as rnk
from tb1
),

tb3 as (
select
id,
visit_date,
people,
id - rnk as diff
from tb2
)

select
id,
visit_date,
people
from tb3
where diff in
(select
diff
from tb3
group by diff
having count(diff) >= 3)
```
[615. Average Salary: Departments VS Company](https://leetcode.com/problems/average-salary-departments-vs-company/)
```
with group_table as (
select
id, s.employee_id, department_id, amount, left(pay_date,7) as month
from salary s
join employee e
on s.employee_id = e.employee_id),

month_avg as (
select
month, avg(amount) as amt
from group_table
group by month),

month_dep as (
select
month, department_id, avg(amount) as amt
from group_table
group by month, department_id)

select 
md.month as pay_month, md.department_id, 
case 
when md.amt > ma.amt then 'higher'
when md.amt < ma.amt then 'lower'
else 'same' end as comparison
from month_dep md
left join month_avg ma
on md.month = ma.month
```
[571. Find Median Given Frequency of Numbers](https://leetcode.com/problems/find-median-given-frequency-of-numbers/)
```
select  avg(n.num) median
from Numbers n
where n.Frequency >= abs((select sum(Frequency) from Numbers where num<=n.num) -
                         (select sum(Frequency) from Numbers where num>=n.num))
```
[579. Find Cumulative Salary of an Employee](https://leetcode.com/problems/find-cumulative-salary-of-an-employee/)
```
with tb1 as (
select
id, month, salary
from employee
where (id,month) not in (
select
id, max(month)
from employee
group by id))

select
a.id, a.month, sum(b.salary) as salary
from tb1 a
left join tb1 b
on a.month - b.month between 0 and 2 and a.id = b.id
group by a.id, a.month
order by id, month desc
```
[618. Students Report By Geography](https://leetcode.com/problems/students-report-by-geography/)
```
with tb1 as (
select
name, continent, row_number() over(partition by continent order by name) as rnk
from student
)

select
max(case when continent = 'America' then name end) as 'America',
max(case when continent = 'Asia' then name end) as 'Asia',
max(case when continent = 'Europe' then name end) as 'Europe'
from tb1
group by rnk
```
[1097. Game Play Analysis V](https://leetcode.com/problems/game-play-analysis-v/)
```
with tb1 as (
select
player_id,
min(event_date) as dt
from activity
group by player_id)

select
tb1.dt as install_dt, count(distinct tb1.player_id) as installs, round(count(distinct a.player_id)/count(distinct tb1.player_id),2) as Day1_retention
from tb1
left join activity a
on tb1.dt = a.event_date - 1 and tb1.player_id = a.player_id
group by tb1.dt
```
[1127. User Purchase Platform](https://leetcode.com/problems/user-purchase-platform/)
```
with tb1 as (
select
*
from
(select
distinct spend_date
from spending) tba
cross join
(select "mobile" as platform
union 
select "desktop" as platform
union 
select "both" as platform
) tbb
),

tb5 as (
select
spend_date,
user_id,
case when count(*) over(partition by spend_date, user_id) = 1 then platform
else 'both' end as "platform",
amount
from spending
)

select
tb1.spend_date, tb1.platform, ifnull(tb2.amount,0) as total_amount, ifnull(total_users,0) as total_users
from tb1
left join 
(select
spend_date, platform, sum(amount) as amount, count(distinct user_id) as total_users
from tb5
group by spend_date, platform) tb2
on tb1.spend_date = tb2.spend_date AND tb1.platform = tb2.platform
# group by tb1.spend_date, tb1.platform
```

















