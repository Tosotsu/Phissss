require("@nomiclabs/hardhat-ethers");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.18", // Matches the version in your contract
  networks: {
    localhost: {
      url: "http://127.0.0.1:7545",
      // Hardhat will automatically use the first account from Ganache
    }
  }
};