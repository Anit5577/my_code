   SUBROUTINE read_snapshots(snapreq,nf,filename,ns,nr,nsim,nmax,tunit,munit,runit,nroot)
! Redundant declarations at bottom - think about deleting
   USE parameters_mod
   USE phys_constants_mod
   USE extract_part_mod
   USE extract_track_mod
   use extract_stellar_ev_mod
   use extract_encounter_mod
   use close_encounter_mod
   use stellar_ev_mod
   IMPLICIT NONE
   INTEGER :: ns,nr,nf,nsim,nmax
   integer :: nroot(1:snapreq)
   INTEGER :: nss
   integer :: s
   integer, intent(in) :: snapreq
   DOUBLE PRECISION, INTENT(in) :: tunit,munit,runit
   CHARACTER*30 :: filename(100)
   CHARACTER*4 :: equals
   CHARACTER*50 :: descriptor
   CHARACTER*20 :: partname
   INTEGER :: j,ntot,multN,singident,nsing
   INTEGER :: i
   INTEGER :: ni,nsys
   INTEGER :: k
   integer :: mergeid  ! binary merger tag
   integer :: ijk

   mergeid=-1


   WRITE(6,*) 'accessing subroutine *read_snapshots*'
   WRITE(6,*) 'tunit = ',tunit,'munit = ',munit,'runit = ',runit
   WRITE(6,*) 'ns',ns,'nr',nr,'nf',nf
   write(6,*) 'nroots',nroot(1:snapreq)
   write(6,*) nsim,snapreq
!   pause

   OPEN(1,file=filename(nf),status='old')

   nss=0
   do s=1,snapreq

! Allocate particle extraction info
   ALLOCATE(m(1:nmax))
   ALLOCATE(r(1:3,1:nmax))
   ALLOCATE(v(1:3,1:nmax))
   m=0.d0
   r=0.d0
   v=0.d0
   ALLOCATE(ident(1:nmax))
   allocate(charident(1:nmax))
   ALLOCATE(totalm(1:nmax))
   ALLOCATE(totalr(1:3,1:nmax))
   ALLOCATE(totalv(1:3,1:nmax))
   ident=0
   charident='null'
   totalm=0.d0
   totalr=0.d0
   totalv=0.d0
   ALLOCATE(childof(1:nmax))
   ALLOCATE(sibling(1:nmax))
   ALLOCATE(nval(1:nmax))
   ALLOCATE(indivstar(1:nmax))
   ALLOCATE(done(1:nmax))
! Allocate stellar evolution extraction info
   allocate(esevstate(1:10,1:nmax))
   allocate(esevtime(1:10,1:nmax))
   allocate(esnkick(1:3,1:nmax))
   allocate(ensevstate(1:nmax))
   esevstate='main_sequence' 
   esevtime=0.d0
   esnkick=0.d0
   ensevstate=0
! allocate encounter extraction info
   allocate(eccname(1:nmax))
   allocate(ed2cc1(1:nmax))
   allocate(ed2cc(1:nmax))
   allocate(ecctime(1:nmax))
   allocate(epcccntr(1:nmax))
   allocate(epccname(1:nmax))
   allocate(epcctime(1:nmax))
   allocate(ecolltskip(1:nmax))
   eccname=0
   ed2cc1=0.d0
   ed2cc=0.d0
   ecctime=0.d0
   epcccntr=0
   epccname=0
   epcctime=0.d0
   ecolltskip=0.d0

!   nss=0

      DO
        READ(1,*,END=1) descriptor
!        write(6,*) descriptor
        IF (descriptor=='name') THEN
           BACKSPACE 1
           READ(1,*) descriptor,equals,partname
           IF (partname=='root') THEN 
              nsing=0
              nss=nss + 1
!              IF (nss==nr) THEN
              IF (nss==nroot(s)) THEN
                 DO
                   READ(1,*,END=2) descriptor
!                   write(6,*) descriptor
                   if (descriptor=='potential_energy') then
                      backspace 1
                      read(1,*) descriptor,equals,potenergy(nsim,snapreq)
                      read(1,*) descriptor,equals,kinenergy(nsim,snapreq)
                   end if
                   IF (descriptor==')Star') THEN
                      j=0  ! Sets the array counter to zero
                      DO
                         READ(1,*,END=3) descriptor                     ! Reads each line from the file
