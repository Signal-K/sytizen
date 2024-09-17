-- Allow authenticated users to insert (upload) files
CREATE POLICY "Allow file uploads for authenticated users"
ON storage.objects
FOR INSERT
USING (auth.uid() IS NOT NULL);

-- Secondary
(bucket_id = 'anomalies'::text)