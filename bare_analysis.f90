   PROGRAM bare_analysis

   USE parameters_mod
   USE stellar_ev_mod
   USE close_encounter_mod
   IMPLICIT NONE
   INTEGER :: nfile,nf  ! number of files
   INTEGER :: nss,nst,ntime ! number of snapshots
   INTEGER :: ns    ! number of snapshots to be extracted
   INTEGER :: nr    ! root number tobe extracted
   INTEGER :: nroot(1:10000)
   INTEGER :: snapreq,maxsnap
   INTEGER :: i,j,k
   INTEGER :: ini,ni
   INTEGER :: nmax
   CHARACTER*30 :: filename(100)!,dummyfilename
   DOUBLE PRECISION :: tunit,munit,runit
   DOUBLE PRECISION :: timeunit(100),radunit(100)
   CHARACTER*4 :: equals
   CHARACTER*40 :: descriptor
   CHARACTER*20 :: partname
   CHARACTER*40 :: data_dump(1:100)
   CHARACTER*40 :: SE_dump(1:100)
   DOUBLE PRECISION :: timecal(10000)
   DOUBLE PRECISION :: timereq(10000)
   CHARACTER*1 :: timespec
   DOUBLE PRECISION :: timefind(10000)
   INTEGER :: nt,t
   INTEGER :: nsim
   INTEGER :: n
 
   nfile=0

   OPEN(1,file='fileslist',status='old')
!   open(1,file='filesM1a0e3VEpl10SbSrU10',status='old')


    DO
       nfile=nfile + 1
       READ(1,*,END=1) filename(nfile) ! this line is altered from 'read(1,*,err=1) filename(nf), which worked on NAG at Sheffield 
       WRITE(6,*) filename(nfile)
     END DO  
   CLOSE(1)
1  nfile=nfile - 1 
   WRITE(6,*) 'finished reading',nfile,' filenames'
 
   OPEN(2,file=filename(2),status='old')
     DO 
       READ(2,*,END=2) descriptor
       IF (descriptor=='time_scale') THEN
          BACKSPACE 2
          READ(2,*) descriptor,equals,tunit
          EXIT
       END IF
     END DO
2  CLOSE(2)
   WRITE(6,*) 'file',filename(2),'closed: tunit = ',tunit

   nss=0
   nst=0
   timecal=0.
   OPEN(2,file=filename(2),status='old')
     DO
       READ(2,*,END=20) descriptor
       IF (descriptor=='name') THEN
          BACKSPACE 2
          READ(2,*,END=20) descriptor,equals,partname
          IF (partname=='root') THEN 
             nss=nss + 1
             READ(2,*,END=20) descriptor,equals,nmax ! we may need to move this to above, if we turn on 'remove escapers' function 
           END IF
       END IF
       IF (descriptor=='system_time') THEN 
          nst=nst + 1
          BACKSPACE 2
          READ(2,*,END=20) descriptor,equals,timecal(nst)
!          write(6,*) 'system time',timecal(nst)
       END IF
     END DO
20 CLOSE(2)
   WRITE(6,*) 'there were',nss,'snapshots',nst
   ntime=nst
   timecal=timecal/tunit ! convert from N-body units to Myr

   WRITE(6,*) 'there are',nmax,'stars in the first run file snapshot'

   timereq=0.
   WRITE(6,*) 'choose number of snapshot times required'
   READ(5,*) snapreq
   IF (snapreq==1) THEN
      WRITE(6,*) 'Enter a snapshot time between',timecal(1),'and',timecal(ntime)
      READ(5,*) timereq(1)
      IF (timereq(1)<timecal(1) .OR. timereq(1)>timecal(ntime)) STOP 'invalid time entered'
      WRITE(6,*) 'comparing initial conditions and chosen snapshot time',timereq(1),'Myr only'
   ELSE
      WRITE(6,*) 'If you require specific times, enter "s". If you would like a linear range, enter "l"'
      READ(5,*) timespec
      IF (timespec=='s') THEN
         WRITE(6,*) 'Enter specific times between',timecal(1),'and',timecal(ntime),':'
         DO i=1,snapreq
            READ(5,*) timereq(i)
            WRITE(6,*) 'Time',i,'=',timereq(i)
            IF (timereq(i)<0.9*timecal(1) .OR. timereq(i)>1.1*timecal(ntime)) STOP 'invalid time entered'
         END DO
      ELSE IF (timespec=='l') THEN
         WRITE(6,*) 'linear'
         DO i=1,snapreq
            timereq(i)=(DBLE(i)/DBLE(snapreq))*timecal(ntime)
            WRITE(6,*) 'Time',i,'=',timereq(i)
         END DO
      ELSE
         STOP 'invalid time specification'    
      END IF
   END IF

   nroot=0


   maxsnap=snapreq + 1  ! Number of snapshots + time = 0 snapshot.
   nmax=nmax*3 ! to account for the head-nodes of particles (raw m, r, v, etc.)

   ALLOCATE(time(1:maxsnap))

   ALLOCATE(id(1:nfile,1:maxsnap,1:nmax))
   ALLOCATE(iid(1:nfile,1:nmax))
   ALLOCATE(imass(1:nfile,1:nmax))
   ALLOCATE(mass(1:nfile,1:maxsnap,1:nmax))
   ALLOCATE(irad(1:nfile,1:3,1:nmax))
   ALLOCATE(rad(1:nfile,1:maxsnap,1:3,1:nmax))
   ALLOCATE(ivel(1:nfile,1:3,1:nmax))
   ALLOCATE(vel(1:nfile,1:maxsnap,1:3,1:nmax))
  
   ALLOCATE(potenergy(1:nfile,1:maxsnap))
   ALLOCATE(kinenergy(1:nfile,1:maxsnap))

