// See LICENSE.vyoma for more details
// Verilog module for Sequence detection: 1011
module seq_detect_1011(seq_seen, inp_bit, reset, clk);

  output seq_seen;
  input inp_bit;
  input reset;
  input clk;

  parameter IDLE = 0,
            SEQ_1 = 1, 
            SEQ_10 = 2,
            SEQ_101 = 3,
            SEQ_1011 = 4;

  reg [2:0] current_state, next_state;

  // if the current state of the FSM has the sequence 1011, then the output is
  // high
  assign seq_seen = current_state == SEQ_1011 ? 1 : 0;

  // state transition
  always @(posedge clk)
  begin
    if(reset)
    begin
      current_state <= IDLE;
    end
    else
    begin
      current_state <= next_state;
    end
  end

  // state transition based on the input and current state
  always @(inp_bit or current_state)
  begin
    case(current_state)
      IDLE:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1; // 1
        else
          next_state = IDLE; // 0
      end
      SEQ_1:
      begin
        if(inp_bit == 1) // <==== Bug: edge case if inp= x or z invalid state change would happen, instead of 1 we need 0, with cases in ifelse switched
          next_state = IDLE; // 11
        else
          next_state = SEQ_10; //10
      end
      SEQ_10:
      begin
        if(inp_bit == 1)
          next_state = SEQ_101; // 101
        else
          next_state = IDLE; // 100
      end
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011; //1011
        else
          next_state = SEQ_10; //1010  <==== Bug, next_state shd be SEQ_10, modification need need to use elif here to handle for x & z
      end
      SEQ_1011:
      begin
        next_state = IDLE; // 1011 detected back to idle
      end
      //<=== BUG: missing default case ===> desing case with z or x value for it
    endcase
  end
endmodule
