Users will be added with the following attributes:
1. Email (retrieved from the Magic SDK)
2. Supabase ID (retrieved when we push 1) to a new Supabase user [entry])
3. Eth address (from their Metamask wallet) -> this can be updated after signing in with Magic, through a form + wagmi protocol
4. Eth address (from their Magic wallet)

## Adding users using Postman
Create a post request like this: ![](../assets/requests/user-add-post.png)

Then we need to modify the body of the POST request: <!--Then get data from Anvil and process it here-->