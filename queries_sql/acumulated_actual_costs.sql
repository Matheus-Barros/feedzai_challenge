-- Build a model using SQL to calculate “actual costs”. This indicator calculates the total accumulated cost of a 
-- project at a given day by summing up all worked hours up until that day. Consider a flat rate of 100$ for the 
-- cost of each work hour.
SELECT
    project_id,
    date,
    SUM((worked/1000.0)*100.0) OVER (PARTITION BY project_id ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total_accumulated_cost
FROM
    work_hours;