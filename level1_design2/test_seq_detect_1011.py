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
async def test_seq_bug(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    # to check for non-sequence overlap
    #inp = [1,1,1,0,1,1,1,1]
    
    # to expose the 1010 state change bug where the pattern doesn't get recognized in the og design
    inp = [1,0,1,0,1,1,1,1]
    
    dut._log.info(f'current_state={int(dut.current_state.value)}')

    string=""
    seen_count = 0

    for i in inp:
        string+= str(i)
        dut.inp_bit.value = i

        await Timer(10, units='us')

        matchedArr = re.findall("1011",string)
        
        if(int(dut.seq_seen.value)==1):
            seen_count+=1
        
        dut._log.info(f'clk={int(dut.clk.value)} rstn={int(dut.reset.value)} inp_bit={dut.inp_bit.value} seq_seen={int(dut.seq_seen.value):02} current_state={int(dut.current_state.value)}')
        assert seen_count == len(matchedArr), "ERROR: Sequence mismatch, expected seq_seen={EXPECTED_SEQ} instead got seq_seen={SEQ_SEEN}".format(EXPECTED_SEQ=len(matchedArr),SEQ_SEEN=int(dut.seq_seen.value))



@cocotb.test()
async def test_invalid_ip_bug(dut):
    """Invalid input 1z11 instead of 1011, leading to valid state and incorrect seq match"""

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    dut.next_state.value = 0
    await Timer(10, units='us')
    
    # to verify z or x edge case logic for SEQ_1 if else bug 
    inp = [1,1,1,cocotb.types.Logic("Z"),1,1,1,1]

    string=""
    seen_count = 0

    for i in inp:
        string+= str(i)
        dut.inp_bit.value = i

        await Timer(10, units='us')

        matchedArr = re.findall("1011",string)
        
        if(int(dut.seq_seen.value)==1):
            seen_count+=1
        

        dut._log.info(f'clk={int(dut.clk.value)} rstn={int(dut.reset.value)} inp_bit={dut.inp_bit.value} seq_seen={int(dut.seq_seen.value):02} current_state={int(dut.current_state.value)}')

        assert seen_count == len(matchedArr), "ERROR: Sequence mismatch, expected seq_seen={EXPECTED_SEQ} instead got seq_seen={SEQ_SEEN}".format(EXPECTED_SEQ=len(matchedArr),SEQ_SEEN=int(dut.seq_seen.value)) 



# internal state change test keep run independently
@cocotb.test()
async def test_invalid_curr_state_bug(dut):
    """ Changing next_state to invalid state to check how the design recovers in that case """
    
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    dut._log.info(f'current_state={int(dut.current_state.value)}')
    
    dut.next_state.value = 5

    for i in range(5):
        await Timer(10, units='us')

        dut._log.info(f'clk={int(dut.clk.value)} rstn={int(dut.reset.value)} inp_bit={dut.inp_bit.value} seq_seen={int(dut.seq_seen.value):02} current_state={int(dut.current_state.value)}')
    
    assert int(dut.current_state.value) < 5 , "ERROR: Invalid current_state={CURR_STATE}, deadlock".format(CURR_STATE=int(dut.current_state.value))
    
    
