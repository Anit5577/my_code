   SUBROUTINE read_ic(snapreq,nf,filename,ns,nr,nsim,nmax,tunit,munit,runit,ni)
! Redundant declarations at bottom - think about deleting
   USE parameters_mod
   USE phys_constants_mod
   USE extract_part_mod
   USE extract_track_mod
   IMPLICIT NONE
   INTEGER :: ns,nr,nf,nsim,nmax
   INTEGER :: nss
   DOUBLE PRECISION, INTENT(in) :: tunit,munit,runit
   integer, intent(in) :: snapreq
   CHARACTER*30 :: filename(100)
   CHARACTER*4 :: equals
   CHARACTER*40 :: descriptor
   CHARACTER*20 :: partname
   INTEGER :: j,ntot,multN,singident,nsing
   INTEGER :: i
   INTEGER :: ni,nsys
   INTEGER :: k

   WRITE(6,*) 'accessing subroutine *read_ic*'
   WRITE(6,*) 'tunit = ',tunit,'munit = ',munit,'runit = ',runit
   WRITE(6,*) 'ns',ns,'nr',nr,'nf',nf,'nsim',nsim,'snapreq',snapreq

   ALLOCATE(m(1:nmax))
   ALLOCATE(r(1:3,1:nmax))
   ALLOCATE(v(1:3,1:nmax))
   m=0.d0
   r=0.d0
   v=0.d0
   ALLOCATE(ident(1:nmax))
   ALLOCATE(totalm(1:nmax))
   ALLOCATE(totalr(1:3,1:nmax))
   ALLOCATE(totalv(1:3,1:nmax))
   ident=0
   totalm=0.d0
   totalr=0.d0
   totalv=0.d0
   ALLOCATE(childof(1:nmax))
   ALLOCATE(sibling(1:nmax))
   ALLOCATE(nval(1:nmax))
   ALLOCATE(indivstar(1:nmax))
   ALLOCATE(done(1:nmax))


   nss=0
   OPEN(1,file=filename(nf),status='old')
      DO
        READ(1,*,END=1) descriptor
!        write(6,*) descriptor
        IF (descriptor=='name') THEN
           BACKSPACE 1
           READ(1,*) descriptor,equals,partname
           IF (partname=='root') THEN 
              nsing=0
              nss=nss + 1
              IF (nss==nr) THEN
                 DO
                   READ(1,*,END=1) descriptor
  !                 write(6,*) descriptor
                   IF (descriptor==')Star') THEN
                      j=0  ! Sets the array counter to zero
                      DO
                         READ(1,*,END=1) descriptor                     ! Reads each line from the file
                         IF (descriptor=='(Particle') THEN            ! if line begins '(Particle' then 
                            READ(1,*) descriptor                       ! it reads the next line 
                            IF (descriptor=='name') THEN             ! If next line begins 'name' then 
 ! ************************************************   this is a multiple particle
                               BACKSPACE 1                           ! rewinds file one line
                               READ(1,*) descriptor,equals,partname  ! reads name of particle
                               IF (partname=='root') GOTO 1           ! snapshot is complete if partname=root
 ! ************************************************ ! and so breaks out of loop to position 1
 !             WRITE(6,*) 'multiple particle - not root'
                               READ(1,*) descriptor,equals,multN     ! Reads next next line to get no. of particles 
                               j=j + 1                               ! increments array counter
                               nval(j)=multN                         ! put number of particles into tracking array(j)
!!              WRITE(6,*) 'nval = ',nval(j)!,multN
                               ident(j)=0
!        ===== EXTRACT MULTIPLE PARTICLE INFORMATION ========
                               CALL read_particle(j,snapreq,ns)
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
                               nval(j)=1                             ! sets number of particles in tracking array(j) to 1
!!              WRITE(6,*) 'nval = ',nval(j)!,multN
!        ===== EXTRACT SINGLE PARTICLE INFORMATION ==========
                               CALL read_particle(j,snapreq,ns)
!             This subroutine extracts information from 'single particles' and places 
!             it into the respective arrays - m(j), r(1:3,j), v(1:3,j) and t(j)
!              WRITE(6,*) 'Single particle information extracted.'
!              WRITE(6,*)''
                            END IF          ! End of loop determing whether particle is multiple or single  
                         END IF              ! End of loop searching for open Particle - (Particle
                      END DO                 ! End of extraction Do loop
!
!   WRITE(6,*) 'out of loop'    ! If the snapshot is fully extracted, end up here
                     ntot=j                      ! set total number of 'particles' to be length of array 
!                      WRITE(6,*) 'ntot = ',ntot
                    END IF
                 END DO
              END IF
           END IF
        END IF
      END DO
!   CLOSE(1)
1  ntot=j
   CLOSE(1)
!WRITE(6,*) 'yo',nss,nr,ntot,'nparticles',nsing

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
! Comment out or delete this if not required
!    WRITE(6,*) 'particle number |', ' number of sub-particles |', ' parent |',' sibling'
!    DO j=1,ntot
!      WRITE(6,*) j,'   ',nval(j),'       ',childof(j),sibling(j)
!    END DO

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
   END DO

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
     iid(nsim,ni)=ident(i)   ! record original identifier
!     write(6,*) id(ni)
     irad(nsim,1:3,ni)=totalr(1:3,i)
     ivel(nsim,1:3,ni)=totalv(1:3,i)
     imass(nsim,ni)=totalm(i)
!     write(6,*) id(ni), mass(ni)
!     WRITE(6,*) iid(nsim,ni), imass(nsim,ni), irad(nsim,1:3,ni), ivel(nsim,1:3,ni)
   END DO
!   WRITE(6,*) ni


   DEALLOCATE(m)
   DEALLOCATE(r)
   DEALLOCATE(v)
   DEALLOCATE(ident)
   DEALLOCATE(totalm)
   DEALLOCATE(totalr)
   DEALLOCATE(totalv)
   DEALLOCATE(childof)
   DEALLOCATE(sibling)
   DEALLOCATE(nval)
   DEALLOCATE(done)
   DEALLOCATE(indivstar)



   RETURN
   END SUBROUTINE read_ic

