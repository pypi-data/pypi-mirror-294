import os,json,re
from typing import Final
from evidently.metric_preset import TargetDriftPreset,RegressionPreset
from evidently.metric_preset import *
from pandas import DataFrame
from evidently.metrics import *
from utility.constants import ProblemType, DriftType
from utility.constants import AlertParams


def get_alert_status(drift_score,alerts_threshold_range):
    status = None
    for item in alerts_threshold_range:
        if drift_score >= item[0] and drift_score <= item[1]:
            severity_map = {
                "Red" : "Poor",
                "Amber" : "Moderate",
                "Green" : "Good"
            }
            status = severity_map[item[2]]
            break
        elif drift_score > item[1] and item[2] == 'Red':
            status = 'Poor'
            break
        elif drift_score < item[0] and item[2] == 'Green':
            status = 'Good'
            break
        else:
            status = 'Moderate'
    return status

def combined_alert_status(alert_statuses:list):
    if all([status == 'Good' for status in alert_statuses]):
        return 'Good'
    elif any([status == 'Poor' for status in alert_statuses]):
        return 'Poor'
    else:
        return 'Moderate'
    
def save_drifts_and_alerts(session,
                           drift_output:dict,
                           alert_json:dict,
                           drift_configs:dict,
                           drift_type:str,
                           drift_id:str):
    
    model_monitor_table = "MODEL_MONITORING"
    model_alerts_table = "MODEL_ALERTS"
    '''
    To save drift_ouput to MODEL_MONITORING table and  alert_json to MODEL_ALERTS table
    '''
    ## saving drift output
    try:
        query = f"""
            INSERT INTO {model_monitor_table} 
                (object_id, model_name, version_name, object_type, object_data, created_by)
            SELECT 
                '{drift_id}' AS object_id,
                '{drift_configs["model_name"]}' AS model_name,
                '{drift_configs["version_name"]}' AS version_name,
                '{drift_type}' AS object_type,
                parse_json('{json.dumps(drift_output)}') AS object_data,
                '{drift_configs["created_by"]}' AS created_by;
"""
        ## commiting the query
        session.sql(query).collect()

        ## saving alert data
        query = f"""
        INSERT INTO {model_alerts_table} (object_id, model_name,version_name,drift_type,alert_data)
            SELECT  
            '{drift_id}' AS object_id,
            '{drift_configs["model_name"]}' AS model_name,
            '{drift_configs["version_name"]}' AS version_name,
            '{drift_type}' AS drift_type,
             parse_json('{json.dumps(alert_json)}') AS alert_data ;
        """
        if alert_json :
            ## commiting the query
            session.sql(query).collect()
            
    except Exception as msg:
        print(msg)
        raise Exception("Failed to save drift output and alert data")


def feature_drift_alerts(drift_output,alert_configs) :
    metrics = [metric for metric in drift_output["metrics"] if metric['metric']=="DatasetDriftMetric"][0]
    drift_score = metrics["result"]["share_of_drifted_columns"]
    actual_columns = metrics["result"]["number_of_columns"]
    drifted_columns = metrics["result"]["number_of_drifted_columns"]
    message  = f"Drift is detected for {drift_score*100}% of columns ({drifted_columns} out of {actual_columns})."
    feature_drift_status = None

    ## metric.json
    metric_info = {
        "DRIFT_SCORE" : round(drift_score,4)
    }
    
    if len(alert_configs) == 0:
        return {},metric_info

    feature_drift_alert_data = [item for item in alert_configs if item["parameter"]=="drift_score"][0]
    alerts_threshold_range = feature_drift_alert_data["threshold_range"]
    feature_drift_status = get_alert_status(drift_score,alerts_threshold_range)

    ## alert.json
    alert_data = {
            "alert_data": {
                "recipe": "feature_drift",
                "metrics": {
                    "feature_drift": round(drift_score,4)
                    },
                "status": feature_drift_status,
                "ui_value" : str(round(drift_score,4)),
                "message": message
                },
                "ai-backend-metadata": {
                "feature_drift_flag": feature_drift_status
            }
    }
    return alert_data,metric_info


