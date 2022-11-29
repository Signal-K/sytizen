// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@thirdweb-dev/contracts/extension/Permissions.sol";
import "@thirdweb-dev/contracts/base/ERC20SignatureMintVote.sol";

contract Contract is ERC20SignatureMintVote, Permissions {
    // bytes32 public constant NUMBER_ROLE = keccak256("NUMBER_ROLE"); test role
    bool public allowSale;
    constructor(
        string memory _name,
        string memory _symbol,
        address _primarySaleRecipient
    )
        ERC20SignatureMintVote(
            _name,
            _symbol,
            _primarySaleRecipient
        )
    {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender); // Deployer is admin, can stop sale of tokens at any time
    }

    function startSale(bool _allowSale) public onlyRole(DEFAULT_ADMIN_ROLE) {
        allowSale = _allowSale;
    }

    function mintTo(address _to, uint256 _amount) public virtual override {
        require(allowSale == true, "Minting currently closed"); // Display message IF !=
        super.mintTo(_to, _amount); // address to send _amount to
    }
}