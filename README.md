# sytizen-unity
[![.github/workflows/moralis.yml](https://github.com/Signal-K/sytizen/actions/workflows/moralis.yml/badge.svg?branch=ansible)](https://github.com/Signal-K/sytizen/actions/workflows/moralis.yml) <br />
Citizen Science (Sci-tizen) visualisation in the Unity.com engine 


Check out our compass [here](http://ar.skinetics.tech/stellarios/compass) for more information about this product

# Contracts
<a href="https://thirdweb.com/goerli/0xCcaA1ABA77Bae6296D386C2F130c46FEc3E5A004?utm_source=contract_badge" target="_blank">
    <img width="200" height="45" src="https://badges.thirdweb.com/contract?address=0xCcaA1ABA77Bae6296D386C2F130c46FEc3E5A004&theme=dark&chainId=5" alt="View contract" />
</a>

<!--
Move `/server` into a separate submodule (or `styizen` into a submodule in another repo)
Add react config (for frontend framework) to react, then move it into `signal-k/polygon`
-->

## Trader branch
This branch contains a connection between Supabase (our current hosting platform for this backend) and the rest our our Notebooks & API. Everything else has been stripped out of this branch.

Run `python3 -m venv .venv` to get started.

Note: Start integrating in API from signal-k/polygon

### Planti branch
Stripping everything out (e.g. `Ansible`/`Generator`) and just leaving the initial dashboard/game frontend. We'll merge it back with `Trader` later