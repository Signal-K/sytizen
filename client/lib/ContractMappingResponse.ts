import { BigNumber } from "ethers";

type ContractMappingResponse = {
    isData: boolean;
    value: BigNumber; // Represents uint256 value on the contract(s)
}

export default ContractMappingResponse;