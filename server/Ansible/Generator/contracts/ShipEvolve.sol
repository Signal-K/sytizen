// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.0;

import "@thirdweb-dev/contracts/base/ERC1155LazyMint.sol";

contract ShipEvolveContract is ERC1155LazyMint {
    constructor(
        string memory _name,
        string memory _symbol
    ) ERC1155LazyMint(_name, _symbol, 0) {}

    function verifyClaim(
        address _claimer,
        uint256 _tokenId,
        uint256 _quantity // Duplicate for planets, add physical location (updated from unity-side)
    ) public view override { // Pull this data and export into Supabase through Moralis speedy nodes -> add crafting feature through API and pass into contract-side
        require(_tokenId == 0, "Only base spaceship is claimable"); // The first spaceship (ERC1155) is the base model, and can be claimed
        require(_quantity == 1, "You can only claim one spaceship at a time"); // However, you can claim multiple spaceships, just over multiple claim transactions
    }

    function evolve() public {
        _burn(msg.sender, 0, 2); // Destroy two of the user's base spaceships to evolve (aka mint) the second spaceship
        _mint(msg.sender, 1, 1, ""); // 1 level 2 spaceship for 2 level 1 spaceships
    }
}
// Deploy with `npx thirdweb deploy`