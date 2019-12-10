SELECT
    gyw_col.humidity,
    sum(gy_col.green_taxi_pickups) as green_pickup_sum
FROM (
    SELECT
        g_col.*,
        y_col.yellow_taxi_pickups
    FROM (
        SELECT
            date_trunc('hour', lpep_pickup_datetime) AS date,
            Count(*) AS green_taxi_pickups
        FROM
            dna_team_db.green
        GROUP BY
            1) AS g_col
        JOIN (
            SELECT
                date_trunc('hour', tpep_pickup_datetime) AS date,
                Count(*) AS yellow_taxi_pickups
            FROM
                dna_team_db.yellow
            GROUP BY
                1) AS y_col ON g_col.date = y_col.date) AS gy_col
        JOIN (
            SELECT
                date_parse (dt,
                    '%Y/%m/%d %H:%i') as datetime,
                new_york AS humidity
            FROM
                dna_team_db.weather) AS gyw_col ON gy_col.date = gyw_col.datetime
        group by
            gyw_col.humidity
        order by
            green_pickup_sum DESC
        limit 10
