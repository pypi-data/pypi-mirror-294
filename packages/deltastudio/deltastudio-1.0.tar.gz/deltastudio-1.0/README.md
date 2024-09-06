# Delta Studio

> ***Note: This project is under active development. Use with caution!***



##  A Jupyter-Lab approach to an End-to-End data platform

- [x] Core functionality

- [x] Custom Metastore

- [x] Authentication and Authorization

- [x] Data Quality module

  


This project is essentially a **customized Apache Spark computational engine**, leveraging **Delta Lake as a storage system**, and complemented with additional features tailored for **data warehousing needs**. My goal with this project is to create a **low-code platform**, equipped with the necessary functionalities for `business intelligence` (BI) processes, `data quality` testing operations, as well as the implementing of `machine learning` models and `statistical computations`. 

This project includes features for user **authentication** and **authorization**, creating databases, tables, and views along with their access levels, using standard SQL, and a set of pre-built methods for common ETL and data quality tasks. At the same time, users will have unrestricted access to all the capabilities of **PySpark**, **Spark SQL**, and the ability to use a variety of **Python libraries** for various tasks.

------

## How to setup

1. Build the docker image
   1. `cd into the project directory`
   2. `docker build -t delta:0.1 .`
4. Run the compose file
   1. `docker compose -f delta.yml up -d`

Now you should be able to access the Jupyter Lab interface at `localhost` . Use `deltastudio` as the password for Jupyter. I'm using the following technologies:

- **Apache Spark** (PySpark, Spark SQL): version 4 with Java version 17
- **Delta Lake** (storage): version 4
- **Jupyter Lab** (and some of its extensions, as an interface for the user)
- **PostgreSQL** (to build a custom Metastore): latest
- **DuckDB** (as a fast OLAP layer and also reading Delta tables): latest
- **Voila** and **Dash** for visualizations

In order to **orchestrate your notebooks and create Jobs**, you can use Jupyter Lab extension to schedule notebooks.

For **visualizations**, I recommend to use `Voila` as this is a Jupyter-Lab first approach. Also there are other options like `Dash`.

------

In case of any issues or bugs, I would be more than happy to help you mortezahajipour.works@gmail.com

**MIT License**
