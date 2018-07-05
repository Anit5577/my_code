   MODULE parameters_mod
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: iid                 ! initial conditions identifier array    
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: id                ! snapshot (x) indentifier array
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: imass      ! initial conditions mass array
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: mass     ! snapshot (x) mass array
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: irad     ! initial conditions radial vector array
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: rad    ! snapshot (x) radial vector array
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: ivel     ! initial conditions velocity vector array
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: vel    ! snapshot (x) velocity vector array
   REAL, DIMENSION(:), ALLOCATABLE :: time                     ! time array as function of snapshot
   INTEGER, DIMENSION(:), ALLOCATABLE :: instar                ! counters for number of stars in initial conditions file 
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: nstar               ! counters for number of stars in snapshots
   double precision, dimension(:,:), allocatable :: potenergy
   double precision, dimension(:,:), allocatable :: kinenergy 
   END MODULE parameters_mod
! ***************** CLUSTER PARAMETERS MODULE *********************************************************
   MODULE cluster_parameters_mod
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: icom        ! initial conditions centre-of-mass
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: scom      ! snapshot centre-of-mass
   DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: iclusmass     ! initial cluster mass
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: sclusmass   ! snapshot cluster mass
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: iradmod     ! initial magnitude of radial vector
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: iradlist             ! list of initial radial vectors
   DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: irhalfm       ! initial half-mass radius
   integer, dimension(:), allocatable :: irhmnum                ! number of stars within the initial half-mass radius
   double precision, dimension(:), allocatable :: itfpe         ! 25% extent of cluster (in ics) 
   double precision, dimension(:), allocatable :: isfpe         ! 75% extent of cluster (in ics) 
   DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: infpe         ! 95% extent of cluster (in ics)
   integer, dimension(:,:), allocatable :: ineigh               ! nearest neighbour to each star in ics   
   
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: sradmod   ! snapshot magnitude of radial vector
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: sradlist           ! list of snapshot radial vectors
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: srhalfm     ! snapshot half-mass radius
   integer, dimension(:,:), allocatable :: srhmnum                ! number of stars within the snapshot half-mass radius
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: stfpe         ! 25% extent of cluster (in snapshot)
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: ssfpe         ! 75% extent of cluster (in snapshot)
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: snfpe         ! 95% extent of cluster (in snapshot)
   integer, dimension(:,:,:), allocatable :: sneigh               ! nearest neighbour to each star in snapshots
   double precision, dimension(:,:,:), allocatable :: stdcentroid ! snapshot 2D centroid
   double precision, dimension(:,:,:), allocatable :: smaxsigpos ! position of star with maximum stellar surface density
   logical, dimension(:,:), allocatable :: ibound             ! initial conditiosn determination of whether a star is energetically bound or not
   logical, dimension(:,:,:), allocatable :: sbound             ! snapshot determination of whether a star is energetically bound or not
   double precision, dimension(:), allocatable :: ijac_rad      ! initial Jacobi radius
   double precision, dimension(:,:), allocatable :: sjac_rad    ! snapshot Jacobi radius
   double precision, dimension(:,:), allocatable :: sjac_rhm    ! half-mass radius within Jacobi radius (snapshot)
   integer, dimension(:,:), allocatable :: nsjac_bound          ! number within Jacobi radius (snapshot)
   double precision, dimension(:,:), allocatable :: sjac_clus_mass ! mass of 'cluster' within Jacobi radius (snapshot)
   double precision, dimension(:,:,:), allocatable :: sjac_mass ! mass of stars within Jacobi radius (snapshot)
   double precision, dimension(:,:,:,:), allocatable :: sjac_pos  ! positional vector of stars within Jacobi radius (snapshot)
   double precision, dimension(:,:),allocatable :: iam
   double precision, dimension(:,:,:), allocatable :: sam
   double precision, dimension(:,:), allocatable :: ipotential
   double precision, dimension(:,:,:), allocatable :: spotential
   real, dimension(:,:,:), allocatable :: sig_array             ! local surface density evolution array
   real, dimension(:,:,:), allocatable :: rho_array             ! local volume-mass density evolution array
   real, dimension(:,:,:), allocatable :: lambda_array
   real, dimension(:,:,:), allocatable :: lambda_pe_array
   real, dimension(:,:,:), allocatable :: lambda_ne_array
   real, dimension(:,:,:), allocatable :: sigma_m_mm_array
   real, dimension(:,:,:), allocatable :: sigma_m_av_array
   real, dimension(:,:,:), allocatable :: sigma_m_ks_array
   real, dimension(:,:,:), allocatable :: r_ss_array
   real, dimension(:,:,:), allocatable :: r_ss_pe_array
   real, dimension(:,:,:), allocatable :: r_ss_ne_array
   real, dimension(:,:,:), allocatable :: kirk_gut_array 
   real, dimension(:,:), allocatable :: imassrange
   real, dimension(:,:,:), allocatable :: smassrange
   END MODULE cluster_parameters_mod
