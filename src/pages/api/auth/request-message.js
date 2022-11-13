import Moralis from "moralis";

const config = {
    domain: "sytizen.vercel.app",
    statement: 'Please sign eh',
    uri: 'http://localhost:3000',
    timeout: 60,
};

export default async function handler(req, res) {
    const { address, chain, network } = req.body;
    await Moralis.start({ apiKey: 'kJfYYpmMmfKhvaWMdD3f3xMMb24B4MHBDDVrfjslkKgTilvMgdwr1bwKUr8vWdHH' });
    try {
        const message = await Moralis.Auth.requestMessage({
            address,
            chain,
            network,
            ...config,
        });
        res.status(200).json(message);
    } catch (error) {
        res.status(400).json({ error });
        console.error(error);
    }
}

// uri 4e314eaa925f4e85fbae0f00978803df