! allocate arrays for stellar evolution
   ALLOCATE(sevid(1:nfile,1:maxsnap,1:nmax))
   ALLOCATE(sevstate(1:nfile,1:10,1:nmax))
   ALLOCATE(sevtime(1:nfile,1:10,1:nmax))
   ALLOCATE(snkick(1:nfile,1:3,1:nmax))
   ALLOCATE(nsevstate(1:nfile,1:nmax))
   sevid='null'
   sevstate='main_sequence' 
   sevtime=0.d0
   snkick=0.d0
   nsevstate=0

! allocate arrays for close encounters
   ALLOCATE(ccname(1:nfile,1:maxsnap,1:nmax))
   ALLOCATE(d2cc1(1:nfile,1:maxsnap,1:nmax))
   ALLOCATE(d2cc(1:nfile,1:maxsnap,1:nmax))
   ALLOCATE(cctime(1:nfile,1:maxsnap,1:nmax))
   ALLOCATE(pcccntr(1:nfile,1:maxsnap,1:nmax))
   ALLOCATE(pccname(1:nfile,1:maxsnap,1:nmax))
   ALLOCATE(pcctime(1:nfile,1:maxsnap,1:nmax))
   ALLOCATE(colltskip(1:nfile,1:maxsnap,1:nmax))
   ccname=0
   d2cc1=0.d0
   d2cc=0.d0
   cctime=0.d0
   pcccntr=0
   pccname=0
   pcctime=0.d0
   colltskip=0.d0

   ALLOCATE(instar(1:nfile))
   ALLOCATE(nstar(1:nfile,1:maxsnap))

   time=0.
   DO i=1,snapreq
      time(i)=REAL(timereq(i))
      WRITE(6,*) time(i)
   END DO 

   id=0
   iid=0
   imass=0.d0
   mass=0.d0
   irad=0.d0
   rad=0.d0
   ivel=0.d0
   vel=0.d0

   potenergy=0.d0
   kinenergy=0.d0


   nsim=0
   nstar=0
   instar=0

   timeunit=0.d0   
   radunit=0.d0

   DO nf=1,nfile
      WRITE(6,*) 'NF IS EQUAL TO ',nf,filename(nf)
      OPEN(3,file=filename(nf),status='old')
        DO
          READ(3,*,END=3) descriptor
          IF (descriptor=='mass_scale') THEN
             BACKSPACE 3
             READ(3,*) descriptor,equals,munit
             READ(3,*) descriptor,equals,runit
             READ(3,*) descriptor,equals,tunit
             EXIT
          END IF
        END DO
3     CLOSE(3)
      WRITE(6,*) 'time unit for ',filename(nf),'=',tunit,munit,runit

      nt=0
      timefind=0.
      OPEN(3,file=filename(nf),status='old')   
         DO
           READ(3,*,END=30) descriptor
           IF (descriptor=='system_time') THEN
              BACKSPACE 3
              nt=nt + 1
              READ(3,*) descriptor,equals,timefind(nt)
           END IF
         END DO
