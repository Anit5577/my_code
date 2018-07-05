SUBROUTINE Transverse_Velocity !(Fname,Nsnaps,Nstars,Transvel)
  
   IMPLICIT NONE
   
   !f2py intent(in) fname,nsnaps,nstars
   !f2py intent(out) transvel

   INTEGER :: nsnaps, nstars
   INTEGER :: i,j,k          
   INTEGER :: snap(1:101,1:nstars)       
   INTEGER :: ids(1:101,1:nstars)
   DOUBLE PRECISION :: mass(1:101,1:nstars) 
   CHARACTER*35 :: fname
   REAL :: age(1:101,1:nstars)
   DOUBLE PRECISION :: rad(1:101,1:3,1:nstars) 
   DOUBLE PRECISION :: cod(1:101,1:3)
   DOUBLE PRECISION :: dist(1:101,1:3,1:nstars) 
   DOUBLE PRECISION :: sdist(1:101,1:nstars) 
   DOUBLE PRECISION :: dens(1:101,1:nstars)
   DOUBLE PRECISION :: nrad(0:101,1:3,1:nstars)
   DOUBLE PRECISION :: transvel(1:101,1:3,1:nstars)
   REAL :: pi

   INTEGER :: idlist(1:101,1:nstars)

   i=0
   j=0
   k=0
   age=0.
   dens=0.d0
   rad=0.d0
   snap=0
   ids=0
   mass=0.d0
   cod=0.d0
   nrad=0.d0
   transvel=0.d0
   sdist=0.d0
   idlist=0
   
   pi=3.1415926535897932

   WRITE(6,*) 'Choose data file to be read into array'
   READ(5,*) fname
   WRITE(6,*) 'Chosen data file is: ',fname
   
   OPEN(1,file=fname,status='old')
   
   nsnaps = 101
   
   DO i=1,nsnaps
      DO j=1,nstars
         READ(1,*) snap(i,j), age(i,j), ids(i,j), mass(i,j), rad(i,1:3,j)
         idlist(i,j)=j
      END DO
   END DO 
   
   DO i=1,nsnaps     
      CALL heapsort(nstars,real(ids(i,1:nstars)),idlist(i,1:nstars))      
   
      DO j=1,nstars

         transvel(i,1:3,idlist(i,j)) = rad(i,1:3,idlist(i,j)) - rad(i-1,1:3,idlist(i-1,j))    
         
      END DO
      
   END DO

   REWIND(1)   !use this when the program is called up as f2py subroutine

END SUBROUTINE Transverse_velocity
     
SUBROUTINE heapsort(psort,measureof,pwhichhas)

   IMPLICIT NONE
   INTEGER, INTENT(IN)  :: psort              ! number of values to be sorted.
   REAL,    INTENT(IN)  :: measureof(1:psort) ! values to be sorted.
   INTEGER, INTENT(OUT) :: pwhichhas(1:psort) ! identifier of value.
   INTEGER              :: rank               ! rank of value.
   INTEGER              :: ranknow            ! dummy rank.
   INTEGER              :: ranktest           ! dummy rank.
!
   DO rank=2,psort                ! THIS DO-LOOP BUILDS THE BINARY HEAP
     ranknow=rank
1    IF (ranknow==1) CYCLE
     ranktest=ranknow/2
     IF (measureof(pwhichhas(ranktest))>=measureof(pwhichhas(ranknow))) CYCLE
     CALL swapi(pwhichhas(ranknow),pwhichhas(ranktest))
     ranknow=ranktest
     GOTO 1
   END DO
!
   DO rank=psort,2,-1             ! AND THIS DO-LOOP INVERTS THE BINARY HEAP
     CALL swapi(pwhichhas(rank),pwhichhas(1))
     ranknow=1
2    ranktest=2*ranknow
     IF (ranktest>=rank) CYCLE
     IF ((measureof(pwhichhas(ranktest+1))>measureof(pwhichhas(ranktest))) &
                            & .AND.(ranktest+1<rank)) ranktest=ranktest+1
     IF (measureof(pwhichhas(ranktest))<=measureof(pwhichhas(ranknow))) CYCLE
     CALL swapi(pwhichhas(ranknow),pwhichhas(ranktest))
     ranknow=ranktest
     GOTO 2
   END DO
!
   END SUBROUTINE heapsort
!
!
   SUBROUTINE swapi(item1,item2)
!
   IMPLICIT NONE
   INTEGER :: item0,item1,item2
!
   item0=item1; item1=item2; item2=item0
!
   END SUBROUTINE swapi
