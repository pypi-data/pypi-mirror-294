## 3.0.0 (2024-09-05)

### BREAKING CHANGE

- upgrade to PowerFactory 2024 (#263)

### Feat

- extend interface for current and voltage sources (#259)
- extend interface for shunts (#258)
- extend export and import functions and move them to utils.io (#245)
- export optional element data as meta dict (#251)
- extend element selection by filter 'out_of_service' (contributors: @SebastianDD)
- supporting multiple PowerFactory versions (contributors: @sasanjac, @SebastianDD)
- properly mapping `system_type` for loads (contributors: @SebastianDD)
- add PowerFactory ErrorCode Description (contributors: @SebastianDD)
- extend PFTypes with LV and MV Load Types and consider LoadModel for LoadLV (contributors: @SebastianDD, @sasanjac)

### Fix

- update example grids to PF 2024 (#270)
- ipynb examples (#272)
- unique name for multiple nested substation nodes and correct names for lv-loads in topology case (#242)
- line length (#237)
- create warning message for empty LV loads (contributors: @SebastianDD, @sasanjac)
- use PF error codes for application startup (contributors: @SebastianDD)
- multiline description of loads/lv-loads not correctly exported (contributors: @SebastianDD)
- use I-type load model for LV-Loads as default instead of Z-type (contributors: @SebastianDD)
- creation of grid variants (contributors: @SebastianDD)

[main dcbcf64] bump: version 2.1.0 → 3.0.0
 6 files changed, 38 insertions(+), 8 deletions(-)