! **************** SINGLE STAR PROPERTIES MODULE ***********************************************************
   MODULE single_parameters_mod                                ! single according to nearest neighbour algorithm
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: ixid                ! initial conditions single identifier
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: ixmass     ! initial conditions single mass
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: ixrad    ! initial conditions single radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: ixvel    ! initial conditions single velocity vector
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: sxid              ! snapshot single indentifier
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: sxmass   ! snapshot single mass
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: sxrad  ! snapshot single radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: sxvel  ! snapshot single velocity vector   
   END MODULE single_parameters_mod 
! **************** BINARY PROPERTIES MODULE ***********************************************************
   MODULE binary_parameters_mod                                ! binary according to nearest neighbour algorithm
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: ipid                ! initial conditions primary id
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: isid                ! initial conditions secondary id
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: ipmass     ! initial conditions primary mass
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: ismass     ! initial conditions secondary mass
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: iprad    ! initial conditions primary radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: israd    ! initial conditions secondary radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: ipvel    ! initial conditions primary velocity vector
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: isvel    ! initial conditions secondary velocity vector
   double precision, dimension(:,:,:), allocatable :: ibcv     ! initial conditions binary centre of velocity vector
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: isma       ! initial conditions semi-major axis
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: iper       ! initial conditions period
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: iEbind       ! initial conditions binding energy
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: iecc       ! initial conditions eccentricity
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: spid              ! snapshot primary id
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: ssid              ! snapshot secondaty id
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: spmass   ! snapshot primary mass
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: ssmass   ! snapshot secondary mass
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: sprad  ! snapshot primary radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: ssrad  ! snapshot secondary radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: spvel  ! snapshot primary velocity vector
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: ssvel  ! snapshot secondary velocity vector
   double precision, dimension(:,:,:,:), allocatable :: sbcv   ! snapshot binary centre of velocity
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: ssma     ! snapshot semi-major axis
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: sper     ! snapshhot period
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: sEbind   ! snapshhot binding energy
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: secc     ! snapshot eccentricity
   END MODULE binary_parameters_mod
! **************** TRIPLE PROPERTIES MODULE ***********************************************************
   MODULE triple_parameters_mod                                    ! triple according to nearest neighbour algorithm
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: itrpid                  ! initial triple primary id
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: itrsid                  ! initial secondary id
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: itrtid                  ! initial tertiary id
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: itrpmass       ! initial triple primary mass
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: itrsmass       ! initial triple secondary mass
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: itrtmass       ! initial triple tertiary mass
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: itrprad      ! initial triple primary radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: itrsrad      ! initial triple secondary radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: itrtrad      ! initial triple tertiary radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: itrpvel      ! initial triple primary velocity vector 
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: itrsvel      ! initial triple secondary velocity vector
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: itrtvel      ! intiial triple tertiary velocity vector

   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: itrsmao      ! snapshot semi-major axis of first triple orbit 
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: itrecco      ! snapshot eccentricity of first triple orbit 
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: itrsmat      ! snapshot semi-major axis of second triple orbit 
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: itrecct      ! snapshot eccentricity of second triple orbit 

   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: strpid                ! snapshot triple primary id
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: strsid                ! snapshot triple secondary id
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: strtid                ! snapshot triple tertiary id
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: strpmass     ! snapshot triple primary mass
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: strsmass     ! snapshot triple secondary mass
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: strtmass     ! snapshot triple tertiary mass
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: strprad    ! snapshot triple primary radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: strsrad    ! snapshot triple secondary radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: strtrad    ! snapshot triple tertiary radial vector
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: strpvel    ! snapshot triple primary velocity vector
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: strsvel    ! snapshot triple secondary velocity vector
   DOUBLE PRECISION, DIMENSION(:,:,:,:), ALLOCATABLE :: strtvel    ! snapshot triple tertiary velocity vector
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: strsmao      ! snapshot semi-major axis of first triple orbit 
!   double precision, dimension(:,:,:), allocatable :: stper1
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: strecco      ! snapshot eccentricity of first triple orbit 
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: strsmat      ! snapshot semi-major axis of second triple orbit 
!   double precision, dimension(:,:,:), allocatable :: stper2
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: strecct      ! snapshot eccentricity of second triple orbit 
   END MODULE triple_parameters_mod
