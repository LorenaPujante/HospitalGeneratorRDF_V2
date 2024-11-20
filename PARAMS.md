
In this file, we present the values for the parameters of H-Outbreak and HospitalGeneratorRDF_VW used to create the dataset used for the experiments of the work [~~doi: TODO~~](NULL).

## 1. Parameters of H-Outbreak
- _n_patients_: 0.7
- _steps_: 270,      `# 1 Step = 8 hours     # 1 Day = 3 steps     # 3 Months = 3 months * 30 days * 3 steps = 270 steps`
- _population_: 400000
- _step_time_: 8     `# hours`
- _init_exposed_: 1
- _init_infected_: 0
  
- _arrival_rate_: 18.603
- _prob_arrival_ER_: 0.7
- _arrival_state_colonized_: 0.076 
- _arrival_state_S_: 0.9973429
- _arrival_state_I_: 0.001563
- _arrival_state_NS_: 0.0010941
  
- _prob_p-env_min_: 0.14
- _prob_p-env_max_: 0.9
- _prob_p-env_mean_: 0.52
  
- _prob_env-p_min_: 0.326
- _prob_env-p_max_: 0.544
- _prob_env-p_mean_: 0.435
  
- _prob_pe_min_: 0.3
- _prob_pe_max_: 0.4
- _prob_pe_mean_: 0.35
  
- _incubation_time_min_: 48
- _incubation_time_max_: 72
- _prob_quick_recov_min_: 0.0
- _prob_quick_recov_max_: 0.23
- _prob_quick_recov_mean_: 0.115 
- _prob_long_recov_min_: 0.5985
- _prob_long_recov_max_: 0.9975
- _prob_long_recov_mean_: 0.7981
- _treatment_days_min_: 5
- _treatment_days_max_: 15
- _treatment_days_mean_: 10
- _prob_death_: 0.027
  
- _max_patients_rx_: 24
- _max_patients_qx_: 27
- _min_steps_rx_: 10          `# (3-4 days)  3*3=9  <->  4*3=12`
- _min_steps_qx_: 15          `# (5 days)  5*3=15`
- _max_ward_movements_: 8     `# 17 Servs (Ward) and 41 HUs     # ~8 Rooms/HU    # 2 Beds/Room    # ~8*41*2 = 656 Beds    # ~656/17 = 38 Beds/Ward    # 20% = 38*20/100 = 7.6 ~ 8`
- _max_steps_er_icu_: 3       `# 1 Day`
- _max_movements_room_: 30    `# ~656 Beds = Patients  # 5% = 656*5/100 ~= 30`
- _occupancy_icu_: 0.46

## 2. parameters of HospitalGenerator_V2
- _index_: 1200
- _nFloors_: 4
- _huPerFloor_: 13
- _nRows_: 2
- _nColumns_: 4
- _startDateTime_: datetime(2024,1,1,8,0,0)

