# WAM-Library-ETH

### Solidity requisites

#### WEB3:
library for interacting with ethereum, setting up connections and interacting with smart contracts

Visual 14 C++ needed
https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15
select visual studio build tools 2017, only the first optional checkbox (windows 10 sdk for desktop c++)

only then with pip
```
pip3 install --user web3                # (prod) 
```

#### Solidity Compiler:
solidity compiler for windows (solc) - based on https://www.codeooze.com/blockchain/solc-hello-world/

Combinations:
- (current)             solidity compiler 0.6.2 and Open Zeppelin 3.0.0 Beta
- (needs adaptation)    solidity compiler 0.5.10 and Open Zeppelin 2.5.0

get windows zip for solidity compiler from:
https://github.com/ethereum/solidity/releases
info:
https://solidity.readthedocs.io/en/v0.6.2/
https://solidity.readthedocs.io/en/v0.5.10/

get open zeppelin zip release from:
https://github.com/OpenZeppelin/openzeppelin-contracts/releases/
for direct lookup of contracts
https://github.com/OpenZeppelin/openzeppelin-contracts/releases/tag/v3.0.0-beta.0
https://github.com/OpenZeppelin/openzeppelin-contracts/releases/tag/v2.5.0

Install solidity compiler:
-extract to any folder, but advised to appdata/roaming/

install open zeppelin release: 
-extract to any folder
-copy contracts content
-paste in contracts folder of git repo/source/contracts

To use
-cd to folder in cmd
-compile by running:
```
solc -o C:\Users\mfvan\Documents\Git\Warband_Manager\source\ethereum\build\build0510\ --optimize --overwrite --bin --abi --ast --asm C:\Users\mfvan\Documents\Git\Warband_Manager\source\ethereum\CryptoCharacter0510.sol
solc -o C:\Users\mfvan\Documents\Git\Warband_Manager\source\ethereum\build\build062\ --optimize --overwrite --bin --abi --ast-json --asm C:\Users\mfvan\Documents\Git\Warband_Manager\source\ethereum\CryptoCharacter062.sol
# I packaged the dependencies (basically all openzeppelin contracts) in the contracts folder in my git.
```

The artifacts are then dropped in a build-version- folder in source\ethereum\build.
- abi: interface of the specific contract
- bin: bytecode of the specific contract
- evm: EVM Assembly / Opcodes
- sol.ast: 

Solidity Contracts Merger
We try to combine our contract with all its dependencies using Solidity Contracts Merger(vs code extention)
We need it as the compiler doesn't merge the outputs of the smart contracts to a single bytecode and abi
however the merged contract is not compilable

#### Openzeppelin default smart contracts
get solidity standards dependencies from openzeppelin:
https://github.com/OpenZeppelin/openzeppelin-contracts
Copy the contracts folder in whole, or just the files we are using (retaining the path):
- contracts/token/ERC721/IERC721.sol
- contracts/token/ERC721/IERC721Receiver.sol
- contracts/introspection/ERC165.sol
- contracts/math/SafeMath.sol
