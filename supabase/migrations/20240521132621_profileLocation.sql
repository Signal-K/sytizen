ALTER TABLE public.profiles
ADD COLUMN location int8 REFERENCES public.anomalies(id); 