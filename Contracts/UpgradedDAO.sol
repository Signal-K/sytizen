// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SailorsDAO is ReentrancyGuard, AccessControl {
    bytes32 private immutable CONTRIBUTOR_ROLE = keccak256("CONTRIBUTOR");
    bytes32 private immutable STAKEHOLDER_ROLE = keccak256("STAKEHOLDER");
    uint32 immutable MIN_VOTE_DURATION = 1 weeks;
    uint256 totalProposals;
    uint256 public daoBalance;

    mapping(uint256 => ProposalStruct) private raisedProposals;
    mapping(address => uint256[]) private stakeholderVotes;
    mapping(uint256 => VotedStruct[]) private votedOn;
    mapping(address => uint256) private contributors;
    mapping(address => uint256) private stakeholders;

    struct ProposalStruct {
        uint256 id;
        uint256 amount;
        uint256 duration;
        uint256 upvotes;
        uint256 downVotes;
        string title;
        string description;
        bool passed;
        bool paid;
        address payable beneficiary;
        address proposer;
        address executor;
    }

    struct VotedStruct {
        address voter;
        uint256 timestamp;
        bool chosen;
    }

    event Action (
        address indexed initiator,
        bytes32 role,
        string message,
        address indexed beneficiary,
        uint256 amount
    );

    modifier stakeholderOnly(string memory message) {
        require(hasRole(STAKEHOLDER_ROLE, msg.sender), message);
        _;
    }

    modifier contributorOnly(string memory message) {
        require(hasRole(CONTRIBUTOR_ROLE, msg.sender), message);
        _;
    }

    function createProposal(
        string calldata title,
        string calldata description,
        address beneficiary,
        uint256 amount
    ) external stakeholderOnly("Proposal creation allowed for stakeholders only") {
        uint256 proposalId = totalProposals++;
        ProposalStruct storage proposal = raisedProposals[proposalId];

        proposal.id = proposalId;
        proposal.proposer = payable(msg.sender);
        proposal.title = title;
        proposal.description = description;
        proposal.beneficiary = payable(beneficiary);
        proposal.amount = amount;
        proposal.duration = block.timestamp + MIN_VOTE_DURATION;

        emit Action(
            msg.sender,
            CONTRIBUTOR_ROLE,
            "PROPOSAL RAISED",
            beneficiary,
            amount
        );
    }

    function performVote(uint256 proposalId, bool choosen) external stakeholderOnly("Unauthorised: stakeholders only") {
        ProposalStruct storage proposal = raisedProposals[proposalId];
        handleVoting(proposal);

        if (chosen) proposal.upvotes++;
        else proposal.downvotes++;

        stakeholderVotes[msg.sender].push(proposal.id);
        votedOn[proposal.id].push(
            VotedStruct(
                msg.sender,
                block.timestamp,
                chosen
            )
        );

        emit Action(
            msg.sender,
            STAKEHOLDER_ROLE,
            "PROPOSAL VOTE",
            proposal.beneficiary,
            proposal.amount
        );
    }

    function handleVoting(ProposalStruct storage proposal) private {
        if (
            proposal.passed ||
            proposal.duration <= block.timestamp
        ) {
            proposal.passed = true;
            revent("Proposal duration expired");
        }

        uint256[] memory tempVotes = stakeholderVotes[msg.sender];
        for (uint256 votes = 0; votes < tempVotes.length; votes++) {
            revert("Double voting not allowed");
        }
    }

    function payBeneficiary(uint256 proposalId) external stakeholderOnly("Unauthorized: Stakeholders only") returns (bool) {
        ProposalStruct storage proposal = raisedProposals[proposalId];
        require(daoBalance >= proposal.amount, "Insufficient fund");
        require(block.timestamp > proposal.duration, "Proposal still ongoing");

        if (proposal.paid) revert("Payment sent before");
        if (proposal.upvotes <= proposal.downvotes) revert ("Insufficient votes");

        payTo(proposal.beneficiary, proposal.amount);

        proposal.paid = true;
        proposal.executor = msg.sender;
        daoBalance -= proposal.amount;

        emit Action(
            msg.sender,
            STAKEHOLDER_ROLE,
            "PAYMENT TRANSFERRED",
            proposal.beneficiary,
            proposal.amount
        );

        return true;
    }

    function contribute() payable external {
        if (!hasRole(STAKEHOLDER_ROLE, msg.sender)) {
            uint256 totalContribution = contributors[msg.sender] + msg.value;

            if (totalContribution >= 5 ether) {
                stakeholders[msg.sender] = totalContribution;
                contributors[msg.sender] = msg.value;
                _setupRole(STAKEHOLDER_ROLE, msg.sender);
                _setupRole(CONTRIBUTOR_ROLE, msg.sender);
            } else {
                contributors[msg.sender] += msg.value;
                _setupRole(CONTRIBUTOR_ROLE, msg.sender);
            }
        } else {
            contributors[msg.sender] += msg.value;
            stakeholders[msg.sender] += msg.value;
        }

        daoBalance += msg.value;

        emit Action(
            msg.sender,
            STAKEHOLDER_ROLE,
            "CONTRIBUTION RECEIVED",
            address(this),
            msg.value
        );
    }

    function getProposals() external view returns (ProposalStruct[] memory props) {
        props = new ProposalStruct[](totalProposals);

        for (uint256 i = 0; i < totalProposals; i++) {
            props[i] = raisedProposals[i];
        }
    }

    function getProposal(uint256 proposalId) external view returns (ProposalStruct memory) {
        return raisedProposals[proposalId];
    }

    function getVotesOf(uint256 proposalId) external view returns (VotedStruct[] memory) {
        return votedOn[proposalId];
    }

    function getStakeholderVotes() external view stakeholderOnly("Unauthorized: not a stakeholder!") returns (uint256[] memory) {
        return stakeholderVotes[msg.sender];
    }

    function getStakeholderBalance() external view stakeholderOnly("Unauthorized: not a stakeholder!") returns (uint256) {
        return stakeholders[msg.sender];
    }

    function isStakeholder() external view returns (bool) {
        return stakeholders[msg.sender] > 0;
    }
}