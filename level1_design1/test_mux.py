# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux(dut):
    """Sequential valid input test for mux2"""

    #cocotb.log.info('##### CTB: Develop your test here ########')

    errCount = 0
    errlog={}

    for i in range(0,31): 
        getattr(dut, 'inp%s'%i).value = 1 # evaluates to dut.inp{i}.value = 1
        dut.sel.value = i

        await Timer(2, units='ns')

        if(dut.out.value == 1):
            dut._log.info(f'sel={int(dut.sel.value):02} out={int(dut.out.value):02}')
        else:
            errCount+=1
            dut._log.info(f'ERROR: sel={int(dut.sel.value):02} out={int(dut.out.value):02} expected out = 1')

    
    #dut._log.info(f'sel={int(dut.sel.value):02} out={int(dut.out.value):02}')
    assert errCount == 0, "Randomised test failed {errCount} time/s respective errors logged".format(
        errCount=errCount)        


