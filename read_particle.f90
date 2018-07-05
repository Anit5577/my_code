   SUBROUTINE read_particle(j,snapreq,ns)
! This subroutine extracts information from 'particles' and places 
! it into the respective temporary arrays - m(j), r(1:3,j) and v(1:3,j)
!
! ========= DECLARATIONS ===============
! Uses various modules found in 'analysis_modules.f90'
! Redunadant declarations at bottom
   USE extract_part_mod
   use extract_stellar_ev_mod
   use extract_encounter_mod
   IMPLICIT NONE
   INTEGER :: j!,nmax,k
   integer, intent(in) :: snapreq,ns
   CHARACTER*4 :: equals
   CHARACTER*50 :: descriptor
   character*20 :: desc_library(1:10)
   integer :: n,ndesc
   character*20 :: ccname_dummy
   integer :: ijk
!
   desc_library(1)='cc_name'
   desc_library(2)='d2cc_1'
   desc_library(3)='d2cc'
   desc_library(4)='cc_time'
   desc_library(5)='pcc_cntr'
   desc_library(6)='pcc_name'
   desc_library(7)='pcc_time'
   desc_library(8)='coll_tskip'
   ndesc=8
! ======= END OF DECLARATIONS ==========
!
! Start of subroutine
! (Log tree opened
! This do loop runs through the Log information, extracting anything 
! that is needed by the user. The Log loop has already been opened 
! in the 'read_sl_out' (parent) subroutine
   DO
     READ(1,*) descriptor            ! reads each line in the loop
! extract encounter information, if applicable
     if (descriptor=='cc_name') then
        backspace 1
!        read(1,*) descriptor,equals,eccname(j)
        read(1,*) descriptor,equals,ccname_dummy
        do ijk=1,13
           if (ccname_dummy(ijk:ijk)=='+' .or. ccname_dummy(ijk:ijk)=='<') then 
              write(6,*) (ccname_dummy(1:ijk-1))
              read(ccname_dummy(1:ijk-1),'(I6)') eccname(j)
              write(6,*) 'merge close encounter id (cc name)',eccname(j)
              exit
           else
              read(ccname_dummy(1:ijk),'(I6)') eccname(j)
           end if
        end do
!        write(6,*) 'close encounter id',eccname(j)
     else if (descriptor=='d2cc_1') then
        backspace 1
        read(1,*) descriptor,equals,ed2cc1(j)
!        write(6,*) descriptor,equals,ed2cc1(j)
     else if (descriptor=='d2cc') then
        backspace 1
        read(1,*) descriptor,equals,ed2cc(j)
!        write(6,*) descriptor,equals,ed2cc(j)
     else if (descriptor=='cc_time') then
        backspace 1
        read(1,*) descriptor,equals,ecctime(j)
!        write(6,*) descriptor,equals,ecctime(j)
     else if (descriptor=='pcc_cntr') then
        backspace 1
        read(1,*) descriptor,equals,epcccntr(j)
!        write(6,*) descriptor,equals,epcccntr(j)
     else if (descriptor=='pcc_name') then
        backspace 1
!        read(1,*) descriptor,equals,epccname(j)
        read(1,*) descriptor,equals,ccname_dummy
        do ijk=1,13
           if (ccname_dummy(ijk:ijk)=='+' .or. ccname_dummy(ijk:ijk)=='<') then 
              write(6,*) (ccname_dummy(1:ijk-1))
              read(ccname_dummy(1:ijk-1),'(I6)') epccname(j)
              write(6,*) 'merge close encounter id (pcc_name)',epccname(j)
              exit
           else
              read(ccname_dummy(1:ijk),'(I6)') epccname(j)
           end if
        end do
!        write(6,*) descriptor,equals,epccname(j)
     else if (descriptor=='pcc_time') then
        backspace 1
        read(1,*) descriptor,equals,epcctime(j)
!        write(6,*) descriptor,equals,epcctime(j)
     else if (descriptor=='coll_tskip') then
        backspace 1
        read(1,*) descriptor,equals,ecolltskip(j)
!        write(6,*) descriptor,equals,ecolltskip(j)
     end if
    
     if (ns==snapreq) then
        do n=1,ndesc
           if (descriptor==desc_library(n)) then 
!              write(6,*) 'exit descript check loop'
              goto 1
           end if
        end do
        if (descriptor.ne.')Log' .and. descriptor.ne.'(Log' .and. descriptor.ne.'v_kick') then
           backspace 1
           ensevstate(j)=ensevstate(j) + 1
           read(1,*) esevstate(ensevstate(j),j),equals,esevtime(ensevstate(j),j)
           write(6,*) esevstate(ensevstate(j),j),equals,esevtime(ensevstate(j),j),ident(j),snapreq
        else if (descriptor=='v_kick') then
              backspace 1
              read(1,*) descriptor,equals,esnkick(1:3,j)
              write(6,*) descriptor,equals,esnkick(1:3,j),ident(j),snapreq
        end if
     end if
1    IF (descriptor==')Log') EXIT    ! exits at end of loop - )Log
   END DO
! close )Log loop
!
!  ======= EXTRACT DYNAMICAL INFORMATION =============================
   READ(1,*) descriptor           ! open (Dynamics
! This do loop runs through the Dynamics information to extract the 
! information and put it into the respective arrays - m(j), r(1:3,j), 
! v(1:3,j) and t(j)
   DO
      READ(1,*) descriptor 
     IF (descriptor=='m') THEN           ! if line is 'm'
        BACKSPACE 1                      ! rewind the file one line
        READ(1,*) descriptor,equals,m(j) ! read in stellar mass
     END IF
     IF (descriptor=='r') THEN                           ! if line is 'r'
        BACKSPACE 1                                      ! rewind the file one line
        READ(1,*) descriptor,equals,r(1,j),r(2,j),r(3,j) ! read in star's position
     END IF 
     IF (descriptor=='v') THEN                           ! if line is 'v'
        BACKSPACE 1                                      ! rewind the file one line
        READ(1,*) descriptor,equals,v(1,j),v(2,j),v(3,j) ! read in star's velocity
     END IF
!     write(6,*) descriptor        
     IF (descriptor==')Dynamics') EXIT ! close )Dynamics and exit loop
   END DO

! Dynamics closed
!
! ========= EXTRACT HYDRO INFORMATION ================================
   READ(1,*) descriptor             ! open hydro tree
! This do loop runs through the Hydro information, extracting anything 
! that is needed by the user
   DO
     READ(1,*) descriptor           ! reads each line in loop
     IF (descriptor==')Hydro') EXIT ! exits at end of loop - )Hydro
   END DO
!  hydro tree closed
!
! ========= EXTRACT STAR INFORMATION =================================
   READ(1,*) descriptor            ! open star tree
! This do loop runs through the Star information, extracting anything 
! that is needed by the user
   DO
     READ(1,*) descriptor          ! reads each line in loop
     IF (descriptor==')Star') EXIT ! exits at end of loop - )Star
   END DO
! star tree closed
!
!   write(6,*) 'close encounter id',eccname(j)

   RETURN
!
   END SUBROUTINE read_particle

!   double precision, intent(out) :: m(1000)
!   double precision, intent(out) :: v(1:3,1000)
!   double precision, intent(out) :: r(1:3,1000)
