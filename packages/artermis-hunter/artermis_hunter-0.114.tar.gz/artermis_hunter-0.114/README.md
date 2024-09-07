# Artemis Hunter
* note the setup steps described here are being beta-tested.

## This package does automated vulnerability enumeration and recommends exploits.<br><br>

### How to Run on Non Kali-Linux Operating System (Recommended)
* Clone repo
* cd into repo
* Build image

    ```
    docker build -t artemis .
    ```
* Run as terminal inside container
  ```
  docker run -ti -v ${PWD}:/root/repo artemis
  ```

* Run Artemis

  ```
  artemis_hunter 
  ```
  
---  

### How to Run on Kali-Linux Operating System
* Install Artemis Python Package

    ```
    pip install artemis_hunter
    ```
* Run Artemis
  ```
  artemis_hunter 
  ```