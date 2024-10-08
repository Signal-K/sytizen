CREATE TABLE public."inventory" (
    id bigint generated by default as identity,
    item bigint null, 
    owner uuid null,
    quantity double precision null,
    notes text null,
    "parentItem" bigint null,
    time_of_deploy timestamp with time zone null,
    "anomaly" bigint null,
    constraint inventory_pkey primary key (id),
    constraint inventory_parentItem_fkey foreign key ("parentItem") references public."inventory" (id), -- Corrected table name in foreign key reference
    constraint inventory_anomaly_fkey foreign key ("anomaly") references public."anomalies" (id), -- Corrected table name in foreign key reference
    constraint inventory_owner_fkey foreign key (owner) references public.profiles (id) -- Assuming "profiles" table is in the public schema
) tablespace pg_default;