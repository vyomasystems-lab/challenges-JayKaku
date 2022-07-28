# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0
import re
import os
import random
from pathlib import Path
from cocotb.triggers import Timer

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    cocotb.log.info('#### CTB: Develop your test here! ######')

    # to check for non-sequence overlap
    # inp = [1,1,1,0,1,1,1,1]
    
    # to verify z or x edge case logic for SEQ_1 if else bug 
    inp = [1,1,1,cocotb.types.Logic("Z"),1,1,1,1]

    
    # to expose the 1010 state change bug where the pattern doesn't get recognized in the og design
    #inp = [1,0,1,0,1,1,1,1]
    string=""

    for i in inp:
        string+= str(i)
        dut.inp_bit.value = i
        await Timer(10, units='us')

        check = re.findall("1011",string)

        dut._log.info(f'clk={int(dut.clk.value)} rstn={int(dut.reset.value)} inp_bit={int(dut.inp_bit.value)} seq_seen={int(dut.seq_seen.value):02}')
        assert dut.seq_seen.value == check, "Error"

    

    
