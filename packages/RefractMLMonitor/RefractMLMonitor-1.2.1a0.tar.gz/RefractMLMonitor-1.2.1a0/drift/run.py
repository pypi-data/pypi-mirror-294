import json,uuid
from evidently.report import Report
from evidently.metric_preset import TargetDriftPreset,DataDriftPreset
from utility.constants import DataConnector, DriftType, ProblemType
from evidently.pipeline.column_mapping import ColumnMapping
from utility.datasource import DataSource
from utility.drift_util import get_alert_configurations
from utility.constants import AlertParams
from utility.drift_util import generate_alerts,save_drifts_and_alerts, validate_inputs



def execute_drift(session, drift_type,drift_configurations):
    # read datasets for drift execution
    try:
        datasource = DataSource(session, drift_configurations, DataConnector.SNOWFLAKE)
        sf_current, sf_reference = datasource.load_snowflake_datasets()
    except Exception as msg:
        return False, f"Error in loading datasets : {msg}"

    ## drift_score alert configurations
    alert_configurations = drift_configurations["alerts_configurations"] if "alerts_configurations" in drift_configurations else None

    if drift_type == DriftType.FEATURE_DRIFT:
        try:
            # prepare pandas datasets for feature drift
            current, reference = sf_current.to_pandas(), sf_reference.to_pandas()
            feature_columns = drift_configurations["feature_columns"]
            current = current[feature_columns]
            reference = reference[feature_columns]

            # Feature drift execution
            feature_drift_obj = DataDriftPreset()
            data_drift_report = Report(metrics=[feature_drift_obj])
            data_drift_report.run(reference_data=reference, current_data=current,column_mapping=None)
            feature_drift_data = json.loads(data_drift_report.json())

            ## Alert generations
            feature_drift_configs = get_alert_configurations(alert_configurations,AlertParams.DRIFT_SCORE)
            alerts_data,metric_info = generate_alerts(feature_drift_data,feature_drift_configs,drift_type)

            feature_drift_data['metric_info'] = metric_info
            feature_drift_id = str(uuid.uuid4()) 

            ## Save the reports for Alerts & Drifts
            save_drifts_and_alerts(session,
                                feature_drift_data,
                                alerts_data,
                                drift_configurations,
                                drift_type,
                                feature_drift_id)
        except Exception as msg:
            return False, f"Error in feature drift execution : {msg}"
    
        return True,"Feature Drift recipe executed successfully !!"
        
    elif drift_type == DriftType.LABEL_DRIFT:
        try:
            # prepare pandas datasets for label drift
            current, reference = sf_current.to_pandas(), sf_reference.to_pandas()

            # Label drift execution
            column_mapping = ColumnMapping()
            column_mapping.prediction = 'None'
            column_mapping.target = drift_configurations['target_column']
            label_drift_dashboard = Report(metrics=[TargetDriftPreset()])
            label_drift_dashboard.run(reference_data=reference, current_data=current,column_mapping=column_mapping)
            label_drift_output = json.loads(label_drift_dashboard.json())

            # Alert generations
            label_drift_configs = get_alert_configurations(alert_configurations,AlertParams.DRIFT_SCORE)
            alerts_data,metric_info = generate_alerts(label_drift_output,label_drift_configs,drift_type)

            label_drift_output['metric_info'] = metric_info
            label_drift_id = str(uuid.uuid4())

            # Save the reports for Alerts & Drifts
            save_drifts_and_alerts(session,
                                label_drift_output,
                                alerts_data,
                                drift_configurations,
                                drift_type,
                                label_drift_id)
        except Exception as msg:
            return False, f"Error in label drift execution : {msg}"

        return True,"Label Drift recipe executed successfully !!"

    elif drift_type == DriftType.PREDICTION_DRIFT:
        try:
            # prepare pandas datasets for Prediction drift
            current, reference = sf_current.to_pandas(), sf_reference.to_pandas()

            # Prediction drift execution
            column_mapping = ColumnMapping()
            column_mapping.prediction = drift_configurations['target_column']
            column_mapping.target = 'None'
            prediction_drift_dashboard = Report(metrics=[TargetDriftPreset()])
            prediction_drift_dashboard.run(reference_data=reference, current_data=current,column_mapping=column_mapping)
            prediction_drift_output = json.loads(prediction_drift_dashboard.json())

            # Alert generations
            prediction_drift_configs = get_alert_configurations(alert_configurations,AlertParams.DRIFT_SCORE)
            alerts_data,metric_info = generate_alerts(prediction_drift_output,prediction_drift_configs,drift_type)

            prediction_drift_output['metric_info'] = metric_info
            prediction_drift_id = str(uuid.uuid4())

            # Save the reports for Alerts & Drifts
            save_drifts_and_alerts(session,
                                prediction_drift_output,
                                alerts_data,
                                drift_configurations,
                                drift_type,
                                prediction_drift_id)
        except Exception as msg:
            return False, f"Error in prediction drift execution : {msg}"

        return True,"Prediction Drift recipe executed successfully !!"

    elif drift_type == DriftType.MODEL_PERFORMANCE_DRIFT:
        if drift_configurations['problem_type'] == ProblemType.CLASSIFICATION:
            from utility.performance_drift import execute_classification_drift
            try:
                # drift execution
                drift_output = execute_classification_drift(drift_configurations,sf_current,sf_reference)
                
                # alert generations
                performance_alert_configs = get_alert_configurations(alert_configurations,AlertParams.PERFORMANCE_DRIFT_SCORE)
                alerts_data,metric_info = generate_alerts(drift_output,performance_alert_configs,drift_type,ProblemType.CLASSIFICATION)

                drift_output['metric_info'] = metric_info
                drift_id = str(uuid.uuid4())
                
                # saving the reports for Alerts & Drifts
                save_drifts_and_alerts(session,
                                drift_output,
                                alerts_data,
                                drift_configurations,
                                drift_type,
                                drift_id)

            except Exception as msg:
                return False, f"Error in model performance drift execution : {msg}"
            
        elif drift_configurations['problem_type'] == ProblemType.REGRESSION:
            from utility.performance_drift import execute_regression_drift
            try:
                # drift execution
                drift_output = execute_regression_drift(drift_configurations,sf_current,sf_reference)

                # alert generations
                performance_alert_configs = get_alert_configurations(alert_configurations,AlertParams.PERFORMANCE_DRIFT_SCORE)
                alerts_data,metric_info = generate_alerts(drift_output,performance_alert_configs,drift_type,ProblemType.REGRESSION)

                drift_output['metric_info'] = metric_info
                drift_id = str(uuid.uuid4())

                # saving the reports for Alerts & Drifts
                save_drifts_and_alerts(session,
                                drift_output,
                                alerts_data,
                                drift_configurations,
                                drift_type,
                                drift_id)
                

            except Exception as msg:
                return False, f"Error in model performance drift execution : {msg}"
        else:
            return False, "Invalid problem type provided"
        
        return True,"Model Performance Drift recipe executed successfully !! "
    
    else:
        return False, "invalid drift type provided"
