import { useEffect, useState } from 'react';
import { supabase } from '../lib/initSupabase';

export default function CountryList() {
  const [countries, setCountries] = useState([]);
  const [newCountry, setNewCountry] = useState('');

  useEffect(() => {
    fetchCountries();
  }, []);

  const fetchCountries = async () => {
    const { data: countries } = await supabase
      .from('countries')
      .select('*')
      .order('name', true);
    setCountries(countries);
  };

  const addCountry = async (countryName) => {
    let { data: country } = await supabase
      .from('countries')
      .insert({ name: countryName })
      .single();
    setCountries([...countries, country]);
  };

  const deleteCountry = async (countryId) => {
    try {
      await supabase.from('countries').delete().eq('id', countryId);
      setCountries(countries.filter((country) => country.id != countryId));
    } catch (error) {
      console.log('error', error);
    }
  };

  return (
    <main>
      <div>
        <input
          type='text'
          placeholder='My Made Up Country'
          value={newCountry}
          onChange={(e) => {
            setNewCountry(e.target.value);
          }}
        />
        <button onClick={() => addCountry(newCountry)}>Add</button>
      </div>
      <ul>
        {countries.map((country) => (
          <li key={country.id}>
            {country.name}{' '}
            <button onClick={() => deleteCountry(country.id)}>
              <svg
                xmlns='http://www.w3.org/2000/svg'
                aria-hidden='true'
                focusable='false'
                role='img'
                viewBox='0 0 448 512'
                width='0.75rem'
              >
                <path
                  fill='currentColor'
                  d='M32 464C32 490.5 53.5 512 80 512h288c26.5 0 48-21.5 48-48V128H32V464zM304 208C304 199.1 311.1 192 320 192s16 7.125 16 16v224c0 8.875-7.125 16-16 16s-16-7.125-16-16V208zM208 208C208 199.1 215.1 192 224 192s16 7.125 16 16v224c0 8.875-7.125 16-16 16s-16-7.125-16-16V208zM112 208C112 199.1 119.1 192 128 192s16 7.125 16 16v224C144 440.9 136.9 448 128 448s-16-7.125-16-16V208zM432 32H320l-11.58-23.16c-2.709-5.42-8.25-8.844-14.31-8.844H153.9c-6.061 0-11.6 3.424-14.31 8.844L128 32H16c-8.836 0-16 7.162-16 16V80c0 8.836 7.164 16 16 16h416c8.838 0 16-7.164 16-16V48C448 39.16 440.8 32 432 32z'
                />
              </svg>
            </button>
          </li>
        ))}
      </ul>
    </main>
  );
}
