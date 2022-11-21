// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.11;

/* Import thirdweb contracts
import "@thirdweb-dev/contracts/drop/DropERC1155.sol"; // For tool collection
import "@thirdweb-dev/contracts/token/TokenERC20.sol"; // For the minerals collection

// OpenZeppelin ReentrancyGuard
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@thirdweb-dev/contracts/openzeppelin-presets/utils/ERC1155/ERC1155Holder.sol"; // This contract is now capable of holding 1155 nfts */

// Import thirdweb contracts
import "@thirdweb-dev/contracts/drop/DropERC1155.sol"; // For my collection of Pickaxes
import "@thirdweb-dev/contracts/token/TokenERC20.sol"; // For my ERC-20 Token contract
import "@thirdweb-dev/contracts/openzeppelin-presets/utils/ERC1155/ERC1155Holder.sol"; // For my ERC-1155 Receiver contract

// OpenZeppelin (ReentrancyGuard)
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract Multitooling is ReentrancyGuard, ERC1155Holder {
    DropERC1155 public immutable multitoolNftCollection;
    TokenERC20 public immutable mineralsToken;

    // Set the rewards token & the NFT collection address
    constructor(DropERC1155 multitoolContractAddress, TokenERC20 mineralsContractAddress) {
        multitoolNftCollection = multitoolContractAddress;
        mineralsToken = mineralsContractAddress;
    }

    struct MapValue {
        bool isData; // Turn on/off depending on if nft data is currently staked
        uint256 value; // Stores tokenId of nft being staked
    }

    mapping (address => MapValue) public playerMultitool; // Map the player to their current multitool. Occurs when they stake a multitool
    mapping(address => MapValue) public playerLastUpdate; // Player address to last time they staked/withdrew/claimed rewards.

    // Stake functionality
    function stake(uint256 _tokenId) external nonReentrant {
        require(multitoolNftCollection.balanceOf(msg.sender, _tokenId) >= 1, "You require at least one multitool to stake"); // Takes the desired level of multitool (tokenId) into account as well
        
        if (playerMultitool[msg.sender].isData) { // If the player already has a multitool, send it back to them
            multitoolNftCollection.safeTransferFrom(address(this), msg.sender, playerMultitool[msg.sender].value, 1, "Returning your old multitool");
        }

        uint256 reward = calculateRewards(msg.sender);
        mineralsToken.transfer(msg.sender, reward);

        // Transfer the multitool to the contract
        multitoolNftCollection.safeTransferFrom(msg.sender, address(this), _tokenId, 1, "Staking your multitool now"); // From user/player address to this contract's address
        playerMultitool[msg.sender].value = _tokenId; // Update multitool mapping
        playerMultitool[msg.sender].isData = true;
        playerLastUpdate[msg.sender].isData = true; // Update playerLastUpdate mapping
        playerLastUpdate[msg.sender].value = block.timestamp;
    }

    // Withdraw your multitool from this staking contract
    function withdraw() external nonReentrant {
        require(playerMultitool[msg.sender].isData, "You do not have a multitool to withdraw"); // Ensure the player has a multitool
        uint256 reward = calculateRewards(msg.sender); // Calculate rewards owed to the player
        mineralsToken.transfer(msg.sender, reward);
        multitoolNftCollection.safeTransferFrom(address(this), msg.sender, playerMultitool[msg.sender].value, 1, "Returning the multitool to you");
        
        // Update mapping
        playerMultitool[msg.sender].isData = false;
        playerLastUpdate[msg.sender].isData = true;
        playerLastUpdate[msg.sender].value = block.timestamp;
    }

    // Claim owed minerals manually
    function claim() external nonReentrant {
        uint256 reward = calculateRewards(msg.sender);
        mineralsToken.transfer(msg.sender, reward);

        // Update mappings
        playerLastUpdate[msg.sender].isData = true;
        playerLastUpdate[msg.sender].value = block.timestamp; // Last call is set to the current block time
    }

    // Calculate & process rewards
    function calculateRewards(address _player) /// Rewards rate -> 20M minerals per block. 
        public /// Calculate rewards since last time the player was paid out
        view /// use block.timestamp and playerLastUpdate
        returns (uint256 _rewards) { 
            if (!playerLastUpdate[_player].isData || !playerMultitool[_player].isData) { // If either is not set
                return 0;
            }
            uint256 timeDifference = block.timestamp - playerLastUpdate[_player].value; // Calculate time difference between NOW and when the player last actioned their reward
            uint256 rewards = timeDifference * 10_000_000_000_000 * (playerMultitool[_player].value + 1); // Calculate rewards user is owed. Formatted to 18 decimals
            return rewards; // View for each player
    }
}