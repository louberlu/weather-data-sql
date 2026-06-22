CREATE TABLE locations (
    location_id SERIAL NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country_code VARCHAR(2) NOT NULL,
    timezone INT NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    CONSTRAINT pk_location 
        PRIMARY KEY (location_id)
);

CREATE TABLE weathers (
    weather_id SERIAL NOT NULL,
    main VARCHAR(20) NOT NULL,
    description VARCHAR2 NOT NULL,
    temp FLOAT NOT NULL,
    feels_like FLOAT NOT NULL,
    temp_min FLOAT NOT NULL,
    temp_max FLOAT NOT NULL,
    pressure FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    visibility FLOAT NOT NULL,
    wind_speed FLOAT NOT NULL,
    clouds FLOAT NOT NULL,
    rain FLOAT,
    snow FLOAT,
    observation_time TIMESTAMP NOT NULL,
    sunrise TIMESTAMP NOT NULL,
    sunset TIMESTAMP NOT NULL,
    location_id INT NOT NULL,
    CONSTRAINT fk_location
        FOREIGN KEY (location_id) 
        REFERENCES location(location_id),
    CONSTRAINT pk_weather 
        PRIMARY KEY (weather_id)
)