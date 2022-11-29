const hre = require('hardhat');

async function main() {
  const Medium = await hre.ethers.getContractFactory("Medium");
  const medium = await Medium.deploy("Medium Clone", "SJournal", "1000");

  await medium.deployed();
  console.log("Medium clone deployed to: ", medium.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });