import { supabase } from "./client";

export default function handler(req, res) {
    supabase.auth.resetPasswordForEmail.setAuthCookie(req, res); // set or clear the cookies based on user action
}