// SDPX-License-Identifier: MIT
pragma solidity ^0.8.11;
// Merge with `Spaceship.sol` -> this is just a slightly more advanced version for a test component on the frontend

// Import thirdweb contracts
import "@thirdweb-dev/contracts/drop/DropErc1155.sol"; // For the NFTs (include 721 later)
import "@thirdweb-dev/contracts/token/TokenERC20.sol"; // ERC-20 contrac

// OpenZeppelin Guards
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC1155/utils/ERC1155Holder.sol";

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
        require(spaceshipNftCollection.balanceOf(msg.sender, _toeknId) >= 1, "You need at least 1 spaceship of correct type to stake");

        if (playerSpaceship[msg.sender].isData) { // If user already has a spaceship, send it back to them
            
        }
    }

    // Calculate rewards the player is owed
    function calculateRewards(address _player) public view returns (uint256 _rewards) { // 20,000,000/block | block.timestamp & playerLastUpdate
        if (!playerLastUpdate[_player].isData || !playerSpaceship[_player].isData) { // If player has no spaceship and has never been paid out
            return 0;
        }

        uint256 timeDifference = block.timestamp - playerLastUpdate[_player].value; // Used to calculate the rewards owed to the player
        uint256 rewards = timeDifference * 10_000_000_000_000 * (playerSpaceship[_player].value + 1); // Equation/algo to calculate rewards owed based on tokenId

        return rewards;
    }
}