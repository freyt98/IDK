-- Install the dblink exstension (dblink is a module that
--              supports connections to other PostgreSQL databases
--              from within a database session.)
CREATE EXTENSION IF NOT EXISTS dblink;

-- Create the postgres superuser role incase it doesn't already
--              exist (we don't create it my default, since the default
--              user was named shoc)
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE  rolname = 'postgres') THEN

      CREATE ROLE postgres WITH LOGIN SUPERUSER INHERIT CREATEDB CREATEROLE REPLICATION PASSWORD 'JustKeepSwimming!';
   END IF;
END
$do$;


-- Create the sample_data database if it doesn't exist
DO
$do$
BEGIN
   IF EXISTS (SELECT FROM pg_database WHERE datname = 'sample_data') THEN
      RAISE NOTICE 'Database already exists';  -- optional
   ELSE
      PERFORM dblink_exec('dbname=' || current_database()  -- current db
                        , 'CREATE DATABASE sample_data OWNER=''shoc''');
   END IF;
END
$do$;

SET search_path TO sample_data;
\connect sample_data

-- #############################################################################
--                        DATABASE CREATION SCRIPTS
-- #############################################################################
CREATE SEQUENCE IF NOT EXISTS public.seq_adsb_uid
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

ALTER SEQUENCE public.seq_adsb_uid
    OWNER TO shoc;

CREATE TABLE IF NOT EXISTS public.adsb_import
(
    uid integer NOT NULL DEFAULT nextval('seq_adsb_uid'::regclass),
    json jsonb,
    CONSTRAINT "adsb-import_pkey" PRIMARY KEY (uid)
) TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.adsb_import
    OWNER to shoc;

-- #############################################################################
--                        AFTER IMPORTING DATA CONVERT TO ARRAY
-- #############################################################################
CREATE SEQUENCE IF NOT EXISTS public.seq_adsb_msg_uid
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

ALTER SEQUENCE public.seq_adsb_msg_uid
    OWNER TO shoc;

CREATE TABLE IF NOT EXISTS public.adsb_message
(
	uid integer NOT NULL DEFAULT nextval('seq_adsb_msg_uid'::regclass),
	timestamp timestamp,
    json jsonb,
    CONSTRAINT "adsb_msg_pkey" PRIMARY KEY (uid)
) TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.adsb_message
    OWNER to shoc;


-- #############################################################################
--                    VIEWS FOR THE DASHBOARD2
-- #############################################################################
 -- View: public.adsb_parsed_messages
 -- DROP VIEW public.adsb_parsed_messages;
CREATE OR REPLACE VIEW public.adsb_parsed_messages
 AS
SELECT adsb_message."timestamp",
    adsb_message.json ->> 'r'::text AS r,
    adsb_message.json ->> 't'::text AS t,
    adsb_message.json ->> 'gs'::text AS gs,
    adsb_message.json ->> 'rc'::text AS rc,
    adsb_message.json ->> 'gva'::text AS gva,
    adsb_message.json ->> 'hex'::text AS hex,
    adsb_message.json ->> 'lat'::text AS lat,
    adsb_message.json ->> 'lon'::text AS lon,
    adsb_message.json ->> 'nic'::text AS nic,
    adsb_message.json ->> 'sda'::text AS sda,
    adsb_message.json ->> 'sil'::text AS sil,
    adsb_message.json ->> 'spi'::text AS spi,
    adsb_message.json ->> 'mlat'::text AS mlat,
    adsb_message.json ->> 'rssi'::text AS rssi,
    adsb_message.json ->> 'seen'::text AS seen,
    adsb_message.json ->> 'tisb'::text AS tisb,
    adsb_message.json ->> 'type'::text AS type,
    adsb_message.json ->> 'alert'::text AS alert,
    adsb_message.json ->> 'nac_p'::text AS nac_p,
    adsb_message.json ->> 'nac_v'::text AS nac_v,
    adsb_message.json ->> 'track'::text AS track,
    adsb_message.json ->> 'flight'::text AS flight,
    adsb_message.json ->> 'squawk'::text AS squawk,
    adsb_message.json ->> 'nav_qnh'::text AS nav_qnh,
    adsb_message.json ->> 'version'::text AS version,
    adsb_message.json ->> 'alt_baro'::text AS alt_baro,
    adsb_message.json ->> 'alt_geom'::text AS alt_geom,
    adsb_message.json ->> 'category'::text AS category,
    adsb_message.json ->> 'messages'::text AS messages,
    adsb_message.json ->> 'nic_baro'::text AS nic_baro,
    adsb_message.json ->> 'seen_pos'::text AS seen_pos,
    adsb_message.json ->> 'sil_type'::text AS sil_type,
    adsb_message.json ->> 'baro_rate'::text AS baro_rate,
    adsb_message.json ->> 'emergency'::text AS emergency,
    adsb_message.json ->> 'nav_heading'::text AS nav_heading,
    adsb_message.json ->> 'nav_altitude_mcp'::text AS nav_altitude_mcp
   FROM adsb_message;