!                         READ(1,*) descriptor                     ! Reads each line from the file
                         IF (descriptor=='(Particle') THEN            ! if line begins '(Particle' then 
                            READ(1,*) descriptor                       ! it reads the next line 
                            IF (descriptor=='name') THEN             ! If next line begins 'name' then 
 ! ************************************************   this is a multiple particle
                               BACKSPACE 1                           ! rewinds file one line
                               READ(1,*) descriptor,equals,partname  ! reads name of particle
!write(6,*) descriptor,equals,partname
                               IF (partname=='root') then 
                                  write(6,*) ns,nss,nroot(s), 'breaking out to 4'
                                  backspace 1
                                  GOTO 4           ! snapshot is complete if partname=root
                               end if
 ! ************************************************ ! and so breaks out of loop to position 1
 !             WRITE(6,*) 'multiple particle - not root'
                               READ(1,*) descriptor,equals,multN     ! Reads next next line to get no. of particles 
                               j=j + 1                               ! increments array counter
                               nval(j)=multN                         ! put number of particles into tracking array(j)
!!              WRITE(6,*) 'nval = ',nval(j)!,multN
                               charident(j)=partname
                               ident(j)=0
!        ===== EXTRACT MULTIPLE PARTICLE INFORMATION ========
                               CALL read_particle(j,snapreq,s)
!             This subroutine extracts information from 'multiple particles' and places 
!             it into the respective arrays - m(j), r(1:3,j), v(1:3,j) and t(j)
!!              WRITE(6,*) 'Multiple particle information extracted.'
!              WRITE(6,*)''
                            ELSE IF (descriptor=='i') THEN           ! If next line begins 'i' then 
!!              WRITE(6,*) 'single particle'          ! this is a single particle
                               nsing=nsing + 1
                               BACKSPACE 1                           ! rewinds file one line
                               READ(1,*) descriptor,equals,singident ! reads next line to get single star indentifier
!              READ(1,*) descriptor,equals,id(j) ! reads next line to get single star indentifier
                               DO
