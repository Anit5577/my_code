Subroutine Bound_unbound_stars(Fname,Nsnaps,Nstars,Boundenergy)

  IMPLICIT NONE
  
  !f2py intent(in) fname,nsnaps,nstars
  !f2py intent(out) boundenergy
  
  INTEGER :: i,j,k, nsnaps,nstars
  INTEGER :: snap(1:101,1:nstars)   ! this represents the snapshot number
  INTEGER :: id(1:101,1:nstars)   ! this represents the id of the star
  INTEGER :: l(1:101)
  CHARACTER*35 :: fname
  DOUBLE PRECISION :: mass(1:101,1:nstars)  !this represents the mass
  DOUBLE PRECISION :: cmass(1:101,1:nstars)  !this is the cumulative mass
  DOUBLE PRECISION :: halfmass(1:101,1:nstars)
  DOUBLE PRECISION :: snapmass(1:101,1:nstars) !total cluster mass per snapshot
  REAL :: age(1:101,1:nstars) !this is the time
  DOUBLE PRECISION :: radvec(1:101,1:3,1:nstars) !this is the position vector
  DOUBLE PRECISION :: nradvec(1:101,1:3,1:nstars) !this is the radius vector value
  DOUBLE PRECISION :: velvec(1:101,1:3,1:nstars) !this is the velocity vector
  DOUBLE PRECISION :: velcod(1:101,1:3) !this is the velocity vector
  DOUBLE PRECISION :: veldif(1:101,1:3,1:nstars) !this is the velocity vector at centre of density
  DOUBLE PRECISION :: poten(1:101,1:nstars) !this is the potential energy of each star
  DOUBLE PRECISION :: kinen(1:101,1:nstars) !this is the kineteic energy of each star
  DOUBLE PRECISION :: boundenergy(1:101,1:nstars) !this is the kineteic energy of each star
  DOUBLE PRECISION :: raddif(1:101,1:nstars)
  DOUBLE PRECISION :: dens(1:101,1:nstars) !this is the radius vector value
  DOUBLE PRECISION :: denv(1:101,1:nstars) !this is the radius vector value
  DOUBLE PRECISION :: top(1:101,1:3,1:nstars) !this is the radius vector value
  DOUBLE PRECISION :: cod(1:101,1:3) !this is the centre of density radius vector value
  DOUBLE PRECISION :: cov(1:101,1:3) !this is the centre of density vector value
  DOUBLE PRECISION :: com(1:101,1:3) !this is the radius vector value
  DOUBLE PRECISION :: dist(1:101,1:3,1:nstars) !this is the distance vector value
  DOUBLE PRECISION :: vdist(1:101,1:nstars) !this is the distance vector value 
  DOUBLE PRECISION :: veldist(1:101,1:3,1:nstars) !this is the distance vector value
  DOUBLE PRECISION :: sdist(1:101,1:nstars) !this is the square distance value
  REAL :: pi
  REAL :: G !graviational constant
  REAL :: Msun !Solar mass
  REAL :: pc ! radius conversion factor from parsec to metre
     
  INTEGER :: vlist(1:101,1:nstars)
  
  snap=0       !integer, real would have a . after the zero
  id=0        
  mass=0.   !real
  halfmass=0.d0
  snapmass=0.d0
  cmass=0.d0
  age=0.d0  !double precision
  i=0
  j=0
  k=0
  l=0
  radvec=0.d0
  nradvec=0.d0
  velvec=0.d0
  velcod=0.d0
  veldif=0.d0
  dens=0.d0
  top=0.d0
  cod=0.d0
  com=0.d0
  dist=0.d0
  sdist=0.d0
  raddif=0.d0
  poten = 0.d0 !kg m^2 s^-2
  kinen = 0.d0 !kg m^2 s^-2
  boundenergy = 0.d0
  G = 6.67408E-11 !m^3 kg^-1 s^-2
  MSun = 1.98892E30 !kg
  pc = 3.0857E16 !parsec to m 
  pi=3.1415926535897932
  
      
  OPEN(1,file=fname,status='old')

 
  DO i=1,nsnaps
    DO j=1,nstars
      READ(1,*) snap(i,j), age(i,j), id(i,j), mass(i,j), radvec(i,1:3,j), velvec (i,1:3,j)
    END DO
  END DO
  

! for each star in each snapshot calculate the velocity difference to all other stars:
   
   vlist=0
   DO i=1,nsnaps
      DO j=1,nstars
         DO k=1,nstars
            veldist(i,1:3,k) = velvec(i,1:3,j) - velvec(i,1:3,k)
            vdist(i,k) = SQRT(veldist(i,1,k)**2. + veldist(i,2,k)**2. +veldist(i,3,k)**2.)            
            vlist(i,k) = k
!            WRITE (6,*) id(i,k), id(i,j), dist(i,1:3,k), sdist(i,k)
         END DO

! sort the list of differences of each star to all other stars in each snapshot
         
      CALL heapsort(nstars,real(vdist(i,1:nstars)),vlist(i,1:nstars))


! for each star, pick the difference to its 5th closest star to calculate the density around that star using dens = 1/V with r being the distance between them
       
         denv(i,j) = 3/(4*pi*(vdist(i,vlist(i,6))**3.))

         
      END DO

! calculate the centre of density vector for each snap by multiplying each stars density with its radius vector, then summing all of these values up and dividing it by the sum of all densities.     
    
      cov(i,1) = SUM (denv(i,1:nstars)*velvec(i,1,1:nstars))/ SUM ( denv(i,1:nstars) )
      cov(i,2) = SUM (denv(i,1:nstars)*velvec(i,2,1:nstars))/ SUM ( denv(i,1:nstars) )
      cov(i,3) = SUM (denv(i,1:nstars)*velvec(i,3,1:nstars))/ SUM ( denv(i,1:nstars) )
      

 !  calculate total potential energy of each individual star by summing up potential energy of each star with all others.

      DO j=1,nstars
         DO k=1,nstars
            dist(i,1:3,k) = radvec(i,1:3,j) - radvec(i,1:3,k)
            sdist(i,k) = SQRT(dist(i,1,k)**2. + dist(i,2,k)**2. + dist(i,3,k)**2.)
            IF (sdist(i,k)/=0) THEN
                poten(i,k) = (G*mass(i,j)*Msun*mass(i,k)*Msun)/(sdist(i,k)*pc)
            ELSE
                poten(i,k) = 0
            END IF
            
         END DO

! after calculating the individual potential energies between each star j and each star k, the negative sum is calculated for each star j by summing up all its individual energy components with each other star

           
         poten(i,j) = - SUM (poten(i,1:nstars))

!         WRITE (6,*) id(i,j), poten(i,j)

           
!  calculate kinetic energy of each star in each snapshot and convert velocities in km/s to m/s
            
!            kinen(i,j) = 0.5 * mass(i,j)* (velvec(i,1:3,j) - cov(i,1:3))**2
         
         kinen(i,j) = 0.5 * mass(i,j)*Msun* (((SQRT((velvec(i,1,j) - cov(i,1))**2.+(velvec(i,2,j) &
                      - cov(i,2))**2.+(velvec(i,3,j) - cov(i,3))**2.))*10**3.)**2.)


         boundenergy(i,j) = kinen(i,j) + poten(i,j)
  
         
      END DO
              
         
  END DO  

  REWIND (1)

End subroutine Bound_unbound_stars
 
  
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

