;; * Required comment?

DEALY .set  49800	;
COUNT .set 1000	;
  .asg "49800", DELAY  	;
  .asg "1000", COUNT	;

  .global doclock

doclock:
  LDI r1, DELAY ; Setup the delay counter
  mov r15, r0   ; Setup the cycle counter (first argument)

MAINLOOP:
  CLR	r30, r30.t5	; set the clock to be low
  CLR	r30, r30.t5	; set the clock to be low -- to balance the duty cycle
  ldi	r1, DELAY	; load the delay r1 into temp r0 (50% duty cycle)

DELAYOFF:
  SUB	r1, r1, 1	; decrement the counter by 1 and loop (next line)
  QBNE	DELAYOFF, r1, 0	; loop until the delay has expired (equals 0)

  SET	r30, r30.t5	; set the clock to be high
  ldi	r1, DELAY	; re-load the delay r1 into temporary r0

DELAYON:
  SUB	r1, r1, 1	; decrement the counter by 1 and loop (next line)
  QBNE	DELAYON, r1, 0	; loop until the delay has expired (equals 0)

  SUB  r15, r15, 1       ; Decrement the cycle counter
  QBNE MAINLOOP, r15, 0  ; Exit criteria

RET:
  CLR r30, r30.t5	; set the clock to be low
  JMP r3.w2             ; Return to the c++ scope
