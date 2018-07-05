SUBROUTINE Transverse_Velocity(Fname,Nsnaps,Nstars,Transvel)

   !f2py intent(in) fname,nsnaps,nstars
   !f2py intent(out) transvel
  
   IMPLICIT NONE
   
   INTEGER :: snap(1:101,1:Nstars)
   INTEGER :: ids(1:101,1:Nstars)
   DOUBLE PRECISION :: mass(1:101,1:Nstars) 
   INTEGER :: i,j
   INTEGER :: nsnaps,nstars
   CHARACTER*35 :: fname
   REAL :: age(1:101,1:Nstars)
   DOUBLE PRECISION :: rad(1:101,1:3,1:Nstars) 
   DOUBLE PRECISION :: transvel(1:101,1:3,1:Nstars)

   INTEGER :: idlist(1:101,1:Nstars)
   
   i=0
   j=0
   rad=0.d0
   snap=0
   ids=0
   mass=0.d0
   transvel=0.d0
   age=0.
   idlist=0
   
   OPEN(1,file=fname,status='old')
   
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

   REWIND(1)   

   END SUBROUTINE Transverse_Velocity
     
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
