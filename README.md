# mtdl-stock-market-price
Quirky data pipeline for extract the Metrodata's stock price from an API, load it to staging area, and do transformation and load it in data warehouse

---

## Language And Data Platform
* For manage data container, writer use `Docker`
* For orchestrate data pipeline, writer use `Airflow`
* For write the scripts, writer use `Python`
* For extract and load the data into staging area & data warehouse, writer use `PostgreSQL`
* For visualize the stock data from data warehouse, writer use `Metabase`
---

## Application
* For write the scripts and manage file management, writer use `VSCode`
* For manage and check the databases, writer use `DBeaver`
* For manage data container, writer use `Docker Desktop`
---

## File Management Setup
1. **mtdl-stock-market-price** folder's contain:
    * `data`: Stock data folders
    * `documentations`: System architecture of data pipeline folders
    * `elt/airflow`: The data platform folders which is used to perform extract-load-transform data pipeline, along with the platform setup
    * `notebooks`: The Jupyter Notebooks folders that contains how to setup the yfinance API and how to predict stock price using certain algorithm
2. In `elt/airflow` folder's contain:
    * `config`: This folder contains Airflow's configuration. For now it's empty
    * `dags`: This folder contains directed acyclic graph (DAG) scripts to run and trigger the pipeline
    * `include`: This folder contains any other files you’d like to include (txt files, SQL query, and so on)
    * `logs`: This folder contains log when the data pipeline is running
    * `plugins`: This folder contains any custom custom operators. For now it's empty
    * `docker-compose.yaml`: This file is to set up and run Airflow
    * `Dockerfile`: This file is to install any dependencies in `requirements.txt` to run the Airflow
    * `requirements.txt` : This file contains any dependencies 

## Docker Setup
1. Install Docker Desktop and Open `Docker Desktop Installer.exe`
2. When prompted, ensure the Use WSL 2 instead of Hyper-V option on the Configuration page is selected or not depending on your choice of backend
3. Follow the instructions on the installation wizard to authorize the installer and proceed with the install
4. When the installation is successful, select Close to complete the installation process
---

## Airflow Setup and Run
1. Install airflow for Airflow in this command:
```
pip install apache-airflow
```
2. Create `docker-compose.yaml`, `Dockerfile`, and `requirements.txt` files base on folder **`mtdl_stock_market_price/etl/airflow`**
3. To run airflow, you can use this command in terminal
```
docker-compose up -d
```

4. To close Airflow, you can use this command in terminal
```
docker-compose down
```
---

## PostgreSQL Setup and Run
1. Install `PostgreSQL`
2. Install `DBeaver` from this [link](https://dbeaver.io/)
3. Make a PostgreSQL connection on `DBeaver` called `postgres`
4. Make a database called `metrodata` for staging area and `metrodata_prod` for data warehouse
5. `PostgreSQL` always run in the background
---

## System Architecture
![System Architecture](https://github.com/syauqikhosyi/mtdl-stock-market-price/blob/main/documentations/System-Architecture.png)

---

## Additional Resources
This repo has several reference sources for working on it:
* [Hands On Apache Airflow in Data Engineer](https://github.com/saipulrx/de-basic-class-airflow)
* [Getting started with Airflow in 10 mins](https://marclamberti.com/blog/getting-started-airflow/)
* [Simple data pipeline](https://github.com/goFrendiAsgard/platform-data)