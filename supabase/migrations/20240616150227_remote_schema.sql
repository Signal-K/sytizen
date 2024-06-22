alter table "public"."anomalies" drop constraint "anomalies_parentanomaly_fkey";

alter table "public"."inventory" drop constraint "inventory_parentitem_fkey";

alter table "public"."missions" drop constraint "missions_user_fkey";

alter table "public"."anomalies" drop column "parentAnomaly";

alter table "public"."classifications" drop column "classificationtype";

alter table "public"."inventory" drop column "parentItem";

alter table "public"."missions" drop column "rewarded_items";

alter table "public"."missions" alter column "user" drop not null;

alter table "public"."missions" add constraint "missions_user_fkey" FOREIGN KEY ("user") REFERENCES profiles(id) not valid;

alter table "public"."missions" validate constraint "missions_user_fkey";