ALTER TABLE public.adsb_parsed_messages
    OWNER TO shoc;

-- #############################################################################
--                    VIEWS FOR THE DASHBOARD
-- #############################################################################
-- View: public.adsb_passed_through_lv
-- DROP VIEW public.adsb_passed_through_lv;
CREATE OR REPLACE VIEW public.adsb_passed_through_lv
 AS
 SELECT DISTINCT adsb_parsed_messages.hex
   FROM adsb_parsed_messages
  WHERE adsb_parsed_messages.lat::double precision >= 35.92282861217139::double precision AND adsb_parsed_messages.lat::double precision <= 36.35390507533636::double precision AND adsb_parsed_messages.lon::double precision >= '-115.47311433635576'::numeric::double precision AND adsb_parsed_messages.lon::double precision <= '-114.77403574646269'::numeric::double precision;

ALTER TABLE public.adsb_passed_through_lv
   OWNER TO shoc;


-- #############################################################################
--                    VIEWS FOR THE DASHBOARD3
-- #############################################################################
-- View: public.adsb_parsed_lv_messages
-- DROP VIEW public.adsb_parsed_lv_messages;

CREATE OR REPLACE VIEW public.adsb_parsed_lv_messages
 AS
SELECT adsb_parsed_messages."timestamp",
    adsb_parsed_messages.r,
    adsb_parsed_messages.t,
    adsb_parsed_messages.gs,
    adsb_parsed_messages.rc,
    adsb_parsed_messages.gva,
    adsb_parsed_messages.hex,
    adsb_parsed_messages.lat,
    adsb_parsed_messages.lon,
    adsb_parsed_messages.nic,
    adsb_parsed_messages.sda,
    adsb_parsed_messages.sil,
    adsb_parsed_messages.spi,
    adsb_parsed_messages.mlat,
    adsb_parsed_messages.rssi,
    adsb_parsed_messages.seen,
    adsb_parsed_messages.tisb,
    adsb_parsed_messages.type,
    adsb_parsed_messages.alert,
    adsb_parsed_messages.nac_p,
    adsb_parsed_messages.nac_v,
    adsb_parsed_messages.track,
    adsb_parsed_messages.flight,
    adsb_parsed_messages.squawk,
    adsb_parsed_messages.nav_qnh,
    adsb_parsed_messages.version,
    adsb_parsed_messages.alt_baro,
    adsb_parsed_messages.alt_geom,
    adsb_parsed_messages.category,
    adsb_parsed_messages.messages,
    adsb_parsed_messages.nic_baro,
    adsb_parsed_messages.seen_pos,
    adsb_parsed_messages.sil_type,
    adsb_parsed_messages.baro_rate,
    adsb_parsed_messages.emergency,
    adsb_parsed_messages.nav_heading,
    adsb_parsed_messages.nav_altitude_mcp
   FROM adsb_parsed_messages
  WHERE adsb_parsed_messages.lat::double precision >= 35.92282861217139::double precision AND adsb_parsed_messages.lat::double precision <= 36.35390507533636::double precision AND adsb_parsed_messages.lon::double precision >= '-115.47311433635576'::numeric::double precision AND adsb_parsed_messages.lon::double precision <= '-114.77403574646269'::numeric::double precision;

ALTER TABLE public.adsb_parsed_lv_messages
    OWNER TO shoc;


