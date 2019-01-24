; This is a PRU program to communicate to the ADS7883 SPI ADC ICs.
; Wiring as coded:
;   Chip Select (CS):	P9_27	 pr1_pru0_pru_r30_5  r30.t5
;   MISO	    :	P9_28	 pr1_pru0_pru_r31_3  r31.t3
;   CLK		    :	P9_30	 pr1_pru0_pru_r30_2  r30.t2
;   Sample Clock    :	P8_46	 pr1_pru1_pru_r30_1  -- for testing only

;;; Important Registers:
;;; r14 - Current write to address (arg 0)
;;; r15 - Stored byte countdown
;;; r16 - Sampled bytes countup
;;; r18 - Bit mask for 10 bit dataz
;;; r22 - SPI Bit read countdown
;;; r23 - Number of samples to be read
;;: r29 - Readout value from the ADC


DEALY_CYCLES .set  49800	    ;
TIME_CLOCK   .set  1	           ;
	.asg "49800", DELAY_CYCLES  ;
        .asg "1", TIME_CLOCK    ;


	.global dosampling

dosampling:
  ; r22 is the pointer to the next storage write location

  ; r15 is the number of bytes remaining to store
  mov r15, r15

  ; initialize the 10 bit mask constant
  ldi r18, 0x00000FFF

  ; initialize the dataspace for spi readout
  ldi r29, 0x00000000

  clr r30, r30.t2  ; set the clock low
	
GET_A_SAMPLE:
  clr r30, r30.t5  ; set the CS line low (active low)
  ldi r22, 16      ; going to write/read 16 bits (2 bytes)

SPICLK_BIT:	   ; loop for each of the 16 bits
  sub r22, r22, 1  ; count down through the bits
  jmp SPICLK       ; repeat call the SPICLK procedure until all 16 bits written/read

SPI_READ_RETURN:
  qbne SPICLK_BIT, r22, 0 ; have we performed 16 cycles?
	
  lsr r29, r29, 2      ; SPICLK shifts left too many times left, shift right once
  and r29, r29, r18    ; AND the data with mask to give only the 10 LSBs
  set r30, r30.t5      ; pull the CS line high (end of sample)

STORE_DATA:	            ; store the sample value in memory
  sbbo  &r29.w0, r14, 0, 2  ; store the value r29 in memory
  add   r14, r14, 2         ; shifting by 2 bytes - 2 bytes per sample

;;; Check to see if this was the last sample, if so break
  sub   r15, r15, 2	  ; reducing the number of samples - 2 bytes per sample
  qbeq  END, r15, 0       ; have taken the full set of samples

;;; TODO(meawoppl) replace with a more legitimate clock waiter etc.
DELAY_START:
  ldi r0, DELAY_CYCLES
DELAY:
  sub r0, r0, 1
  qbne DELAY, r0, 0

  qba GET_A_SAMPLE

;;; Return to the c++ stack
END:
  jmp r3.w2

; This procedure applies an SPI clock cycle to the SPI clock and on the rising edge of the clock
; it writes the current MSB bit in r2 (i.e. r31) to the MOSI pin. On the falling edge, it reads
; the input from MISO and stores it in the LSB of r3.
; The clock cycle is determined by the datasheet of the product where TIME_CLOCK is the
; time that the clock must remain low and the time it must remain high (assuming 50% duty cycle)
; The input and output data is shifted left on each clock cycle

SPICLK:
  lsl r29, r29, 1        ; shift the captured data left by one position
  ldi r0, TIME_CLOCK	 ; time for clock low -- assuming clock low before cycle

CLKLOW:
  sub  r0, r0, 1	 ; decrement the counter by 1 and loop (next line)
  qbne CLKLOW, r0, 0	 ; check if the count is still low

  set  r30, r30.t2           ; set the clock high
  qbbc DATAINLOW, r31, 3     ; check if the bit that is read in is low? jump
  or   r29, r29, 0x00000001  ; set the stored bit LSB to 1 otherwise

DATAINLOW:
  ; Clock goes high for a time period
  ldi  r0, TIME_CLOCK	 ; time for clock high

CLKHIGH:
  sub  r0, r0, 1	 ; decrement the counter by 1 and loop (next line)
  qbne CLKHIGH, r0, 0	 ; check the count
  clr  r30, r30.t2	 ; set the clock low
  jmp SPI_READ_RETURN
