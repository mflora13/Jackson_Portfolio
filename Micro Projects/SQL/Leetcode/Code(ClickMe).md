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
[1159. Market Analysis II](https://leetcode.com/problems/market-analysis-ii/)
```
with tb1 as (
select
seller_id,
item_id,
row_number() over(partition by seller_id order by order_date) as rnk
from orders
),

tb2 as (
select
seller_id,
item_id
from tb1
where rnk = 2)

select
u.user_id as seller_id,
case when u.favorite_brand = i.item_brand then 'yes' else 'no' end as "2nd_item_fav_brand"
from users u
left join tb2
on u.user_id = tb2.seller_id
left join items i
on tb2.item_id = i.item_id
```
[1225. Report Contiguous Dates](https://leetcode.com/problems/report-contiguous-dates/)
```
with tb1 as (
select
fail_date as dt, 'failed' as id
from failed
union
select
success_date as dt, 'succeeded' as id
from succeeded),

tb2 as (
select
dt, id,
row_number() over(partition by id order by dt) as r,
row_number() over(order by dt) as r2
from tb1 
where year(dt) = 2019)

select
id as period_state, min(dt) as start_date, max(dt) as end_date
from tb2
group by r2-r, id
order by start_date
```
[1369. Get the Second Most Recent Activity](https://leetcode.com/problems/get-the-second-most-recent-activity/)
```
with tb1 as (
select 
username
from useractivity
group by username
having count(username) = 1
),

tb2 as (
select
username, max(endDate) as maxdt
from useractivity
where (username,endDate) not in 
(select
username, max(endDate) as maximum
from useractivity
where username not in (select username from tb1)
group by username)
group by username
)

select * 
from useractivity
where username in (select username from tb1)

union

select *
from useractivity
where (username,endDate) in (select username, maxdt from tb2)
```
[1412. Find the Quiet Students in All Exams](https://leetcode.com/problems/find-the-quiet-students-in-all-exams/)
```
with tb1 as (
select
student_id,
rank() over(partition by exam_id order by score desc) as max_rank,
rank() over(partition by exam_id order by score) as min_rank
from exam
)

select
student_id, student_name
from student
where student_id not in
(select
student_id
from tb1
where max_rank = 1 or min_rank = 1)
and student_id in (select distinct student_id from exam)
```
[1635. Hopper Company Queries I](https://leetcode.com/problems/hopper-company-queries-i/)
```
with recursive tb1 as (
select 1 as month
union all
select month + 1
from tb1
where month <= 11
),

tb2 as (
select
case when year(join_date) = 2019 then '1' else month(join_date) end as month
from drivers
where join_date < '2021-01-01'
),

tb3 as (
select
distinct tb1.month,
count(case when tb2.month is null then tb2.month else 0 end) over(order by tb1.month) as active_drivers
from tb1
left join tb2
on tb1.month = tb2.month
),

tb4 as (
select
month(requested_at) as month
from rides r
join AcceptedRides a
on r.ride_id = a.ride_id
where year(requested_at) = 2020)

select
tb3.month, active_drivers, ifnull(count(tb4.month),0) as accepted_rides
from tb3
left join tb4
on tb3.month = tb4.month
group by tb3.month, active_drivers
```
[1645. Hopper Company Queries II](https://leetcode.com/problems/hopper-company-queries-ii/)
```
with recursive months as (
select      1 as month
union all
select      month+1
from        months
where       month <12),

available_drivers as (
select      months.month, ifnull(max(t1.active_driver) over (order by month),0) as active_driver
from        months
left join   
(select     month(join_date) as month, count(driver_id) over (order by join_date rows unbounded preceding) as active_driver
from        drivers
where       year(join_date) <= 2020) t1
on          t1.month = months.month
),

working_drivers as (
select      month(requested_at) as month, count(distinct driver_id) as working_driver
from        Rides R
join        AcceptedRides A on R.ride_id = A.ride_id
where       year(requested_at) = 2020
group by    1)

select      months.month, ifnull(round(working_driver/active_driver*100,2),0) as working_percentage
from        months
left join   available_drivers on available_drivers.month = months.month
left join   working_drivers on working_drivers.month = months.month
group by    1
```
[1651. Hopper Company Queries III](https://leetcode.com/problems/hopper-company-queries-iii/)
```
with recursive month_rank as(
select 1 as month
union all
select month + 1
from month_rank
where month <= 11),

accepeted_rides as (
select
month(requested_at) as month,
ride_distance,
ride_duration
from rides r
join acceptedrides a
on r.ride_id = a.ride_id
where year(requested_at) = 2020),

join_month_rides as (
select 
m.month, sum(a.ride_distance) as ride_distance, sum(a.ride_duration) as ride_duration
from month_rank as m
left join accepeted_rides a
on m.month = a.month
group by m.month
)

select
month,
round(avg(ifnull(ride_distance,0)) over(order by month rows between current row and 2 following),2) as average_ride_distance,
round(avg(ifnull(ride_duration,0)) over(order by month rows between current row and 2 following),2) as average_ride_duration
from join_month_rides
order by month
limit 10
```
[1767. Find the Subtasks That Did Not Execute](https://leetcode.com/problems/find-the-subtasks-that-did-not-execute/)
```
with recursive tasks_rnk as (
select 1 as cnt
union all
select cnt + 1
from tasks_rnk
where cnt <= 19),

subtasks_join as (
select
t.task_id, t.subtasks_count, t1.cnt
from tasks t
join tasks_rnk t1
on t.subtasks_count >= t1.cnt)

select 
task_id, cnt as subtask_id
from subtasks_join
where (task_id,cnt) not in (select task_id, subtask_id from executed)
order by task_id
```
[1892. Page Recommendations II](https://leetcode.com/problems/page-recommendations-ii/)
```
with tb1 as (
select
user1_id as user_id, user2_id as friend
from friendship
union all
select
user2_id as user_id, user1_id as friend
from friendship
),

tb2 as (
select
tb1.user_id, l.page_id, count(distinct friend) as friends_likes
from tb1
join likes l
on tb1.friend = l.user_id
left join likes l2
on tb1.user_id = l2.user_id AND l.page_id = l2.page_id
where l2.page_id is null
group by tb1.user_id, l.page_id)

select * from tb2
```




