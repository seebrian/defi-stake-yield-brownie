pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract HappyToken is ERC20 {
    constructor() public ERC20("Happy Token", "HAPPY") {
        _mint(msg.sender, 1000000000000000000000000);
    }
}
