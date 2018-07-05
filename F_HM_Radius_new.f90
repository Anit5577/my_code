SUBROUTINE Half_Mass__Radius(Fname,Nsnaps,Nstars,Hmrad)
  
   IMPLICIT NONE
   INTEGER :: snap(1:101,1:1000)
   INTEGER :: ids(1:101,1:1000)
   DOUBLE PRECISION :: mass(1:101,1:1000)
   DOUBLE PRECISION :: cmass(1:101,1:1000) 
   DOUBLE PRECISION :: halfmass(1:101,1:1000)
   DOUBLE PRECISION :: snapmass(1:101,1:1000)
   INTEGER :: i,j,k
   INTEGER :: nsnaps,nstars
   CHARACTER*35 :: fname
   REAL :: age(1:101,1:1000)
   DOUBLE PRECISION :: rad(1:101,1:3,1:1000) 
   DOUBLE PRECISION :: cod(1:101,1:3)
   DOUBLE PRECISION :: dist(1:101,1:3,1:1000) 
   DOUBLE PRECISION :: sdist(1:101,1:1000) 
   DOUBLE PRECISION :: dens(1:101,1:1000)
   DOUBLE PRECISION :: codrad(1:101,1:3,1:1000)
   DOUBLE PRECISION :: radval(1:101,1:1000) 
   DOUBLE PRECISION :: hmrad(1:101) 
   REAL :: hmdif(1:101,1:1000)
   
   REAL :: pi

   INTEGER :: dlist(1:101,1:1000)
   INTEGER :: rlist(1:101,1:1000)
  
   !f2py intent(in) fname,nsnaps,nstars
   !f2py intent(out) hmrad
   
   i=0
   j=0
   k=0
   dens=0.d0
   rad=0.d0
   snap=0
   ids=0
   mass=0.d0
   cod=0.d0
   codrad=0.d0
   sdist=0.d0
   pi=3.1415926535897932

   OPEN(1,file=fname,status='old')

   DO i=1,nsnaps
      DO j=1,nstars
         READ(1,*) snap(i,j), age(i,j), ids(i,j), mass(i,j), rad(i,1:3,j)
      END DO
   END DO
   
   dlist=0
   DO i=1,nsnaps
      snapmass = SUM ( mass(i,1:1000) )
      halfmass = snapmass / 2. 
      DO j=1,nstars
         DO k=1,nstars
            dist(i,1:3,k) = rad(i,1:3,j) - rad(i,1:3,k)
            sdist(i,k) = SQRT(dist(i,1,k)**2. + dist(i,2,k)**2. +dist(i,3,k)**2.)     
            dlist(i,k) = k
         END DO
         
   CALL heapsort(nstars,real(sdist(i,1:nstars)),dlist(i,1:nstars))
  
      dens(i,j) = 3./(4.*pi*(sdist(i,dlist(i,6))**3.))
            
      END DO
      cod(i,1) = SUM (dens(i,1:1000)*rad(i,1,1:1000))/ SUM ( dens(i,1:1000) )
      cod(i,2) = SUM (dens(i,1:1000)*rad(i,2,1:1000))/ SUM ( dens(i,1:1000) )
      cod(i,3) = SUM (dens(i,1:1000)*rad(i,3,1:1000))/ SUM ( dens(i,1:1000) )

      DO j=1,nstars
         codrad(i,1,j) = rad(i,1,j) - cod(i,1)
         codrad(i,2,j) = rad(i,2,j) - cod(i,2)
         codrad(i,3,j) = rad(i,3,j) - cod(i,3)
         radval(i,j) = SQRT(nradx(i,j)**2. + nrady(i,j)**2. + nradz(i,j)**2. )
         rlist(i,j)=j
      END DO

      CALL heapsort(nstars,real(radval(i,1:nstars)),rlist(i,1:nstars))

            DO j=2,nstars
         cmass(i,rlist(i,1))= mass(i,rlist(i,1))   
         cmass(i,rlist(i,j))= cmass(i,rlist(i,j-1))+mass(i,rlist(i,j))

      END DO
           
      DO j=1,nstars
         hmdif(i,rlist(i,j)) = ABS (halfmass(i,rlist(i,j))-cmass(i,rlist(i,j)))

      END DO
         hmrad(i) =  radval(i,MINLOC( hmdif(i,1:nstars)))
      
   END DO



   END SUBROUTINE Half_Mass_Radius
     
   SUBROUTINE heapsort(psort,measureof,pwhichhas)

   IMPLICIT NONE
   INTEGER, INTENT(IN)  :: psort              
   REAL,    INTENT(IN)  :: measureof(1:psort) 
   INTEGER, INTENT(OUT) :: pwhichhas(1:psort) 
   INTEGER              :: rank               
   INTEGER              :: ranknow            
   INTEGER              :: ranktest           

   DO rank=2,psort                
     ranknow=rank
1    IF (ranknow==1) CYCLE
     ranktest=ranknow/2
     IF (measureof(pwhichhas(ranktest))>=measureof(pwhichhas(ranknow))) CYCLE
     CALL swapi(pwhichhas(ranknow),pwhichhas(ranktest))
     ranknow=ranktest
     GOTO 1
   END DO
!
   DO rank=psort,2,-1             
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