def target_drift_alerts(drift_output,alert_configs,drit_type):
    metrics = [metric for metric in drift_output['metrics'] if metric["metric"]=="ColumnDriftMetric"][0]
    drift_score = metrics["result"]["drift_score"]
    drift_detected = metrics["result"]["drift_detected"]
    detection_method = metrics["result"]["stattest_name"]
    message = f"Drift detected. Drift detection method: {detection_method}. Drift score: {drift_score}" if drift_detected else f"Data drift not detected. Drift detection method: {detection_method}. Drift score: {drift_score}"
    drift_status = None
    
    if len(alert_configs) == 0:
        return {},metric_info

    # metric.json
    metric_info = {
        "DRIFT_SCORE" : round(drift_score,4)
    }

    drift_alert_data = [item for item in alert_configs if item["parameter"]=="drift_score"][0]
    alerts_threshold_range = drift_alert_data["threshold_range"]
    drift_status = get_alert_status(drift_score,alerts_threshold_range)

    # alert.json
    alert_data = {
            "alert_data": {
                "recipe": drit_type,
                "metrics": {
                    "score": drift_score
                    },
                "status": drift_status,
                "message": message,
                "ui_value" : drift_status,
                },
                "ai-backend-metadata": {
                "prediction_drift_flag": drift_status
            }
        }
    
    return alert_data,metric_info

