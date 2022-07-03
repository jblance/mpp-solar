# Using with PostgreSQL

try running `mpp-solar --help`. This should describe how PostgreSQL url can be used:

  --postgres_url POSTGRES_URL
                        PostgresSQL connection url, example postgresql://user:password@server:5432/postgres
  
Connection string reference: (https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)

The `user` with the `password` must be available in advance on the postgres server.

The code runs `insert into mppsolar (command,data, updated) values (%s,%s,%s)', (command, msg, now)` on every message
received from the inverter. There must be a table created and accessible from advance as well. Example DML code
for the table creation:

    create table mppsolar
    (
        id      serial
            constraint mppsolar_pk
                primary key,
        command varchar,
        data    json,
        updated timestamp
    );
    
    alter table mppsolar
        owner to postgres;
    
    create index mppsolar_command_updated_index
        on mppsolar (command, updated);
    
Validating data from the table:

    select * from mppsolar;

and this should return data example like this:

    32290,PS,"{""solar_input_power_1"": 4244, ""solar_input_power_2"": 0, ""battery_power"": """", ""ac_input_active_power_r"": -1346, ""ac_input_active_power_s"": -1348, ""ac_input_active_power_t"": -1365, ""ac_input_total_active_power"": -4059, ""ac_output_active_power_r"": 0, ""ac_output_active_power_s"": 0, ""ac_output_active_power_t"": 0, ""ac_output_total_active_power"": 0, ""ac_output_apparent_power_r"": 47, ""ac_output_apparent_power_s"": 96, ""ac_output_apparent_power_t"": 121, ""ac_output_total_apparent_power"": 264, ""ac_output_power_percentage"": 3, ""ac_output_connect_status"": ""Connected"", ""solar_input_1_work_status"": ""Working"", ""solar_input_2_work_status"": ""Idle"", ""battery_power_direction"": ""Charging"", ""dc/ac_power_direction"": ""DC to AC"", ""line_power_direction"": ""Output"", ""updated"": ""2022-05-15T11:24:28+02:00""}",2022-05-15 11:24:28.000000
    32291,GS,"{""solar_input_voltage_1"": 5043, ""solar_input_voltage_2"": 0, ""solar_input_current_1"": 850, ""solar_input_current_2"": 0, ""battery_voltage"": 532, ""battery_capacity"": 98, ""battery_current"": 28, ""ac_input_voltage_r"": 2386, ""ac_input_voltage_s"": 2416, ""ac_input_voltage_t"": 2425, ""ac_input_frequency"": 5004, ""ac_input_current_r"": 0, ""ac_input_current_s"": 0, ""ac_input_current_t"": 0, ""ac_output_voltage_r"": 2384, ""ac_output_voltage_s"": 2416, ""ac_output_voltage_t"": 2427, ""ac_output_frequency"": 5001, ""ac_output_current_r"": """", ""ac_output_current_s"": """", ""ac_output_current_t"": """", ""inner_temperature"": 30, ""component_max_temperature"": 43, ""external_battery_temperature"": 0, ""setting_change_bit"": ""No setting change"", ""updated"": ""2022-05-15T11:24:31+02:00""}",2022-05-15 11:24:31.000000
    32292,MOD,"{""working_mode"": ""Hybrid mode (Line mode, Grid mode)"", ""updated"": ""2022-05-15T11:24:33+02:00""}",2022-05-15 11:24:33.000000
    32293,PS,"{""solar_input_power_1"": 4236, ""solar_input_power_2"": 0, ""battery_power"": """", ""ac_input_active_power_r"": -1344, ""ac_input_active_power_s"": -1343, ""ac_input_active_power_t"": -1367, ""ac_input_total_active_power"": -4054, ""ac_output_active_power_r"": 0, ""ac_output_active_power_s"": 0, ""ac_output_active_power_t"": 0, ""ac_output_total_active_power"": 0, ""ac_output_apparent_power_r"": 47, ""ac_output_apparent_power_s"": 96, ""ac_output_apparent_power_t"": 121, ""ac_output_total_apparent_power"": 264, ""ac_output_power_percentage"": 3, ""ac_output_connect_status"": ""Connected"", ""solar_input_1_work_status"": ""Working"", ""solar_input_2_work_status"": ""Idle"", ""battery_power_direction"": ""Charging"", ""dc/ac_power_direction"": ""DC to AC"", ""line_power_direction"": ""Output"", ""updated"": ""2022-05-15T11:25:05+02:00""}",2022-05-15 11:25:05.000000

And the `data` column is type *json*. So more complex queries can be done to query by the JSON content like this:

    select data ->> 'solar_input_power_1'  from mppsolar where command = 'PS';

this will show just solar power from output of the PS command. Or the JSON data can be included into the where condition like this:

    select data ->> 'solar_input_power_1'  from mppsolar where command = 'PS' and CAST ( data ->> 'solar_input_power_1' AS INTEGER) > 0;

Reference: (https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-json/)


    