! **************** PHYSICAL CONSTANTS MODULE **********************************************************
   MODULE phys_constants_mod
   DOUBLE PRECISION :: pi,twopi
   DOUBLE PRECISION :: au=1.5d11              ! m
   DOUBLE PRECISION :: rsun=6.955d8           ! m
   DOUBLE PRECISION :: msun=2.d30             ! kg
   DOUBLE PRECISION :: pc=3.086d16            ! m
   DOUBLE PRECISION :: yr=365.25*24.*60.*60.  ! s
   DOUBLE PRECISION :: day=24.*60.*60.        ! s
   DOUBLE PRECISION :: G=6.673d-11            ! m^3 kg^-1 s^-2
   real :: r_gal=8000.                           ! Galactocentric distance - 8kpc
   double precision :: m_gal=1.d12            ! Galaxy mass (msun)
   END MODULE phys_constants_mod
! **************** STELLAR CONSTANTS MODULE ************************************************************
   MODULE stellar_constants_mod
   DOUBLE PRECISION :: mh=0.08  ! Hydrogen burning limit
   DOUBLE PRECISION :: mv=0.106 ! maximum mass of a VLM object
   DOUBLE PRECISION :: mm=0.47  ! maximum mass of an M-dwarf
   DOUBLE PRECISION :: mk=0.84  ! maximum mass of a K-dwarf
   DOUBLE PRECISION :: mg=1.2   ! maximum mass of a G-dwarf
   DOUBLE PRECISION :: mf=1.8   ! maximum mass of an F star
!   DOUBLE PRECISION :: ma=3.5   ! maximum mass of an A star
   DOUBLE PRECISION :: ma=2.5   ! maximum mass of an A star
!   DOUBLE PRECISION :: lb=8.    ! lower mass limit for a B-type star
   DOUBLE PRECISION :: lb=5.    ! lower mass limit for a B-type star   ! Pacman's book, page 103 gives masses of O/B stars
   DOUBLE PRECISION :: lo=17.5  ! lower mass limit for an O-type star
   END MODULE stellar_constants_mod
!***************** EXTRACTION (PARTICLE) MODULE ********************************************************
   MODULE extract_part_mod                                   ! temporarily stores particle info at each snapshot
   DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: m          ! mass
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: r        ! radial vector
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: v        ! velocity vector
   INTEGER, DIMENSION(:), ALLOCATABLE :: ident               ! id
   character*14, dimension(:), allocatable :: charident
   DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: totalm     ! total mass of particle (from node info)
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: totalr   ! total radial vector (from node info)
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: totalv   ! total velocity vector (from node info)
   END MODULE extract_part_mod
! **************** EXTRACTION TRACKING MODULE *********************************************************
   MODULE extract_track_mod                                  ! counters for various particles in nodes
   INTEGER :: parent
   INTEGER, DIMENSION(:), ALLOCATABLE :: childof
   INTEGER, DIMENSION(:), ALLOCATABLE :: sibling
   INTEGER, DIMENSION(:), ALLOCATABLE :: nval
   LOGICAL, DIMENSION(:), ALLOCATABLE :: indivstar
   LOGICAL, DIMENSION(:), ALLOCATABLE :: done
   INTEGER :: nfalse
   INTEGER :: ncounter 
   END MODULE extract_track_mod
