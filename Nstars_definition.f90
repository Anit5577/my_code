   PROGRAM velocity_dispersion
!
! Fortran 90 programm to read in values from star simulation .dat files with 101 snapshots and 1000 stars --> change array, if the data looks different
!
   IMPLICIT NONE
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: starcounter
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: snap
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: age
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: id
   INTEGER :: i, j,nstars
   CHARACTER*35 :: infilename
   
! setting all variables/parameters to 0 before start, definition depends on whether they are INTEGERS, REAL or DOUBLE PRES.
   snap=0       !integer
   age=0.d0
   id=0        
   nstars=0
   
! start to read-in file by opening .dat files as input into the terminal by use
      
   WRITE(6,*) 'Choose data file to be read into array'
   READ(5,*) infilename
   WRITE(6,*) 'Chosen data file is: ',infilename

   OPEN(1,file=infilename,status='old')

! the below reads in 2-dimensional arrays based on total snapshots and total system star; keeping the age of the cluster active, which is in column 2
 
   
   ALLOCATE (snap(1:101,1:nstars)
   ALLOCATE (age(1:101,1:nstars)
   ALLOCATE (id(1:101,1:nstars)
   ALLOCATE (starcounter(1:101,1:nstars)

   IF 


      
      DO j = 1,nstars
         READ(1,*) snap(i,j), age(i,j), id(i,j) 
         !         WRITE(6,*) snap(i,j), age(i,j), id(i,j), mass(i,j), radx(i,j), rady(i,j), radz(i,j), velx(i,j), vely(i,j), velz(i,j)
         WRITE (6,*) nstars
      END DO
   END DO
      
   END PROGRAM velocity_dispersion
 
  
    
   ! 13 columns in file with data as follows:
   ! i,time(i),id(i),mass(i),rad(i,1:3),vel(i,1:3),ccname(i),cctime(i),d2cc(i)
