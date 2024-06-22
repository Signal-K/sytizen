ALTER TABLE public.missions
ADD COLUMN rewarded_items BIGINT[] NULL;

-- Add the parentItem column if it does not already exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name='inventory' AND column_name='parentItem') THEN
        ALTER TABLE public."inventory"
        ADD COLUMN "parentItem" BIGINT NULL;
    END IF;
END
$$;

-- Add the foreign key constraint for parentItem
ALTER TABLE public."inventory"
ADD CONSTRAINT inventory_parentItem_fkey FOREIGN KEY ("parentItem") REFERENCES public."inventory" (id);

-- Ensure the existing foreign key constraints are added (skip if they already exist)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints 
                   WHERE table_name='inventory' AND constraint_name='inventory_anomaly_fkey') THEN
        ALTER TABLE public."inventory"
        ADD CONSTRAINT inventory_anomaly_fkey FOREIGN KEY (anomaly) REFERENCES public."anomalies" (id);
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints 
                   WHERE table_name='inventory' AND constraint_name='inventory_owner_fkey') THEN
        ALTER TABLE public."inventory"
        ADD CONSTRAINT inventory_owner_fkey FOREIGN KEY (owner) REFERENCES public.profiles (id);
    END IF;
END
$$;

-- Add the parentAnomaly column
ALTER TABLE public.anomalies
ADD COLUMN "parentAnomaly" BIGINT NULL;

-- Add the foreign key constraint for parentAnomaly
ALTER TABLE public.anomalies
ADD CONSTRAINT anomalies_parentAnomaly_fkey FOREIGN KEY ("parentAnomaly") REFERENCES public.anomalies (id);

-- Add the classificationType column
ALTER TABLE public.classifications
ADD COLUMN classificationType TEXT NULL;