! *************** EXTRACTION (STELLAR EVOLUTION) MODULE ***********************************************
   MODULE extract_stellar_ev_mod                                  ! (extract) stellar evolution info 
   CHARACTER*50, DIMENSION(:,:), ALLOCATABLE :: esevstate         ! (extract) stellar evolution state
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: esevtime      ! (extract) stellar evolution time
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: esnkick       ! (extract) supernova kick
   INTEGER, DIMENSION(:), ALLOCATABLE :: ensevstate               ! (extract) numbered stellar evolution state
   END MODULE extract_stellar_ev_mod
! *************** STELLAR EVOLUTION MODULE ************************************************************
   MODULE stellar_ev_mod                                          ! stellar evolution info 
   character*13, dimension(:,:,:), allocatable :: sevid           ! stelalr evolution ID
   CHARACTER*50, DIMENSION(:,:,:), ALLOCATABLE :: sevstate        ! stellar evolution state
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: sevtime     ! stellar evolution time
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: snkick      ! supernova kick
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: nsevstate              ! numbered stellar evolution state
   END MODULE stellar_ev_mod
! *************** EXTRACTION (CLOSE ENCOUNTER) MODULE *************************************************
   MODULE extract_encounter_mod
   integer, dimension(:), allocatable :: eccname
   double precision, dimension(:), allocatable :: ed2cc1
   double precision, dimension(:), allocatable :: ed2cc
   double precision, dimension(:), allocatable :: ecctime
   integer, dimension(:), allocatable :: epcccntr
   integer, dimension(:), allocatable :: epccname
   double precision, dimension(:), allocatable :: epcctime
   double precision, dimension(:), allocatable :: ecolltskip
   end module extract_encounter_mod
! *************** CLOSE ENCOUNTER MODULE **************************************************************
   MODULE close_encounter_mod
   integer, dimension(:,:,:), allocatable :: ccname
   double precision, dimension(:,:,:), allocatable :: d2cc1
   double precision, dimension(:,:,:), allocatable :: d2cc
   double precision, dimension(:,:,:), allocatable :: cctime
   integer, dimension(:,:,:), allocatable :: pcccntr
   integer, dimension(:,:,:), allocatable :: pccname
   double precision, dimension(:,:,:), allocatable :: pcctime
   double precision, dimension(:,:,:), allocatable :: colltskip
   end module close_encounter_mod
!**************** MULTIPLICITY CALCULATOR *************************************************************
   MODULE mult_calc_mod                                           ! calculate multiplicity fractions from counters
   INTEGER :: nmult                                               ! number of different multiplicity categories [1 = all stars, 2 = BDs, etc.] 
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: isingle                ! number of initial singles
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: ibinary                ! number of initial binaries
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: itriple                ! number of initial triples
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: iquadruple             ! number of initial quadruples
   REAL, DIMENSION(:,:), ALLOCATABLE :: imult                     ! initial multiplicity
   logical, dimension(:,:), allocatable :: ibin
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: ssingle              ! number of snapshot singles
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: sbinary              ! number of snapshot binaries
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: striple              ! number of snapshot triples
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: squadruple           ! number of snapshot quadruples
   REAL, DIMENSION(:,:,:), ALLOCATABLE :: smult                   ! snapshot multiplicity
   logical, dimension(:,:,:), allocatable :: sbin
   INTEGER, DIMENSION(:), ALLOCATABLE :: totisingle               ! total number of initial singles
   INTEGER, DIMENSION(:), ALLOCATABLE :: totibinary               ! total number of initial binaries
   INTEGER, DIMENSION(:), ALLOCATABLE :: totitriple               ! total number of initial triples
   INTEGER, DIMENSION(:), ALLOCATABLE :: totiquadruple            ! total number of initial quadruples
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: totssingle             ! total number of snapshot singles
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: totsbinary             ! total number of snapshot binaries
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: totstriple             ! total number of snapshot triples
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: totsquadruple          ! total number of snapshot quadruples
   END MODULE mult_calc_mod
