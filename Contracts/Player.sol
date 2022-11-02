// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;
// Merge with `Spaceship.sol` -> this is just a slightly more advanced version for a test component on the frontend

// Import thirdweb contracts
import "@thirdweb-dev/contracts/drop/DropERC1155.sol"; // For my collection of Pickaxes
import "@thirdweb-dev/contracts/token/TokenERC20.sol"; // For my ERC-20 Token contract
import "@thirdweb-dev/contracts/openzeppelin-presets/utils/ERC1155/ERC1155Holder.sol"; 

// OpenZeppelin Guards
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract Mining is ReentrancyGuard, ERC1155Holder {
    // Store edition drop & token contract [addresses] here
    DropERC1155 public immutable spaceshipNftCollection; // Jumping UFO game component (flying between points)
    TokenERC20 public immutable rewardsToken;

    // Set the rewards token and nft collection addresses
    constructor(DropERC1155 spaceshipContractAddress, TokenERC20 gemsContractAddress) {
        spaceshipNftCollection = spaceshipContractAddress;
        rewardsToken = gemsContractAddress;
    }

    // Mapping player address to their current tools/resources
    struct MapValue {
        bool isData; // True when the NFT is staked
        uint256 value; // TokenID that is being staked by the user
    }

    mapping(address => MapValue) public playerSpaceship; // Players have no spaceship by default - they need to stake one to use it. `tokenId` of the spaceship is the multiplier for the reward (i.e. more advanced ships will increase the reward)
    mapping(address => MapValue) public playerLastUpdate; // Map address to last time stake/withdrew/claim transaction. Default -> player has no `lastTime` -> no mapping

    // Stake functionality
    function stake(uint256 _tokenId) external nonReentrant {
        require(spaceshipNftCollection.balanceOf(msg.sender, _tokenId) >= 1, "You need at least 1 spaceship of correct type to stake");

        if (playerSpaceship[msg.sender].isData) { // If user already has a spaceship [staked], send it back to them
            spaceshipNftCollection.safeTransferFrom(address(this), msg.sender, playerSpaceship[msg.sender].value, 1, "Returning your old Spaceship"); // Use safeTransfer to send spaceship back
        }

        uint256 reward = calculateRewards(msg.sender); // Calculate rewards owed to the player
        rewardsToken.transfer(msg.sender, reward); // Transfer reward tokens based on what's owed

        // Stake component
        spaceshipNftCollection.safeTransferFrom(msg.sender, address(this), _tokenId, 1, "Staking your spaceship"); // Transfer the spaceship (Still attached to `msg.sender`) to the [staking] contract

        // Update the spaceship mapping
        playerSpaceship[msg.sender].value = _tokenId;
        playerSpaceship[msg.sender].isData = true; // Currently being staked
        playerLastUpdate[msg.sender].isData = true; // Updating `lastUpdate` mapping for player
        playerLastUpdate[msg.sender].value = block.timestamp;
    }

    // Function to withdraw your spaceships from the staking vault
    function withdraw() external nonReentrant {
        require(playerSpaceship[msg.sender].isData, "You do not have a spaceship you can currently withdraw"); // Ensure user has something to withdraw before proceeding
        uint256 reward = calculateRewards(msg.sender);
        rewardsToken.transfer(msg.sender, reward);
        spaceshipNftCollection.safeTransferFrom(address(this), msg.sender, playerSpaceship[msg.sender].value, 1, "Returned spaceship to msg.sender");

        // Update spaceship mapping
        playerSpaceship[msg.sender].isData = false;
        playerLastUpdate[msg.sender].isData = true;
        playerLastUpdate[msg.sender].value = block.timestamp;
    }

    // Claim functionality
    function claim() external nonReentrant {
        // Calculate rewards owed and pay them out to the user
        uint256 reward = calculateRewards(msg.sender);
        rewardsToken.transfer(msg.sender, reward);

        // Update last update mapping
        playerLastUpdate[msg.sender].isData = true;
        playerLastUpdate[msg.sender].value = block.timestamp;
    }

    // Calculate rewards the player is owed
    function calculateRewards(address _player) public view returns (uint256 _rewards) { // 20,000,000/block | block.timestamp & playerLastUpdate
        if (!playerLastUpdate[_player].isData || !playerSpaceship[_player].isData) { // If player has no spaceship and has never been paid out
            return 0;
        }

        // Start calculating rewards IF `isData` is true
        uint256 timeDifference = block.timestamp - playerLastUpdate[_player].value; // Used to calculate the rewards owed to the player
        uint256 rewards = timeDifference * 10_000_000_000_000 * (playerSpaceship[_player].value + 1); // Equation/algo to calculate rewards owed based on tokenId

        return rewards;
    }
}