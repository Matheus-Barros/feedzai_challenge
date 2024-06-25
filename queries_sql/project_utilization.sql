-- Build a model using SQL to calculate “project utilization”. This indicator calculates the percentage of total 
-- available hours each employee is allocated to a project, per month, assuming 8h/day of work time for each employee
-- except on weekends and time off.

with max_min as (
    SELECT date from work_hours UNION SELECT date_start FROM time_off UNION SELECT date_end FROM time_off
),
all_working_days as (
    with RECURSIVE DateRange AS (
        SELECT min(date) AS Date FROM max_min
        UNION ALL
        SELECT DATE(Date, '+1 day') FROM DateRange WHERE Date < (select max(date) from max_min)
    )
    SELECT Date
    FROM DateRange
    WHERE strftime('%w', Date) NOT IN ('0', '6')
),
available_work_hours_per_user as (
    SELECT
        t.employee_id,
        t.employee_name,
        --t.date_start,
        --t.date_end,
        STRFTIME('%Y-%m', d.Date) as work_month,
        count(d.Date)*8 as hours
    FROM time_off t
    CROSS JOIN all_working_days d
    WHERE d.Date < t.date_start OR d.Date > t.date_end
    group by employee_id, employee_name, work_month
),
worked_hours_by_month_by_project_by_employee as (
    SELECT
        wh.employee_id,
        STRFTIME('%Y-%m', wh.date) as work_month,
        wh.project_id,
        sum(wh.worked)/1000.0 as worked_total
    FROM work_hours wh
    GROUP BY employee_id, work_month, project_id
)
SELECT 
    ah.employee_name,
    ah.work_month,
    wh.project_id,
    100.0*wh.worked_total/ah.hours as project_utilization_percent
FROM worked_hours_by_month_by_project_by_employee wh
JOIN available_work_hours_per_user ah ON ah.employee_id = wh.employee_id AND ah.work_month = wh.work_month
