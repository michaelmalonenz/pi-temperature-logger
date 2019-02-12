CREATE TABLE temperatures (
    temperature float8 NOT NULL,
    pressure float8 NOT NULL,
    humidity float8 NOT NULL,
    "timestamp" timestamp with time zone NOT NULL
);

CREATE TABLE lux (
    infrared float8 NOT NULL,
    visible float8 NOT NULL,
    "timestamp" timestamp with time zone NOT NULL
);

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'temperature') THEN
        CREATE ROLE temperature WITH
        LOGIN
        NOSUPERUSER
        NOINHERIT
        NOCREATEDB
        NOCREATEROLE
        NOREPLICATION
        PASSWORD 'temperature';
        COMMENT ON ROLE temperature IS 'Service user for updating the usage events';
    END IF;
END
$$;

GRANT INSERT ON TABLE temperatures TO temperature;
GRANT INSERT ON TABLE lux TO temperature;