!*************** VELOCITY DISPERSION *******************************************************************
   MODULE vel_disp_mod                                                  ! to calculate velocity distributions
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: threedivel          ! magnitude of initial velocity vector
   double precision, dimension(:,:), allocatable :: ivelx               ! x-component of initial velocity, with COV subtracted
   double precision, dimension(:,:), allocatable :: ively               ! y-component of initial velocity, with COV subtracted
   double precision, dimension(:,:,:), allocatable :: ivelz               ! z-component (RV) of initial velocity, with COV subtracted
   double precision, dimension(:,:), allocatable :: izdispersion        ! z-component initial velocity dispersion (definition-dependent)
   double precision, dimension(:,:), allocatable :: innvelzdiff         ! difference between velocity of star and nearest neighbour
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: threedvel         ! magnitude of snapshot velocity vector
   double precision, dimension(:,:,:), allocatable :: svelx             ! x-component of snapshot velocity, with COV subtracted
   double precision, dimension(:,:,:), allocatable :: svely             ! y-component of snapshot velocity, with COV subtracted
   double precision, dimension(:,:,:,:), allocatable :: svelz             ! z-component (RV) of snapshot velocity, with COV subtracted
   double precision, dimension(:,:,:), allocatable :: szdispersion      ! z-component snapshot velocity dispersion (definition-dependent)
   double precision, dimension(:,:,:), allocatable :: snnvelzdiff         ! difference between velocity of star and nearest neighbour
!   double precision, dimension(:,:,:), allocatable :: snnvelpmdiff      ! difference between proper motion of star and nearest neighbour
   DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: meanthreedivel        ! mean magnitude initial velocity vector
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: meanthreedvel       ! mean magnitude snapshot velocity vector
   DOUBLE PRECISION :: meanofmeanthreediv                               ! mean of mean magnitude initial velocity vector 
   DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: meanofmeanthreedv     ! mean of mean magnitude snapshot velocity vector 
   DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: icov                ! initial centre of velocity
   DOUBLE PRECISION, DIMENSION(:,:,:), ALLOCATABLE :: scov              ! snapshot centre of velocity
   INTEGER, DIMENSION(:,:), ALLOCATABLE :: ivlist                       ! list of initial velocities (mag)
   integer, dimension(:,:), allocatable :: ivxlist                      ! list of initial x-velocities
   integer, dimension(:,:), allocatable :: ivylist                      ! list of initial y-velocities
   integer, dimension(:,:,:), allocatable :: ivzlist                      ! list of initial z-velocities (RV)
   integer, dimension(:,:), allocatable :: innvzdifflist                ! list of initial nearest neighbour velocity differences 
   INTEGER, DIMENSION(:,:,:), ALLOCATABLE :: svlist                     ! list of snapshot velocities (mag)
   integer, dimension(:,:,:), allocatable :: svxlist                    ! list of snapshot x-velocities
   integer, dimension(:,:,:), allocatable :: svylist                    ! list of snapshot y-velocities
   integer, dimension(:,:,:,:), allocatable :: svzlist                    ! list of snapshot z-velocities (RV)
   integer, dimension(:,:,:), allocatable :: snnvzdifflist              ! list of snapshot nearest neighbour velocity differences 
   DOUBLE PRECISION :: meanofmedianthreediv                             ! mean of median initial velocity magnitudes
   DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: meanofmedianthreedv   ! mean of meadian snapshot velocity magnitudes
   DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: meanoftfpcthreedv     ! mean of 25% percentile velocity magnitude
   DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: meanofsfpcthreedv     ! mean of 75% percentile velocity magnitude
   double precision, dimension(:), allocatable :: meanofmedianboundvel ! mean of median snaphsot bound velocities
   double precision, dimension(:), allocatable :: meanoftfpcboundvel    ! mean of 25% percentile velocity magnitude (bound)
   double precision, dimension(:), allocatable :: meanofsfpcboundvel    ! mean of 75% percentile velocity magnitude (bound)
   double precision, dimension(:), allocatable :: meanofmedianescvel ! mean of median snaphsot bound velocities
   double precision, dimension(:), allocatable :: meanoftfpcescvel      ! mean of 25% percentile velocity magnitude (escaper)
   double precision, dimension(:), allocatable :: meanofsfpcescvel      ! mean of 75% percentile velocity magnitude (escaper)
   real, dimension(:,:), allocatable :: vdr_ks_array                    ! KS test array for velocites of 20 most massive stars compared to cluster
   END MODULE vel_disp_mod
