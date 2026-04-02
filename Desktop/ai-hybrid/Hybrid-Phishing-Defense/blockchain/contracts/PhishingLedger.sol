// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PhishingLedger {
    
    struct PhishingRecord {
        bytes32 urlHash;
        uint256 timestamp;
        uint8 approvalCount;
        bool isConfirmed;
    }

    mapping(bytes32 => PhishingRecord) public records;
    mapping(address => bool) public validators;
    mapping(bytes32 => mapping(address => bool)) public hasVoted;
    
    uint8 public constant THRESHOLD = 2; 
    uint8 public validatorCount;

    event SuspectReported(bytes32 indexed urlHash, address reporter);
    event PhishingConfirmed(bytes32 indexed urlHash);

    modifier onlyValidator() {
        require(validators[msg.sender], "Access Denied: Not a Validator");
        _;
    }

    constructor() {
        validators[msg.sender] = true; 
        validatorCount = 1;
    }

    function addValidator(address _newValidator) external onlyValidator {
        require(!validators[_newValidator], "Already a validator");
        validators[_newValidator] = true;
        validatorCount++;
    }

    function reportPhishing(bytes32 _urlHash) external onlyValidator {
        PhishingRecord storage record = records[_urlHash];
        if (record.isConfirmed) return;

        if (record.timestamp == 0) {
            record.urlHash = _urlHash;
            record.timestamp = block.timestamp;
            record.approvalCount = 0;
            emit SuspectReported(_urlHash, msg.sender);
        }

        if (!hasVoted[_urlHash][msg.sender]) {
            hasVoted[_urlHash][msg.sender] = true;
            record.approvalCount++;

            if (record.approvalCount >= THRESHOLD) {
                record.isConfirmed = true;
                emit PhishingConfirmed(_urlHash);
            }
        }
    }

    function isBlacklisted(bytes32 _urlHash) external view returns (bool) {
        return records[_urlHash].isConfirmed;
    }
}