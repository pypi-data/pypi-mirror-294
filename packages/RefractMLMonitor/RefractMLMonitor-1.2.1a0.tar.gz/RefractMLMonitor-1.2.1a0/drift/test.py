
import pathlib,shutil,os,sys
import pandas as pd

from run import execute_drift

def remove_cache_files():
    for i in pathlib.Path(".").rglob("__pycache__"):
        print(i)
        shutil.rmtree(i)

def test_snowflake_recipes(session, drift_configs, drift_type):
    '''
    To test and execute the drift recipes using snowflake session
    '''
    status, response = execute_drift(session, drift_type= drift_type, drift_configurations=drift_configs)
    if not status:
        print(f"Error in executing {drift_type} recipe",response)

    print(response)

def is_table_exists(session,MODEL_MONITOR):
    query = f"""
    SHOW TABLES LIKE '{MODEL_MONITOR}';
    """
    result = session.sql(query).collect()
    return len(result) > 0

if __name__ == "__main__" :
    # remove_cache_files()
    # exit()
    from snowflake.snowpark import Session
    CONNECTION_PARAMETERS = {
        }
    
    session = Session.builder.configs(CONNECTION_PARAMETERS).create()

    model_monitor_table = "MODEL_MONITORING"
    model_alerts_table = "MODEL_ALERTS"

    if not is_table_exists(session,model_monitor_table):
        '''
        create drift table if not exists
        '''
        query = f"""
            CREATE TABLE IF NOT EXISTS {model_monitor_table} (
                    object_id STRING PRIMARY KEY DEFAULT UUID_STRING(),
                    model_name STRING,
                    version_name STRING,
                    object_type STRING,
                    object_data VARIANT ,
                    created_at TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP(),
                    created_by STRING
                );
        """
        session.sql(query).collect()
        print("created drift table")

    if not is_table_exists(session,model_alerts_table):
        '''
        create alert table if not exists
        '''
        query = f"""
                CREATE TABLE IF NOT EXISTS {model_alerts_table} (
                object_id STRING PRIMARY KEY,
                model_name STRING,
                version_name STRING,
                drift_type STRING,
                created_at TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP(),
                alert_data VARIANT,
                FOREIGN KEY (object_id) REFERENCES model_reports(object_id)
            );
        """
        session.sql(query).collect()
        print("created alert table")

    # sf_dataframe = session.create_dataframe(pd.read_csv("reference_loan.csv"))
    # sf_dataframe.write.mode("overwrite").save_as_table("refence_loan")

    driftype = "model_performance_drift"  # model_performance_drift, feature_drift, label_drift, prediction_drift
    drift_configs = {
        "project_id" : "asvw4g124-124sdvrgwef",
        "feature_columns": ["SATISFACTION_LEVEL", "LAST_EVALUATION", "AVERAGE_MONTLY_HOURS","PROMOTION_LAST_5YEARS"],
        "current_dataset" : "reference_loan",
        "reference_dataset" : "reference_loan",
        "model_name" : "HR_CHURN_MODEL",
        "problem_type" : "classification",  # classification or regression
        "target_column" : "LOAN_STATUS",
        "prediction_column" : "PREDICTION",
        "predict_probability_columns" : ['NOT_DEFAULT', 'DEFAULT'],
        "version_name" : "V2",
        "alerts_configurations" : [
            {
                "parameter": "performance_drift_score",
                "threshold_range": [[0.5, 1,'Red'],[0.5, 1,'Amber'],[0.5, 1,'Green']]
            },
            {
                "parameter": "drift_score",
                "threshold_range": [[0.5, 1,'Red'],[0.5, 1,'Amber'],[0.5, 1,'Green']]
            }
        ]
    }

    drift_configs['created_by'] = "mahesh.10698046@ltimindtree.com"
    
    test_snowflake_recipes(session=session, drift_configs=drift_configs, drift_type=driftype)