!            This do loop accounts for a starlab bug - sometimes a single 
!            particle has three descriptors before (Log loop, sometimes 
!            only two....................................................
                                  READ(1,*) descriptor                 ! reads each line before the start of (Log 
                                  IF (descriptor=='(Log') EXIT         ! (Log tree open, so closes this Do loop                 
                               END DO
                               j=j + 1                               ! increments array counter
                               ident(j)=singident
                               if (ident(j)==0) pause
                               nval(j)=1                             ! sets number of particles in tracking array(j) to 1
!!              WRITE(6,*) 'nval = ',nval(j)!,multN
!        ===== EXTRACT SINGLE PARTICLE INFORMATION ==========
                               CALL read_particle(j,snapreq,s)
!             This subroutine extracts information from 'single particles' and places 
!             it into the respective arrays - m(j), r(1:3,j), v(1:3,j) and t(j)
!              WRITE(6,*) 'Single particle information extracted.'
!              WRITE(6,*)''
                            END IF          ! End of loop determing whether particle is multiple or single  
                         END IF              ! End of loop searching for open Particle - (Particle
                      END DO                 ! End of extraction Do loop
!
   WRITE(6,*) 'out of loop'    ! If the snapshot is fully extracted, end up here
                     ntot=j                      ! set total number of 'particles' to be length of array 
                      WRITE(6,*) 'ntot = ',ntot
                    END IF
                 END DO
              END IF
           END IF
        END IF
      END DO
1  stop 'read error 1'
2  stop 'read error 2'
3  write(6,*) 'completed reading?'
4  ntot=j
!   CLOSE(1)

WRITE(6,*) nss,nr,ntot,'nparticles',nsing,'   ',ns,s,nroot(s)
!pause

! This loop reconstructs the hierarchical tree. It searches the starlab hierarchy so that all the particles 
! "know" which other particles they are related too. This allows the user to obtain information on a single 
! star in a hierarchical system, and then realte that to the information describing the system itself. 
!
! 1 T        Eg, in this tree there are 5 particles (ntot = 5) from j = 1 to j=5. There is 'system' info
! 2   B      For the triple and the binary within this triple; and also 'star' info for single star and  
! 3     S    the stars that form the binary. All of this info is preserved using the following code...
! 4     S
! 5   S
!
    done=.FALSE.     ! Set a variable 'done' to be FALSE
    childof=0        ! All particles that are children of higher particles are 'childof'. Zero this array
    parent=0         ! All particles that are parents of lower particles are 'parent'. Zero this integer

!
    DO
       ncounter=0                              ! Set ncounter to be zero
       nfalse=0                                ! set number of 'false' occurrences to be zero
       DO j=1,ntot                             ! do from j=1 to ntot 
          IF (done(j)) CYCLE                   ! if value of j has been assigned a parent/child then cycle
          IF (ncounter==0) THEN                ! if ncounter is zero go into 'if' loop
              IF (nval(j)>1) ncounter=nval(j)  ! if particle is multiple then set ncounter to be number of 
! ********************************************   constituents in multiple particle
              parent=j                         ! set parent to be j
              done(j)=.TRUE.                   ! set flag 'done' to be true
          ELSE
          IF (nval(j)==1) ncounter=ncounter - 1 ! if single star, subtract 1 star from total number in system
          childof(j)=parent                     ! set this star's parent to be the last multiple system
          END IF                                ! end this loop
          IF (.NOT.done(j)) nfalse=nfalse + 1   ! if all parents/children not assigned then repeat loop
       END DO                                   ! end 'do' loop 
      IF (nfalse==0) EXIT                       ! exit loop when all parents/children have been assigned   
    END DO                                      ! end 'do' loop

! This loop assigns siblings to particles   
    DO j=1,ntot
       IF (childof(j)==0) CYCLE                 ! if there are no children, moves to next particle
       DO i=1,ntot
          IF (i==j) CYCLE                       ! sibling cant be a sibling with itself, so it cycles
          IF (childof(i)==childof(j)) THEN      ! if children have the same parent, it assigns them as 
             sibling(i)=j                       ! siblings
             sibling(j)=i
             EXIT                               ! exits when siblings are assigned
          END IF
       END DO
    END DO

! display parents, siblings and children in a table:
! Comment out if not required - do NOT delete - this helped me find merger stars
!    WRITE(6,*) 'particle number |', ' number of sub-particles |', ' parent |',' sibling'
!    DO j=1,ntot
!      WRITE(6,*) j,'   ',nval(j),'       ',childof(j),sibling(j),ident(j),charident(j),m(j)/munit
!      if (nval(j)==1 .and. ident(j)==0) pause
!    END DO

!pause

! ===== CONVERT FROM N-BODY UNITS =======================
! This section takes the N-body scaling units taken from the 
! extracted files and performs a units conversion to put the 
! units into pc, Myr, Myr pc^-1 and Msun
!
! This loop goes through each 'particle' stored in the array and performs 
! the appropriate unit scaling, converting from N-body units. It then also 
! converts velcoity from pc/Myr to km/s 
   DO j=1,ntot
!     t(j)=t(j)/tunit
     m(j)=m(j)/munit
     r(1:3,j)=r(1:3,j)*(2.255e-8/runit)  
     v(1:3,j)=v(1:3,j)*(2.255e-8/runit)*tunit
!
!  Convert from pc/Myr into km/s
     v(1:3,j)=v(1:3,j)*pc*1.e-9/yr

!     write(6,*) 'star = ',ident(j)
!     write(6,*) 'mass = ',m(j)
!     write(6,*) 'radi = ',r(1:3,j)
!     write(6,*) 'velo = ',v(1:3,j)

! do the same conversion for the encounter arrays
!     ed2cc1(j)=ed2cc(j)*(2.255e-8/runit)
!     ed2cc(j)=ed2cc(j)*(2.255e-8/runit)
     ed2cc1(j)=sqrt(ed2cc1(j))*(2.255e-8/runit)
     ed2cc(j)=sqrt(ed2cc(j))*(2.255e-8/runit)
     ecctime(j)=ecctime(j)/tunit
     epcctime(j)=epcctime(j)/tunit
     ecolltskip(j)=ecolltskip(j)/tunit
      
   END DO
!pause
! get the total (absolute) positions etc. and see if something is 
! a single star or a system
     indivstar=.FALSE.
     totalr=0.
     totalv=0.
     totalm=0.
! if nval is one this is a single star *not* a system or sub-system
     DO j=1,ntot
       IF (nval(j)==1) indivstar(j)=.TRUE.
     END DO
! now get the total values
     nsys=0
     DO j=1,ntot
! if this is a top level it's right already
       IF (childof(j)==0) THEN
         nsys=nsys + 1           ! count number of systems
         totalr(1:3,j)=r(1:3,j)
         totalv(1:3,j)=v(1:3,j)
         totalm(j)=m(j)
         CYCLE
       ELSE
! if it has a parent then add those values
         k=childof(j)        ! id of j's parent
         DO
           IF (k==0) EXIT    ! exit if top level
           totalr(1:3,j)=r(1:3,j) + r(1:3,k)
           totalv(1:3,j)=v(1:3,j) + v(1:3,k)
           totalm(j)=m(j)
           k=childof(k)
         END DO
       END IF
     END DO

! Simon's starfinder

! get a list of *individual* stars to work with (far easier)
! ni is total number of *individual* stars

   ni=0
   DO i=1,ntot
     IF (.NOT.indivstar(i)) CYCLE
     ni=ni + 1
!     id(ni)=ident(i)   ! record original identifier
     if (ident(i)==0) then
        write(6,*) charident(i)        
        do ijk=1,13
           write(6,*) charident(i)(1:ijk)
!           if (charident(i)(ijk:ijk)=='+') then 
           if (charident(i)(ijk:ijk)=='+' .or. charident(i)(ijk:ijk)=='<') then 
              write(6,*) (charident(i)(1:ijk-1))
              read(charident(i)(1:ijk-1),'(I6)') ident(i)
              write(6,*) 'mergeid',ident(i)
              exit
           end if
        end do
!        ident(i)=mergeid
!        mergeid=mergeid-1
     end if
     id(nsim,s,ni)=ident(i)   ! record original identifier
! give the particle a stellar evolution state (gives merger information)
     if (charident(i)=='null') then
        write(sevid(nsim,s,ni),'(I6)') ident(i)
     else
        sevid(nsim,s,ni)=charident(i)
        write(6,*) totalm(i)
     end if
!     write(6,*) id(ni)
     rad(nsim,s,1:3,ni)=totalr(1:3,i)
     vel(nsim,s,1:3,ni)=totalv(1:3,i)
     mass(nsim,s,ni)=totalm(i)
! place encounter information into arrays
     ccname(nsim,s,ni)=eccname(i)
     d2cc1(nsim,s,ni)=ed2cc1(i)
     d2cc(nsim,s,ni)=ed2cc(i)
     cctime(nsim,s,ni)=ecctime(i)
     pcccntr(nsim,s,ni)=epcccntr(i)
     pccname(nsim,s,ni)=epccname(i)
     pcctime(nsim,s,ni)=epcctime(i)
     colltskip(nsim,s,ni)=ecolltskip(i)

! place stellar evolution info in arrays
     if (s==snapreq) then
        sevstate(nsim,1:10,ni)=esevstate(1:10,i)
        sevtime(nsim,1:10,ni)=esevtime(1:10,i)
        snkick(nsim,1:3,ni)=esnkick(1:3,i)
        nsevstate(nsim,ni)=ensevstate(i)
     end if

!     WRITE(6,*) id(nsim,s,ni), mass(nsim,s,ni),rad(nsim,s,1:3,ni),vel(nsim,s,1:3,ni),ns,s,d2cc(nsim,s,ni)*pc/au,&
!          &d2cc1(nsim,s,ni)*pc/au,cctime(nsim,s,ni),pcctime(nsim,s,ni),ccname(nsim,s,ni),pccname(nsim,s,ni)
!     if (ident(i)==0) pause ! merger binaries
   END DO
   WRITE(6,*) ni,ns,nss
   nstar(nsim,s)=ni
   write(6,*) nstar(nsim,s)
   ntot=0


   DEALLOCATE(m)
   DEALLOCATE(r)
   DEALLOCATE(v)
   DEALLOCATE(ident)
   deallocate(charident)
   DEALLOCATE(totalm)
   DEALLOCATE(totalr)
   DEALLOCATE(totalv)
   DEALLOCATE(childof)
   DEALLOCATE(sibling)
   DEALLOCATE(nval)
   DEALLOCATE(done)
   DEALLOCATE(indivstar)
   deallocate(esevstate)
   deallocate(esevtime)
   deallocate(esnkick)
   deallocate(ensevstate) 
! deallocate encounter extraction info
   deallocate(eccname)
   deallocate(ed2cc1)
   deallocate(ed2cc)
   deallocate(ecctime)
   deallocate(epcccntr)
   deallocate(epccname)
   deallocate(epcctime)
   deallocate(ecolltskip)


   end do

   close(1)
!pause


   RETURN
   END SUBROUTINE read_snapshots

