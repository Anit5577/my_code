   Subroutine Half_Mass_Radius (Fname,Nsnaps,Nstars,Hmrad)

   IMPLICIT NONE
   INTEGER :: snap(1:101,1:1000)   ! this represents the snapshot number
   INTEGER :: ids(1:101,1:1000)   ! this represents the id of the star
   INTEGER :: i,j,k,nsnaps,nstars
   CHARACTER*35 :: fname
   CHARACTER*1 :: COD_answer
   CHARACTER*40 :: HMR(1:101)
   DOUBLE PRECISION :: mass(1:101,1:1000)  !this represents the mass
   DOUBLE PRECISION :: cmass(1:101,1:1000)  !this is the cumulative mass
   DOUBLE PRECISION :: halfmass(1:101,1:1000)
   REAL :: hmdif(1:101,1:1000)
   INTEGER :: hrj(1:101,1:1000)
   DOUBLE PRECISION :: snapmass(1:101,1:1000) !total cluster mass per snapshot
   REAL :: age(1:101,1:1000) !this is the time
   DOUBLE PRECISION :: radx(1:101,1:1000) !this is the position x
   DOUBLE PRECISION :: rady(1:101,1:1000) !this is the position y
   DOUBLE PRECISION :: radz(1:101,1:1000) !this is the postion  z
   DOUBLE PRECISION :: nradx(1:101,1:1000) !this is the position x
   DOUBLE PRECISION :: nrady(1:101,1:1000) !this is the position y
   DOUBLE PRECISION :: nradz(1:101,1:1000) !this is the postion  z
   DOUBLE PRECISION :: codx(1:101) !this is the radius vector value
   DOUBLE PRECISION :: cody(1:101) !this is the radius vector value
   DOUBLE PRECISION :: codz(1:101) !this is the radius vector value
   DOUBLE PRECISION :: radval(1:101,1:1000) !this is the radius vector
   DOUBLE PRECISION :: hmrad(1:101,1:1000) !this is the half-mass radius
   DOUBLE PRECISION :: velx(1:101,1:1000) !this is the velocity x
   DOUBLE PRECISION :: vely(1:101,1:1000) !this is the velocity y
   DOUBLE PRECISION :: velz(1:101,1:1000) !this is the velocity z

   
!#  heapsorting variables
   INTEGER :: rlist(1:101,1:1000)

   !f2py intent(in) fname,nsnaps,nstars
   !f2py intent(out) hmrad
   
!# setting all variables/parameters to 0 before start, definition depends on whether they are INTEGERS, REAL or DOUBLE PRES.
   snap=0       !integer, real would have a . after the zero
   ids=0        
   mass=0.   !real
   halfmass=0.d0
   snapmass=0.d0
   cmass=0.d0
   age=0.  !double precision
   i=0
   j=0
   k=0
   radx=0.d0
   rady=0.d0
   radz=0.d0
   nradx=0.d0
   nrady=0.d0
   nradz=0.d0
   velx=0.d0
   vely=0.d0
   velz=0.d0
   hmrad=0.d0
   hmdif=0.
   hrj=0.
   
!# start to read-in file by opening .dat files as input into the terminal by use
      
   OPEN(1,file=fname,status='old')

   !# the below reads in 2-dimensional arrays based on total snapshots and total system star; keeping the age of the cluster active, which is in column 2

   nsnaps=101         ! always remember to check...
   nstars=1000
   DO i=1,nsnaps
      DO j=1,nstars
         READ(1,*) snap(i,j), age(i,j), id(i,j), mass(i,j), radx(i,j), rady(i,j), radz(i,j)
! remaining content  velx(line), vely(line), velz(line), ccname (i,j), cctimeradx(i,j), j
     !    WRITE(6,*) snap(i,j), age(i,j), id(i,j), mass(i,j), radx(i,j), rady(i,j), radz(i,j)
      END DO
   END DO

   WRITE(6,*) 'Reading in data file completed'

   ! the subroutine Centre_of_Density uses the x-,y-,z-component of the radius as an input and calculates the centre of density for these 3 components as an output. The correction for Centre of Density can be switched on or off.

   WRITE(6,*) 'Correct positions for Centre of Density - (Y/N)?'
   READ(5,*) COD_answer

   IF (COD_answer=='Y') THEN
      CALL Centre_of_Density(nsnaps,nstars,radx,rady,radz,codx,cody,codz)
   ELSE
      codx=0
      cody=0
      codz=0
      
   END IF
   
   DO i=1,nsnaps
!       WRITE (6,*) codx(i), cody(i), codz(i)
   END DO
    
! Do-loop calculates the halfmass for each snapshot, then radius magnitude, which it sorts for  each snapshot according to the radius of each star from smallest to largest

   IF (COD_answer=='Y') THEN
      HMR='HMR_COD'//infilename(1:27)//'.dat'
   ELSE
      HMR='HMR_noCOD'//infilename(1:27)//'.dat'
   ENDIF
   
   rlist=0
   DO i=1,nsnaps
      
      OPEN(40,file=HMR(i),status='unknown')
            
      snapmass = SUM ( mass(i,1:1000) )
      halfmass = snapmass / 2. 
      
      DO j=1,nstars
         nradx(i,j) = radx(i,j) - codx(i)
         nrady(i,j) = rady(i,j) - cody(i)
         nradz(i,j) = radz(i,j) - codz(i)
         radval(i,j) = SQRT(nradx(i,j)**2. + nrady(i,j)**2. + nradz(i,j)**2. )
         rlist(i,j)=j
!        WRITE(6,*) snap(i,j), id(i,j), mass(i,j), radval(i,j)
      END DO
      
      CALL heapsort(nstars,real(radval(i,1:nstars)),rlist(i,1:nstars))
      
!     The next do-loop is only used for writing the data to screen
      DO j=1,nstars
         !         WRITE(6,*) snap(i,rlist(i,j)), id(i,rlist(i,j)), mass(i,rlist(i,j)), radval(i,rlist(i,j))
      END DO
      
! summing masses for reach position from smallest to largest radius
      DO j=2,nstars
         cmass(i,rlist(i,1))= mass(i,rlist(i,1))   
         cmass(i,rlist(i,j))= cmass(i,rlist(i,j-1))+mass(i,rlist(i,j))
!         WRITE(6,*) radval(i,rlist(i,j)), cmass(i,rlist(i,j)), snapmass(i,rlist(i,j)), halfmass(i,rlist(i,j))
      END DO
           
      DO j=1,nstars
         hmdif(i,rlist(i,j)) = ABS (halfmass(i,rlist(i,j))-cmass(i,rlist(i,j)))
 !       WRITE(6,*) snap(i,rlist(i,j)), radval(i,rlist(i,j)), hmdif(i,rlist(i,j)), halfmass(i,rlist(i,j)), cmass(i,rlist(i,j))
      END DO
!        hmrad =  radval(i,MINLOC( hmdif(i,1:nstars)))
!      WRITE(6,*) 'Minimum difference is:', MINVAL( hmdif(i,1:nstars) ), MINLOC ( hmdif(i,1:nstars))

      WRITE(40,*) snap(i,nstars), radval(i,MINLOC( hmdif(i,1:nstars) ))       
        
         
   END DO   
     
   END PROGRAM half_mass_radius
 
 
    
   ! 13 columns in file with data as follows:
   ! i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)

   ! 

