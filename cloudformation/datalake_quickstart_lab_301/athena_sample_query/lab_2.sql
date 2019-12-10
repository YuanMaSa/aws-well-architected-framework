SELECT
    weekday,
    yellow_pickups,
    yellow_distance as yellow_total_miles,
    AVG(humidity) as humidity_avg
FROM (
    SELECT
        g_col.*,
        y_col.yellow_distance,
        y_col.yellow_pickups
    FROM (
        SELECT
            weekday,
            sum(cast(trip_distance as BIGINT)) AS green_distance,
            count(*) as green_pickups
        FROM
            dna_team_db.green
        GROUP BY
            weekday) AS g_col
        JOIN (
            SELECT
                weekday,
                sum(cast(trip_distance as BIGINT)) AS yellow_distance,
                count(*) as yellow_pickups
            FROM
                dna_team_db.yellow
            GROUP BY
                weekday) AS y_col ON g_col.weekday = y_col.weekday) AS gy_col
        JOIN (
            SELECT
                case day_of_week (date_parse (dt,
                        '%Y/%m/%d %H:%i'))
                when 1 then
                    'Mon'
                    when 2 then
                    'Tue'
                    when 3 then
                    'Wed'
                    when 4 then
                    'Thu'
                    when 5 then
                    'Fri'
                    when 6 then
                    'Sat'
                    when 7 then
                    'Sun'
                end as weekday_type,
                new_york AS humidity
            FROM
                dna_team_db.weather) AS gyw_col ON gy_col.weekday = gyw_col.weekday_type
        group by
            weekday,
            yellow_distance,
            yellow_pickups
        order by
            yellow_pickups DESC
