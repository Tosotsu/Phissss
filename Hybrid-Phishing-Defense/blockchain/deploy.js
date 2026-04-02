const { ethers } = require("hardhat"); // Or standard ethers.js setup

async function main() {
    console.log("Deploying PhishingLedger contract...");

    // 1. Get the Contract Factory
    const PhishingLedger = await ethers.getContractFactory("PhishingLedger");
    
    // 2. Deploy
    const ledger = await PhishingLedger.deploy();
    await ledger.deployed();

    console.log("------------------------------------------------");
    console.log("✅ Contract Deployed Successfully!");
    console.log("📍 Contract Address:", ledger.address);
    console.log("------------------------------------------------");
    console.log("IMPORTANT: Copy this address into backend/app.py");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });