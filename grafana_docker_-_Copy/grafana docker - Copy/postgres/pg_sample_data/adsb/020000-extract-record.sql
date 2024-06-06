SET search_path TO sample_data;
\connect sample_data

insert into adsb_message (timestamp, json)  
	(select to_timestamp((adsb_import.json->>'now')::float) as timestamp, adsb_import2.json as json
	 from adsb_import 
	 CROSS JOIN (select jsonb_array_elements((json->>'aircraft')::jsonb) as json from adsb_import) adsb_import2);
