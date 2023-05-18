import { createClient } from '@supabase/supabase-js';
import * as fs from 'fs';
import * as path from 'path';

// Initialize Supabase client
const supabaseUrl = 'https://qwbufbmxkjfaikoloudl.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDE3NTksImV4cCI6MTk4NTUxNzc1OX0.RNz5bvsVwLvfYpZtUjy0vBPcho53_VS2AIVzT8Fm-lk'
const supabase = createClient(supabaseUrl, supabaseKey);

// Define the directory containing the image files
const outputDirectory = path.join(__dirname, 'output');

// Get an array of all image files in the directory
const imageFiles = fs.readdirSync(outputDirectory).filter((file) => {
  const extension = path.extname(file);
  return extension === '.jpg' || extension === '.jpeg' || extension === '.png';
});

// Upload each image file to the "planets" bucket
imageFiles.forEach(async (file) => {
  const filePath = path.join(outputDirectory, file);
  const fileBuffer = fs.readFileSync(filePath);
  const { data, error } = await supabase.storage.from('planets').upload(file, fileBuffer);
  if (error) {
    console.error(error);
  } else {
    console.log(`File ${file} uploaded successfully!`);
  }
});