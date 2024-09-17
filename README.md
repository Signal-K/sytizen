# sytizen-unity
[![.github/workflows/moralis.yml](https://github.com/Signal-K/sytizen/actions/workflows/moralis.yml/badge.svg?branch=ansible)](https://github.com/Signal-K/sytizen/actions/workflows/moralis.yml)
[![Node.js CI](https://github.com/Signal-K/sytizen/actions/workflows/node.js.yml/badge.svg)](https://github.com/Signal-K/sytizen/actions/workflows/node.js.yml)
[![Node.js CI](https://github.com/Signal-K/sytizen/actions/workflows/node.js.yml/badge.svg?branch=wb3-7--interacting-with-anomalies-from-smart)](https://github.com/Signal-K/sytizen/actions/workflows/node.js.yml)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/signal-k/sytizen/HEAD)
[![](https://github.com/Signal-K/sytizen/actions/workflows/node.js.yml/badge.svg?branch=wb3-7--interacting-with-anomalies-from-smart)](https://deepnote.com/workspace/star-sailors-49d2efda-376f-4329-9618-7f871ba16007/project/Supabase-Talk-ab6b31e5-13c3-4949-af38-1197d00bd4d1/notebook/Flask%20API-cb9219547b9e4e228b15cbf8a1aa9cf4#99de0381ef0d40ffaee2354354861bae)
[![](https://badges.thirdweb.com/contract?address=0xCcaA1ABA77Bae6296D386C2F130c46FEc3E5A004&theme=light&chainId=5)](https://thirdweb.com/goerli/0xCcaA1ABA77Bae6296D386C2F130c46FEc3E5A004?utm_source=contract_badge)

# Signal-K/Sytizen Repo
## Related repositories
* [Signal-K/polygon](https://github.com/Signal-K/polygon/issues/26) ↝ Contract interactions
* [Signal-K/client](https://github.com/Signal-K/client) ↝ Frontend for interactions with our contracts

## Documentation
All documentation is visible on [Notion](https://www.notion.so/skinetics/Sample-Planets-Contract-4c3bdcbca4b9450382f9cc4e72e081f7)

# Citizen Science Classifications
## Process
* User mints an anomaly that has appeared in their UI (for now, the webapp, later it will be the game as well)
* API searches for a token that has already been lazy minted with the TIC id of the anomaly (or the identifier of the candidate)
  * If there is a token id that has the TIC Id, then claim a copy of that to the `msg.sender` (player’s address) so they can manipulate it in-game
  * If the TIC ID has never been minted before, lazy mint a new one with parameters fetched from the data source and send it to `msg.sender`
  * Return the IPFS metadata
* Add some buttons that allow manipulations for the NFT (e.g. viewing (reading) metadata (e.g. image/video files, graphs).
  * Graphs should be generated in a Jupyter notebook and returned in the Next app.
* User creates post (proposal [Proposal Board → Migration from Vite](https://www.notion.so/Proposal-Board-Migration-from-Vite-2e3ef95e384d4ac1875e0dbbe9a59337)) with the NFT ID for their anomaly and some extra metadata for their discoveries and proposal, and then users can vote

## Planet Generation
### Light Curve/Exofop + Unity integration
See `/tests/quarterKurve.py`
**API Release Notes: Exoplanet Habitability Assessment**

**Version 1.0**

We are excited to introduce the Exoplanet Habitability Assessment API, a tool designed to provide an estimate of habitability for exoplanets based on their light curve data. This API aims to assist in identifying potential habitable exoplanets and understanding their characteristics. Here are the key features and details of this initial release:

**1. Overview:**
The Exoplanet Habitability Assessment API leverages the lightkurve library and integrates with external data sources to analyze light curve data and calculate habitability scores for exoplanets. The API provides information on the number of trees, a rough estimate of habitability, and insights into potential life types and resource availability.

**2. Input:**
The API accepts a Target Identification (TIC) ID, which uniquely identifies a star and its associated exoplanets. The TIC ID is used to retrieve the light curve data for analysis.

**3. Analysis Process:**
Upon receiving a TIC ID, the API performs the following steps:

- Light Curve Retrieval: The API retrieves the light curve data for the specified TIC ID using the lightkurve library.

- Amplitude Calculation: The amplitude, representing the variation in the brightness of the star over time, is calculated from the light curve data.

- Number of Trees Calculation: The amplitude is used to estimate the number of trees, indicating a rough measure of habitability. The number of trees is determined based on predefined thresholds and corresponding values.

- Habitability Score Calculation: The number of trees is combined with the amplitude to calculate a habitability score. The habitability score provides an indicator of potential habitability, considering both the amplitude and the estimated habitable environment.

- Life Type Determination: The habitability score is used to determine the most likely type of life that could exist on the exoplanet. The classification includes advanced life forms, complex life forms, microbial life, or no known life forms.

- Resource Type Assessment: The radius of the star and the calculated planet radius are used to estimate the availability of resources. The resource type is determined based on the star and planet radius, categorizing them as heavy elements (e.g., gold, silver, iron) or basic resources (e.g., carbon, minerals).

**4. Output:**
The API provides the following outputs:

- Amplitude: Represents the variation in the brightness of the star over time. This value indicates the level of fluctuation in the light curve.

- Number of Trees: An estimate of the habitability of the exoplanet, based on the amplitude. The number of trees reflects the rough potential for habitability.

- Habitability Score: A combined score that incorporates the number of trees and the amplitude. It provides an overall measure of potential habitability for the exoplanet.

- Life Type: A prediction of the most likely type of life that could exist on the exoplanet, based on the habitability score.

- Resource Type: An estimation of the available resources on the exoplanet, categorized as heavy elements or basic resources.

**5. Limitations and Compromises:**
The current version of the API has the following limitations and compromises:

- Simplified Calculations: The calculations and thresholds used in the API are based on approximate assumptions and simplified models. This may lead to some inaccuracies in the results. Future versions will incorporate more sophisticated models and refined calculations.

- Limited Data Sources: The API relies on the lightkurve library and external data sources for star and planet information. Integration with additional data sources and endpoints will be implemented in future versions to enhance the accuracy and reliability of the results.

**6. Integration with Unity Editor:**
The Exoplanet Habitability Assessment API is designed to seamlessly integrate with the Unity Editor, providing developers with the ability to query the API using TIC IDs and retrieve habitability-related information for exoplanets. The API responses can be used within Unity projects to enhance gameplay mechanics, generate exoplanet visuals, and facilitate resource management systems.

**7. Future Enhancements:**
In upcoming releases, we plan to introduce the following enhancements:

- Integration with Stellar Information: The API will integrate with additional endpoints and databases to retrieve accurate and detailed information about stars, including mass, radius, and other relevant parameters.

- Refinement of Habitability Calculations: The habitability score calculation will be further refined using advanced models and additional factors, such as planetary temperature, atmospheric composition, and stellar radiation.

- Resource Estimation Improvements: The estimation of available resources will be enhanced by considering factors like the star's metallicity and the planet's geological composition.

- Real-time Data Updates: The API will be connected to live data sources to provide up-to-date information on exoplanets and their habitability.

We are excited to continue improving the Exoplanet Habitability Assessment API to deliver more accurate and comprehensive insights into exoplanet habitability. Your feedback and suggestions are invaluable as we work towards refining the tool and expanding its capabilities.

Please note that the API is provided for research and educational purposes and should not be considered a definitive source for exoplanet habitability. The results should be interpreted with caution and verified through additional research and observations.