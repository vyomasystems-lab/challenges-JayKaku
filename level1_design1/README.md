# Mux (31:1) Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![](../imgs/screenshot_gitpod_ctb_mux.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. 

## Test 1 (Sequential test for all valid inputs)
Values form 0 to 31 (inclusive) are applied on the `sel` while the respective `inp` = 1 i.e. set to active and the others are by default set to 0
 
 Code:
 ```
for i in range(0,31): 
  dut.inp{1}.value = 1
  dut.sel.value = i
```

The `if` statement is used for comparing the adder's outut to the expected value
```
  if(dut.out.value == 1) # i.e. out == inp{i}
      dut._log.info(...)
  else:
    errCount+=1
    dut._log.info(f'ERROR: ...')

 ```
## Test 2 (Invalid sel (select) input)

Value -3 was chosen as it translates to 1101 which out equal to inp29 in the mux design

Note: Verilog takes input of the negative numbers in two's complement form and hence -3 translates to 29

## Captured Bugs

## Test 1

![](../imgs/level1_design1_mux_bugs.png)

## Test 2

![](../imgs/level1_design1_mux_invalid_ip.png)

Note: Verilog takes input of the negative numbers in two's complement form and hence -3 translates to 29

## Test Scenario

## Test 1
### Scenario 1
- Test Inputs: inp12 = 1, sel = 12
- Expected Output: out = 1
- Observed Output in the DUT dut.out=0

### Scenario 2

- Test Inputs: inp30 = 1, sel = 20
- Expected Output: out = 1
- Observed Output in the DUT dut.out=0

## Test 2

- Test Inputs: inp{xx} = x, sel = -3
- Expected Output: out = 0
- Observed Output in the DUT dut.out=0

Note: Verilog takes input of the negative numbers in two's complement form and hence -3 translates to 29

## Design Bug
Based on the above test input and analysing the design, we see the following

```
  begin
    case(sel)
      5'b00000: out = inp0;  
      5'b00001: out = inp1;  
      5'b00010: out = inp2;  
      5'b00011: out = inp3;  
      5'b00100: out = inp4;  
      5'b00101: out = inp5;  
      5'b00110: out = inp6;  
      5'b00111: out = inp7;  
      5'b01000: out = inp8;  
      5'b01001: out = inp9;  
      5'b01010: out = inp10;
      5'b01011: out = inp11;
      5'b01101: out = inp12; <====== BUG wrong sel mapped to inp12
      5'b01101: out = inp13;
      5'b01110: out = inp14;
      5'b01111: out = inp15;
      5'b10000: out = inp16;
      5'b10001: out = inp17;
      5'b10010: out = inp18;
      5'b10011: out = inp19;
      5'b10100: out = inp20;
      5'b10101: out = inp21;
      5'b10110: out = inp22;
      5'b10111: out = inp23;
      5'b11000: out = inp24;
      5'b11001: out = inp25;
      5'b11010: out = inp26;
      5'b11011: out = inp27;
      5'b11100: out = inp28;
      5'b11101: out = inp29;
      <=== BUG missing case so the out=0 comes from default case ===>
      default: out = 0;
    endcase
  end
```

## Design Fix
Updating the design and re-running the test makes the test pass.

### Updated design

```
  begin
    case(sel)
      5'b00000: out = inp0;  
      5'b00001: out = inp1;  
      5'b00010: out = inp2;  
      5'b00011: out = inp3;  
      5'b00100: out = inp4;  
      5'b00101: out = inp5;  
      5'b00110: out = inp6;  
      5'b00111: out = inp7;  
      5'b01000: out = inp8;  
      5'b01001: out = inp9;  
      5'b01010: out = inp10;
      5'b01011: out = inp11;
      5'b01100: out = inp12; <== fix
      5'b01101: out = inp13;
      5'b01110: out = inp14;
      5'b01111: out = inp15;
      5'b10000: out = inp16;
      5'b10001: out = inp17;
      5'b10010: out = inp18;
      5'b10011: out = inp19;
      5'b10100: out = inp20;
      5'b10101: out = inp21;
      5'b10110: out = inp22;
      5'b10111: out = inp23;
      5'b11000: out = inp24;
      5'b11001: out = inp25;
      5'b11010: out = inp26;
      5'b11011: out = inp27;
      5'b11100: out = inp28;
      5'b11101: out = inp29;
      5'b11110: out = inp30; <== fix
      default: out = 0;
    endcase
  end
```
### Passed Test
![](../imgs/level1_design1_mux_fixed.png)

## Verification Strategy

The verification strategy was to test the mux against all the expected inputs and outputs as the combination design would instantly produced the output without the clock delay.

Loop was run to give i/p to the `sel` using iterator `i` while the respective active `inp{i}` was set to active.

Hence the each and every of the `inpxx` signals were tested with the respective `sel` signals and the `if out == inpxx` was checked.

## Is the verification complete ?

The verification is complete as the valid as well as invalid inputs have been tested against as well as the design has `default: out = 0;` for recovery from unknown cases also the `sensitivity list` has `sel` line only, as it as cobinational (which remove the cases of delayed outputs and states to an extent) design it can be claimed that the verification is indeed complete.