def model_performance_drift_alerts(drift_output,alert_configs,problem_type="classification"):
    if problem_type == ProblemType.CLASSIFICATION:
        current_quality_metrics = [item for item in drift_output["metrics"] if "classification_quality_metrics" in item][0]["classification_quality_metrics"]["current"]
        reference_quality_metrics = [item for item in drift_output["metrics"] if "classification_quality_metrics" in item][0]["classification_quality_metrics"]["reference"]
        
        # performance metrics
        cu_accuracy_score = current_quality_metrics["accuracy_score"]; re_accuracy_score = reference_quality_metrics["accuracy_score"]
        cu_f1_score = current_quality_metrics["f1_score"]; re_f1_score = reference_quality_metrics["f1_score"]
        cu_precision_score = current_quality_metrics["precision_score"]; re_precision_score = reference_quality_metrics["precision_score"]
        cu_recall_score = current_quality_metrics["recall_score"]; re_recall_score = reference_quality_metrics["recall_score"]

        #alert message
        accuracy_message = f"Accuracy has improved by {round((cu_accuracy_score-re_accuracy_score)/re_accuracy_score*100,2)}% from {round(re_accuracy_score,3)} to {round(cu_accuracy_score,3)}." if cu_accuracy_score > re_accuracy_score else "No change found in Accuracy." if cu_accuracy_score == re_accuracy_score else f"Accuracy has decreased by {round((cu_accuracy_score-re_accuracy_score)/re_accuracy_score*100,2)}% from {round(re_accuracy_score,3)} to {round(cu_accuracy_score,3)}."
        f1_message = f"F1 Score has improved by {round((cu_f1_score-re_f1_score)/re_f1_score*100,2)}% from {round(re_f1_score,3)} to {round(cu_f1_score,3)}." if cu_f1_score > re_f1_score else "No change found in F1 Score." if cu_f1_score == re_f1_score else f"F1 Score has decreased by {round((cu_f1_score-re_f1_score)/re_f1_score*100,2)}% from {round(re_f1_score,3)} to {round(cu_f1_score,3)}."
        precision_message = f"Precision has improved by {round((cu_precision_score-re_precision_score)/re_precision_score*100,2)}% from {round(re_precision_score,3)} to {round(cu_precision_score,3)}." if cu_precision_score > re_precision_score else "No change found in Precision." if cu_precision_score == re_precision_score else f"Precision has decreased by {round((cu_precision_score-re_precision_score)/re_precision_score*100,2)}% from {round(re_precision_score,3)} to {round(cu_precision_score,3)}."
        recall_message = f"Recall has improved by {round((cu_recall_score-re_recall_score)/re_recall_score*100,2)}% from {round(re_recall_score,3)} to {round(cu_recall_score,3)}." if cu_recall_score > re_recall_score else "No change found in Recall." if cu_recall_score == re_recall_score else f"Recall has decreased by {round((cu_recall_score-re_recall_score)/re_recall_score*100,2)}% from {round(re_recall_score,3)} to {round(cu_recall_score,3)}."
      
        #metrics.json
        metric_info = {
            "ACCURACY": cu_accuracy_score,
            "F1_SCORE": cu_f1_score,
            "PRECISION": cu_precision_score,
            "RECALL": cu_recall_score
        }

        if len(alert_configs) == 0:
            return {},metric_info
        
        drift_alert_data = [item for item in alert_configs if item["parameter"]=="performance_drift_score"][0]
        alerts_threshold_range = drift_alert_data["threshold_range"]
        accuracy_status = get_alert_status(cu_accuracy_score,alerts_threshold_range)
        precision_status = get_alert_status(cu_precision_score,alerts_threshold_range)
        recall_status = get_alert_status(cu_recall_score,alerts_threshold_range)
        f1_status = get_alert_status(cu_f1_score,alerts_threshold_range)

        all_status = [accuracy_status,precision_status,recall_status,f1_status]

        overall_drift_status = combined_alert_status(all_status)
        overall_drift_message = f"{accuracy_message},{precision_message},{recall_message} and {f1_message}."

        # alert.json
        alert_data = {
            "alert_data": {
                "recipe": DriftType.MODEL_PERFORMANCE_DRIFT,
                "metrics": {
                    "accuracy": cu_accuracy_score,
                    "accuracy_drift" : f"+{round((cu_accuracy_score-re_accuracy_score)/re_accuracy_score*100,2)}%" if cu_accuracy_score > re_accuracy_score else "0%" if cu_accuracy_score == re_accuracy_score else f"-{round((cu_accuracy_score-re_accuracy_score)/re_accuracy_score*100,2)}%",
                    "accuracy_status" : accuracy_status,

                    "precision": cu_precision_score,
                    "precision_drift" : f"+{round((cu_precision_score-re_precision_score)/re_precision_score*100,2)}%" if cu_precision_score > re_precision_score else "0%" if cu_precision_score == re_precision_score else f"-{round((cu_precision_score-re_precision_score)/re_precision_score*100,2)}%",
                    "precision_status" : precision_status,

                    "recall": cu_recall_score,
                    "recall_drift" : f"+{round((cu_recall_score-re_recall_score)/re_recall_score*100,2)}%" if cu_recall_score > re_recall_score else "0%" if cu_recall_score == re_recall_score else f"-{round((cu_recall_score-re_recall_score)/re_recall_score*100,2)}%",
                    "recall_status" : recall_status,

                    "f1_value": cu_f1_score,
                    "f1_score_drift" : f"+{round((cu_f1_score-re_f1_score)/re_f1_score*100,2)}%" if cu_f1_score > re_f1_score else "0%" if cu_f1_score == re_f1_score else f"-{round((cu_f1_score-re_f1_score)/re_f1_score*100,2)}%",
                    "f1_status" : f1_status
                    },
                "status": overall_drift_status,
                "message": overall_drift_message,
                "ui_value" : overall_drift_status
                },
                "ai-backend-metadata": {
                "model_performance_flag": overall_drift_status
            }
        }

        return alert_data,metric_info
    else:
        current_quality_metrics = [item for item in drift_output["metrics"] if "regression_quality_metrics" in item ][0]["regression_quality_metrics"]["current"]
        reference_quality_metrics = [item for item in drift_output["metrics"] if "regression_quality_metrics" in item][0]["regression_quality_metrics"]["reference"]

        # performance metrics
        cu_mean_abs_error = current_quality_metrics["mean_absolute_error"]; re_mean_abs_error = reference_quality_metrics["mean_absolute_error"]
        cu_evs = current_quality_metrics["explained_variance_score"]; re_evs = reference_quality_metrics["explained_variance_score"]
        cu_r2_score = current_quality_metrics["r2_score"]; re_r2_score = reference_quality_metrics["r2_score"]

        #alert message
        cu_mean_abs_message = f"Mean Absolute Error has increased by {round((cu_mean_abs_error-re_mean_abs_error)/re_mean_abs_error*100,2)}% from {round(re_mean_abs_error,3)} to {round(cu_mean_abs_error,3)}." if cu_mean_abs_error > re_mean_abs_error else "No change found in Mean Absolute Error." if cu_mean_abs_error == re_mean_abs_error else f"Mean Absolute Error has decreased by {round((cu_mean_abs_error-re_mean_abs_error)/re_mean_abs_error*100,2)}% from {round(re_mean_abs_error,3)} to {round(cu_mean_abs_error,3)}."
        cu_evs_message = f"Explained Variance Score has increased by {round((cu_evs-re_evs)/re_evs*100,2)}% from {round(re_evs,3)} to {round(cu_evs,3)}." if cu_evs > re_evs else "No change found in Explained Variance Score." if cu_evs == re_evs else f"Explained Variance Score has decreased by {round((cu_evs-re_evs)/re_evs*100,2)}% from {round(re_evs,3)} to {round(cu_evs,3)}."
        cu_r2_message = f"R2 Score has increased by {round((cu_r2_score-re_r2_score)/re_r2_score*100,2)}% from {round(re_r2_score,3)} to {round(cu_r2_score,3)}." if cu_r2_score > re_r2_score else "No change found in R2 Score." if cu_r2_score == re_r2_score else f"R2 Score has decreased by {round((cu_r2_score-re_r2_score)/re_r2_score*100,2)}% from {round(re_r2_score,3)} to {round(cu_r2_score,3)}."

        #metrics.json
        metric_info = {
            "MEAN_ABS_ERROR": cu_mean_abs_error,
            "EXPLAINED_VARIANCE_SCORE": cu_evs,
            "R2_SCORE": cu_r2_score
        }

        if len(alert_configs) == 0:
            return {},metric_info
        
        # alert.json
        drift_alert_data = [item for item in alert_configs if item["parameter"]=="performance_drift_score"][0]
        alerts_threshold_range = drift_alert_data["threshold_range"]
        mean_abs_error_status = get_alert_status(cu_mean_abs_error,alerts_threshold_range)
        evs_status = get_alert_status(cu_evs,alerts_threshold_range)
        r2_status = get_alert_status(cu_r2_score,alerts_threshold_range)

        all_status = [mean_abs_error_status,evs_status,r2_status]
        overall_drift_status = combined_alert_status(all_status)
        overall_drift_message = f"{cu_mean_abs_message},{cu_evs_message} and {cu_r2_message}."

        alert_data = {
            "alert_data": {
                "recipe": DriftType.MODEL_PERFORMANCE_DRIFT,
                "metrics": {
                    "mean_abs_error": cu_mean_abs_error,
                    "mean_abs_error_drift" : f"+{round((cu_mean_abs_error-re_mean_abs_error)/re_mean_abs_error*100,2)}%" if cu_mean_abs_error > re_mean_abs_error else "0%" if cu_mean_abs_error == re_mean_abs_error else f"-{round((cu_mean_abs_error-re_mean_abs_error)/re_mean_abs_error*100,2)}%",
                    "mean_abs_error_status" : mean_abs_error_status,

                    "evs": cu_evs,
                    "evs_drift" : f"+{round((cu_evs-re_evs)/re_evs*100,2)}%" if cu_evs > re_evs else "0%" if cu_evs == re_evs else f"-{round((cu_evs-re_evs)/re_evs*100,2)}%",
                    "evs_status" : evs_status,

                    "r2_score": cu_r2_score,
                    "r2_score_drift" : f"+{round((cu_r2_score-re_r2_score)/re_r2_score*100,2)}%" if cu_r2_score > re_r2_score else "0%" if cu_r2_score == re_r2_score else f"-{round((cu_r2_score-re_r2_score)/re_r2_score*100,2)}%",
                    "r2_status" : r2_status

                    },
                "status": overall_drift_status,
                "message": overall_drift_message,
                "ui_value" : overall_drift_status
                },
                "ai-backend-metadata": {
                "model_performance_flag": overall_drift_status
            }
        }

        return alert_data,metric_info


