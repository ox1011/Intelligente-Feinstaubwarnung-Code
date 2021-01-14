CREATE TABLE sensor(
  id INT,
  name VARCHAR(200),
  manufacturer VARCHAR(200), 
  PRIMARY KEY(id)
);

CREATE TABLE location(
  id INT,
  sensor_id INT,
  altitude NUMERIC,
  latitude NUMERIC,
  longitude NUMERIC,
  indoor BOOL,
  country VARCHAR(2),
  PRIMARY KEY(id),
  CONSTRAINT fk_sensor FOREIGN KEY (sensor_id) REFERENCES sensor(id)
);

CREATE TABLE sensordatavalues(
 id BIGINT,
 sensor_id INT, 
 value NUMERIC,
 value_type VARCHAR(200),
 date DATE,
 time TIME,
 PRIMARY KEY(id, sensor_id, value, value_type, date, time),
 CONSTRAINT fk_sensor FOREIGN KEY (sensor_id) REFERENCES sensor(id)
);

CREATE OR REPLACE FUNCTION _final_median(numeric[])
   RETURNS numeric AS
$$
   SELECT AVG(val)
   FROM (
     SELECT val
     FROM unnest($1) val
     ORDER BY 1
     LIMIT  2 - MOD(array_upper($1, 1), 2)
     OFFSET CEIL(array_upper($1, 1) / 2.0) - 1
   ) sub;
$$
LANGUAGE 'sql' IMMUTABLE;

CREATE AGGREGATE median(numeric) (
  SFUNC=array_append,
  STYPE=numeric[],
  FINALFUNC=_final_median,
  INITCOND='{}'
);