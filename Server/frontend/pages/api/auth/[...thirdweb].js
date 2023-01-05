import { ThirdwebAuth } from '@thirdweb-dev/auth';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
    process.env.SUPABASE_URL || "",
    process.env.SUPABASE_SERVICE_ROLE || "",
);

const login = async (address) => {
    const { data: user } = await supabase
        .from("users")
        .select("*")
        .eq("address", address.toLowerCase())
        .single();

    if (!user) {
        const res = await supabase
            .from("users")
            .insert({ address: address.toLowerCase() })
            .single();
    
        if (res.error) {
            throw new Error("Failed to create user!");
        }
    };
}

const user = async (address) => {
    // Fetch the user data in our DB associated with the specified address
    const { data: user } = await supabase
      .from("users")
      .select("*")
      .eq("address", address.toLowerCase())
      .single();
  
    return user;
};

export const { ThirdwebAuthHandler, getUser } = ThirdwebAuth({
    privateKey: process.env.ADMIN_PRIVATE_KEY || "",
    domain: 'portal.skinetics.tech',
    callbacks: { login, user },
});

export default ThirdwebAuthHandler();