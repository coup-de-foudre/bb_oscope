;* Required comment?

DEALY .set  49800		;
COUNT .set 10000       		;
	.asg "49800", DELAY  	;
	.asg "10000", COUNT	;

	.global doclock

doclock:
  LDI r1, DELAY         ; Setup the delay counter
  LDI r14, COUNT        ; Setup the cycle counter

MAINLOOP:
  CLR	r30, r30.t5	; set the clock to be low
  CLR	r30, r30.t5	; set the clock to be low -- to balance the duty cycle
  MOV	r0, r1		; load the delay r1 into temp r0 (50% duty cycle)

DELAYOFF:
  SUB	r0, r0, 1	; decrement the counter by 1 and loop (next line)
  QBNE	DELAYOFF, r0, 0	; loop until the delay has expired (equals 0)
  SET	r30, r30.t5	; set the clock to be high
  MOV	r0, r1		; re-load the delay r1 into temporary r0

DELAYON:
  SUB	r0, r0, 1	; decrement the counter by 1 and loop (next line)
  QBNE	DELAYON, r0, 0	; loop until the delay has expired (equals 0)

  SUB r14, r14, 1       ; Decrement the cycle counter
  QBNE MAINLOOP, r14, 0      ; Exit criteria

RET:
  JMP r3.w2             ; Return to the c++ scope

