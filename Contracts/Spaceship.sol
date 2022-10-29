// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@thirdweb-dev/contracts/base/ERC1155LazyMint.sol";

contract Spaceship is ERC1155LazyMint {
    constructor(
        string memory _name,
        string memory _symbol
    ) ERC1155LazyMint(_name, _symbol, msg.sender, 0) { } // 0 Royalty amount

    function burn( // Sort of like a crafting function -> https://github.com/Signal-K/sytizen/commit/39da03aec3e9bf14dd33125487f0cfe6ec58290d
        address _owner, // Burning gen 1 = gen 2. Then we can add "recipes" ^^
        uint256 _tokenId,
        uint256 _amount
    ) external override {
        address caller = msg.sender;
        require(caller == _owner || isApprovedForAll[_owner][caller], "Unapproved Caller");
        require(balanceOf[_owner][_tokenId] >= _amount, "Not enough tokens owned");

        _burn(_owner, _tokenId, _amount);

        if(_tokenId == 0) { // If base spaceship model
            _mint(_owner, 1, 1, ""); // id: 1 (2nd model), quantity: 1, address ""
        }
    }
}