def generate_alerts(drift_output,alert_configs,drift_type,problem_type="classification"):
    '''
    drift_output : dict
    alert_configs : dict
    return alerts : dict
    Based on alert_configs, generate alerts using data from drift_output
    '''
    if drift_type == DriftType.FEATURE_DRIFT:
        return feature_drift_alerts(drift_output,alert_configs)
    elif drift_type == DriftType.LABEL_DRIFT:
        return target_drift_alerts(drift_output,alert_configs,drift_type)
    elif drift_type == DriftType.MODEL_PERFORMANCE_DRIFT:
        return model_performance_drift_alerts(drift_output,alert_configs,problem_type)
    elif drift_type == DriftType.PREDICTION_DRIFT:
        return target_drift_alerts(drift_output,alert_configs,drift_type)
    else:
        return None


def validate_inputs(temp:list):
    for item in temp:
        if not all([any([
                        isinstance(item[0],int),
                        isinstance(item[0],float),
                        ]),
                    any([
                        isinstance(item[1],int),
                        isinstance(item[1],float),
                        ])
                    ]
                    ):
            raise Exception("Alert thresholds should of type int or float")
        
        if not all([0 <= item[0] <= 1,0 <= item[1] <= 1]):
            raise Exception("threshold input range should be between 0 and 1")
        
def get_alert_configurations(alert_configurations,alert_param):
    '''
    To fetch the alert configurations for given list of alerts params
    sample :
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
    output : []
    '''

    alert_configuration = []
    for alert_info in alert_configurations:
        if alert_info["parameter"] == alert_param :
            validate_inputs(alert_info["threshold_range"])
            alert_configuration.append(alert_info)

    return alert_configuration
