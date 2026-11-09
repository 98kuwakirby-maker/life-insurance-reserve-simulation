# life-insurance-reserve-simulation
Actuarial mathematics simulation of life insurance policy reserves (tV) using Python.
You can enjoy how reserve works changing the interest rate(constant)

DETAIL BELOW

# Life Insurance Reserve Simulation (${}_t V$)

A quantitative finance and actuarial simulation modeling the prospective policy reserve (${}_t V$) for a cohort of policyholders from age 40 onward.

## Mathematical & Actuarial Background
* **Mortality Law:** Utilizes realistic mortality rates ($\mu_x$) and survival probabilities (${}_t p_x$) based on a standard select-and-ultimate life table.
* **Premium & Interest:** Computes continuous life insurance premiums ($\bar{A}_x$) and annual annuity-due factors ($\ddot{a}_x$) under a constant force of interest ($\delta = \ln(1+i)$).
* **Stochastic Simulation:** Simulates individual policyholder death events across discrete time increments ($\Delta t$) and tracks the evolution of the aggregate reserve fund dynamically.

## Tech Stack
* **Language:** Python