30    CLOSE(3)
      WRITE(6,*) '?',nt
      timefind=timefind/tunit

      IF (filename(nf)(1:2)=='ic') THEN
         nsim=nsim + 1
         WRITE(6,*) 'time = 0, snap==1'
         ns=1        ! snapshot number
         nr=1        ! root number required
         WRITE(6,*) 'ns',ns,'nr',nr,'nf',nf,tunit,munit,runit
         CALL read_ic(snapreq,nf,filename,ns,nr,nsim,nmax,tunit,munit,runit,ni)
         instar(nsim)=ni
      ELSE
         data_dump(nsim)='data_'//filename(nf)(4:25)//'.dat'
         SE_dump(nsim)='SeBa_'//filename(nf)(4:25)//'.dat'
         DO i=1,snapreq
            IF (snapreq<nss) THEN
               DO t=1,nt+1
                  IF (t.NE.nt) THEN 
                     IF (timereq(i)>timefind(t) .AND. timereq(i)<=timefind(t+1)) THEN
                        IF ((timereq(i) - timefind(t)) <= (timefind(t+1) - timereq(i))) THEN
                           WRITE(6,*) timereq(i),timefind(t),'if less',timefind(t+1),i,t
                           nr=t          ! root number required
                        ELSE
                           WRITE(6,*) timereq(i),timefind(t+1),'if greater',timefind(t),i,t+1
                           nr=t+1        ! root number required
                        END IF
                     END IF
                  ELSE IF (timereq(i)>timefind(nt)) THEN
                     WRITE(6,*) timereq(i),timefind(nt),'end',timefind(t),i,t
                     nr=t                ! root number required 
                  ELSE IF (timereq(i)<timefind(1)) THEN
                     WRITE(6,*) timereq(i),timefind(1),'start',timefind(1),i,t   ! was timefind(t)
                     nr=1                 ! root number required                 ! was nr=t
                  END IF
                  ns=i! + 1  ! snapshot number 
               END DO
            ELSE
               nr=i
               ns=i
            END IF
            nroot(i)=nr
            WRITE(6,*) 'ns',ns,'nr',nr,'nf',nf,tunit,munit,runit
            timeunit(nsim)=tunit
            radunit(nsim)=runit
         END DO
         WRITE(6,*) snapreq
         CALL read_snapshots(snapreq,nf,filename,ns,nr,nsim,nmax,tunit,munit,runit,nroot)
      END IF
   END DO

   WRITE(6,*)'number of simulations = ',nsim,snapreq,ns

! creates two datafiles:
! file 30 writes out particle info: snapshot number (initial conditions = 0), time (Myr), particle id, 
! mass (msun), position vector (pc), velocity vector (km/s), id of close encounter star, close encounter time, 
! close encounter distance (pc). 
! file name = 'data_XXXX.dat'
!
! file 40 writes out stellar evolution info *if* the star moves off main sequence: particle id, stellar evolution state,
! stellar evolution time and then the supernova's velocity kick vector (= 0 0 0 if no supernova)
! file name = SeBa_XXXX.dat'
!
   DO i=1,nsim
      OPEN(30,file=data_dump(i),status='new')
      OPEN(40,file=SE_dump(i),status='new')
      DO j=1,instar(i)
         WRITE(30,*) 0, 0., iid(i,j),imass(i,j),irad(i,1:3,j),ivel(i,1:3,j),0,0.,0.
      END DO
      DO k=1,snapreq
         DO j=1,nstar(i,k)
            WRITE(30,*) k,time(k),id(i,k,j),mass(i,k,j),rad(i,k,1:3,j),vel(i,k,1:3,j),&
                 &ccname(i,k,j),cctime(i,k,j),d2cc(i,k,j)
            IF (k==snapreq) THEN
               IF (sevstate(i,1,j)=='main_sequence') CYCLE
               DO n=1,nsevstate(i,j)
                  WRITE(40,*) id(i,k,j),sevstate(i,n,j),'=',sevtime(i,n,j)
               END DO
               WRITE(40,*) 'SN kick velocity',snkick(i,1:3,j)
            END IF
         END DO
      END DO
      CLOSE(30)
      CLOSE(40)
   END DO

   DEALLOCATE(time)

   DEALLOCATE(id)
   DEALLOCATE(iid)
   DEALLOCATE(imass)
   DEALLOCATE(mass)
   DEALLOCATE(irad)
   DEALLOCATE(rad)
   DEALLOCATE(ivel)
   DEALLOCATE(vel)
   DEALLOCATE(potenergy)
   DEALLOCATE(kinenergy)
   DEALLOCATE(sevid)
   DEALLOCATE(sevstate)
   DEALLOCATE(sevtime)
   DEALLOCATE(snkick)
   DEALLOCATE(nsevstate)
   DEALLOCATE(ccname)
   DEALLOCATE(d2cc1)
   DEALLOCATE(d2cc)
   DEALLOCATE(cctime)
   DEALLOCATE(pcccntr)
   DEALLOCATE(pccname)
   DEALLOCATE(pcctime)
   DEALLOCATE(colltskip)
   DEALLOCATE(instar)
   DEALLOCATE(nstar)

   WRITE(6,*) 'Extraction routine finished'
  
   END PROGRAM

! 
