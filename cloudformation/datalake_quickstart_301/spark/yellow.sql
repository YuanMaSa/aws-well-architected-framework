select *,
cast(date_format(tpep_pickup_datetime,'Y') AS INT) AS year,
cast(date_format(tpep_pickup_datetime,'M') AS INT) AS month,
cast(date_format(tpep_pickup_datetime,'d') AS INT) AS day,
cast(hour(tpep_pickup_datetime) AS INT) AS hour,
case when dayofweek(tpep_pickup_datetime) in (1,7) then 'Weekend' else 'Weekday' end AS day_type,
cast(date_format(tpep_pickup_datetime,'w') AS INT) AS week_number,
replace(date_format(tpep_pickup_datetime, 'E'),'day','') AS weekday
from yellow
