// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.0;

import "@thirdweb-dev/contracts/base/ERC1155LazyMint.sol";

contract SpaceshipContract is ERC1155LazyMint {
    constructor(
        string memory _name,
        string memory _symbol
    ) ERC1155LazyMint(_name, _symbol, msg.sender, 0) {}

    function burn ( address _owner, uint256 _tokenId, uint256 _amount ) external override {
        address caller = msg.sender;

        require(caller == _owner || isApprovedForAll[_owner][caller], "Unapproved caller");
        require(balanceOf[_owner][_tokenId] >= _amount, "Not enough tokens owned");
        
        _burn(_owner, _tokenId, _amount);
        if (_tokenId == 0) {
            _mint(_owner, 1, _amount, "");
        }
    }
}