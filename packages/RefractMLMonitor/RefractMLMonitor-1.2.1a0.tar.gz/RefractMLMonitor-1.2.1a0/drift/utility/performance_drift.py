
import pandas as pd
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, try_cast, when, cast
from sklearn.datasets import load_diabetes
import json
from snowflake.ml.modeling.metrics import (confusion_matrix,
                                                accuracy_score,
                                                f1_score, recall_score,
                                                precision_score,
                                                log_loss ,
                                                roc_auc_score ,
                                            )

from snowflake.ml.modeling.metrics import explained_variance_score, \
                    mean_absolute_percentage_error ,\
					mean_squared_error, \
					mean_absolute_error, \
					r2_score


def map_to_numeric_col(df,col_name,mapping_data,mapped_col_name):
    columns_map = {col:index for index,col in enumerate(mapping_data)}
    mapped_col = col(col_name)
    for category, value in columns_map.items():
        mapped_col = when(col(col_name) == category,value).otherwise(mapped_col)

    df = df.with_column(mapped_col_name, mapped_col)
    return df

def is_numeric_col(df,col_name):
    status = True
    try:
        df_numeric_col_count = df.with_column("converted_column",try_cast(col(col_name),"INTEGER")) \
                                                    .filter(col("converted_column").is_not_null()).count()
        if not df_numeric_col_count == df.count():
            status = False
    except :
        pass

    try:
        df_numeric_col_count = df.with_column("converted_column",cast(col(col_name),"INTEGER")) \
                                                    .filter(col("converted_column").is_not_null()).count()
        if not df_numeric_col_count == df.count():
            status = False
    except :
        pass

    return status

def get_classification_metrics(sf_df,true_cn,pred_cn,drift_configs):
    quality_metrics = {}
    no_classes = len(drift_configs['predict_probability_columns'])
    average='weighted' if no_classes > 2 else 'binary'
    quality_metrics['accuracy_score'] = accuracy_score(df=sf_df,y_true_col_names=true_cn, y_pred_col_names=pred_cn)
    quality_metrics['f1_score'] = f1_score(df= sf_df,y_true_col_names=true_cn, y_pred_col_names=pred_cn,average=average)
    quality_metrics['recall_score'] = recall_score(df=sf_df,y_true_col_names=true_cn, 
                                                y_pred_col_names=pred_cn,average=average)
    quality_metrics['precision_score'] = precision_score(df=sf_df,
                                                        y_true_col_names=true_cn,
                                                        y_pred_col_names=pred_cn,
                                                        average=average)
    quality_metrics['log_loss'] = log_loss(df=sf_df,y_true_col_names=true_cn, y_pred_col_names=pred_cn)
    if no_classes > 2 :
        quality_metrics['roc_auc_score'] = roc_auc_score(df=sf_df, 
                                                        y_true_col_names=true_cn,
                                                        y_score_col_names=drift_configs['predict_probability_columns'].keys(), 
                                                        multi_class='ovr',average=None).tolist()
    elif no_classes == 2 :
        quality_metrics['roc_auc_score'] = roc_auc_score(df=sf_df, 
                                                        y_true_col_names=true_cn, 
                                                        y_score_col_names=pred_cn ,average="macro").tolist()
    else:
        quality_metrics['roc_auc_score'] = None
                
    quality_metrics['gini'] = round((2*quality_metrics['roc_auc_score'])-1, 3) if quality_metrics['roc_auc_score'] else None

    return quality_metrics

def get_class_representation(df,target_column,prediction_column,drift_configs):
    class_count_dict = {}
    mapping_data = {index:col for index,col in enumerate(drift_configs['predict_probability_columns'])}
    temp_target_df  = df.group_by(col(target_column)).count()
    class_count_dict[drift_configs['target_column']] = {mapping_data[int(row[target_column])]:row['COUNT'] for row in temp_target_df.collect()}
    temp_prediction_df  = df.group_by(col(prediction_column)).count()
    class_count_dict[drift_configs['prediction_column']] = {mapping_data[int(row[prediction_column])]:row['COUNT'] for row in temp_prediction_df.collect()}
    return class_count_dict



def execute_classification_drift(drift_configs,
                                 sf_current,
                                 sf_reference):
    
    #################### Classification Drift Metrics #############################
    classification_quality_metrics = {}
    
    if not is_numeric_col(sf_current,drift_configs['target_column']):
        mapped_target_col_name = drift_configs['target_column'] + '_NUMERIC'
        sf_current = map_to_numeric_col(sf_current,
                                        drift_configs['target_column'],
                                        drift_configs['predict_probability_columns'],
                                        mapped_target_col_name)
        sf_reference = map_to_numeric_col(sf_reference,
                                        drift_configs['target_column'],
                                        drift_configs['predict_probability_columns'],
                                        mapped_target_col_name)
        drift_configs['categorical_target_col'] = drift_configs['target_column'] 
        drift_configs['numeric_target_col'] = mapped_target_col_name
    else:
        drift_configs['numeric_target_col'] = drift_configs['target_column']


    if not is_numeric_col(sf_current,drift_configs['prediction_column']):
        mapped_prediction_col_name = drift_configs['prediction_column'] + '_NUMERIC'
        sf_current = map_to_numeric_col(sf_current,
                                        drift_configs['prediction_column'],
                                        drift_configs['predict_probability_columns'],
                                        mapped_prediction_col_name)
        sf_reference = map_to_numeric_col(sf_reference,
                                        drift_configs['prediction_column'],
                                        drift_configs['predict_probability_columns'],
                                        mapped_prediction_col_name)
        drift_configs['categorical_prediction_col'] = drift_configs['prediction_column']
        drift_configs['numeric_prediction_col'] = mapped_prediction_col_name
    else:
        drift_configs['numeric_prediction_col'] = drift_configs['prediction_column']

        
    metrics = []
    numeric_target_col = drift_configs['numeric_target_col']
    numeric_prediction_col = drift_configs['numeric_prediction_col']

    ## Performance metrics
    classification_quality_metrics['current'] = get_classification_metrics(sf_current,numeric_target_col,numeric_prediction_col,drift_configs)
    classification_quality_metrics['reference'] = get_classification_metrics(sf_reference,numeric_target_col,numeric_prediction_col,drift_configs)
    metrics.append({
        "classification_quality_metrics" : classification_quality_metrics
    })


    ## Class Representation
    class_representation = {}
    class_representation['current'] = get_class_representation(sf_current,numeric_target_col,numeric_prediction_col,drift_configs)
    class_representation['reference'] = get_class_representation(sf_reference,numeric_target_col,numeric_prediction_col,drift_configs)
    metrics.append({
        "class_representation" : class_representation
    })


    ## Confusion Matrix
    current_confusion_matrix = confusion_matrix(df=sf_current, y_true_col_name=numeric_target_col, y_pred_col_name=numeric_prediction_col).tolist()
    reference_confusion_matrix = confusion_matrix(df=sf_reference, y_true_col_name=numeric_target_col, y_pred_col_name=numeric_prediction_col).tolist()
    metrics.append({
        "confusion_matrix" : {'current':current_confusion_matrix,'reference':reference_confusion_matrix}
    })

    ## Quality Metrics by class
    quality_metrics_by_class = {}
    current_class_metrics = {} ; reference_class_metrics = {}
    
    for i,class_name in enumerate(drift_configs['predict_probability_columns']):
        cu_class_metrics = {} 
        cu_tp = current_confusion_matrix[i][i]
        cu_fp = sum([row[i] for row in current_confusion_matrix])-cu_tp
        cu_fn = sum(current_confusion_matrix[i])-cu_tp
        cu_tn = sf_current.count() - cu_tp - cu_fp - cu_fn
        cu_class_metrics['precision_score'] = cu_tp/(cu_tp+cu_fp) if (cu_tp+cu_fp) > 0 else 0
        cu_class_metrics['recall_score'] = cu_tp/(cu_tp+cu_fn) if (cu_tp+cu_fn) > 0 else 0
        cu_class_metrics['f1_score'] = 2*(cu_class_metrics['precision_score']*cu_class_metrics['recall_score'])/(cu_class_metrics['precision_score']+cu_class_metrics['recall_score']) if (cu_class_metrics['precision_score']+cu_class_metrics['recall_score']) > 0 else 0
        cu_class_metrics['accuracy_score'] = (cu_tp+cu_tn)/(cu_tp+cu_fp+cu_fn+cu_tn)
        current_class_metrics[class_name] = cu_class_metrics

        re_class_metrics = {}
        re_tp = reference_confusion_matrix[i][i]
        re_fp = sum([row[i] for row in reference_confusion_matrix])-re_tp
        re_fn = sum(reference_confusion_matrix[i])-re_tp
        re_tn = sf_reference.count() - re_tp - re_fp - re_fn
        re_class_metrics['precision_score'] = re_tp/(re_tp+re_fp) if (re_tp+re_fp) > 0 else 0
        re_class_metrics['recall_score'] = re_tp/(re_tp+re_fn) if (re_tp+re_fn) > 0 else 0
        re_class_metrics['f1_score'] = 2*(re_class_metrics['precision_score']*re_class_metrics['recall_score'])/(re_class_metrics['precision_score']+re_class_metrics['recall_score']) if (re_class_metrics['precision_score']+re_class_metrics['recall_score']) > 0 else 0
        re_class_metrics['accuracy_score'] = (re_tp+re_tn)/(re_tp+re_fp+re_fn+re_tn)
        reference_class_metrics[class_name] = re_class_metrics
    
    quality_metrics_by_class['current'] = current_class_metrics
    quality_metrics_by_class['reference'] = reference_class_metrics
    metrics.append({
        "quality_metrics_by_class" : quality_metrics_by_class}
        )

    return {
        "metrics" : metrics
    }



#####################
#####################

def get_regression_metrics(sf_df,true_cn,pred_cn):
    import math
    performance_metrics = {}
    performance_metrics['explained_variance_score'] = explained_variance_score(df=sf_df,
                                                                               y_true_col_names=true_cn,
                                                                               y_pred_col_names=pred_cn)

    performance_metrics['mean_absolute_percentage_error'] = mean_absolute_percentage_error(df=sf_df,
                                                                                            y_true_col_names=true_cn,
                                                                                            y_pred_col_names=pred_cn)

    performance_metrics['mean_squared_error'] = mean_squared_error(df=sf_df,
                                                                    y_true_col_names=true_cn, 
                                                                    y_pred_col_names=pred_cn)

    performance_metrics['mean_absolute_error'] = mean_absolute_error(df=sf_df,
                                                                        y_true_col_names=true_cn, 
                                                                        y_pred_col_names=pred_cn)

    performance_metrics['r2_score'] = r2_score(df=sf_df,y_true_col_name=true_cn, y_pred_col_name=pred_cn)

    performance_metrics['root_mean_square_error'] = math.sqrt(performance_metrics['r2_score'])

    return performance_metrics


def get_list_of_bins(total_rows):
    total_bins = 150
    bin_indexs = [] ; count = 0
    if total_rows > 150 :
        for i in range(0,total_rows,int(total_rows/total_bins)):
            bin_indexs.append(i)
            count += 1
            if count > 150 :
                break
    else :
        return [i for i in range(total_rows)]
    return bin_indexs

def get_binned_sf_dataframe(sf_df,plot_bins):
    from snowflake.snowpark.functions import row_number, lit, col
    from snowflake.snowpark.window import Window

    window_spec = Window.order_by(lit(1))
    df_with_row_numbers = sf_df.with_column("row_number",row_number().over(window_spec))
    temp_df = df_with_row_numbers.filter(col("row_number").isin(plot_bins)).drop("row_number")
    return temp_df

def get_prediction_vs_actual_data(sf_df,true_cn,pred_cn):
    regression_plot = {}
    regression_plot["x_axis"] = sf_df.select(true_cn).to_pandas().squeeze().tolist()
    regression_plot["y_axis"] = sf_df.select(pred_cn).to_pandas().squeeze().tolist()
    return regression_plot

def get_regression_plot_in_time(sf_df,true_cn,pred_cn,bins):
    regression_in_time_plot = {}
    target_plot = {} ; prediction_plot = {}
    target_plot['x_axis'] = bins[:-1]
    target_plot['y_axis'] = sf_df.select(true_cn).to_pandas().squeeze().tolist()
    prediction_plot['x_axis'] = bins[:-1]
    prediction_plot['y_axis'] = sf_df.select(pred_cn).to_pandas().squeeze().tolist()
    regression_in_time_plot[true_cn] = target_plot
    regression_in_time_plot[pred_cn] = prediction_plot
    return regression_in_time_plot

def get_errors_plot(sf_df,true_cn,pred_cn,bins):
    error_plot = {}
    error_plot['x_axis'] = bins[:-1]
    error_plot['y_axis'] = sf_df.with_column("difference",col(pred_cn)-col(true_cn)) \
                            .select("difference").to_pandas().squeeze().tolist()
    return error_plot

def get_error_normality_plot(sf_df,true_cn,pred_cn,bins):
    import numpy as np
    import scipy.stats as stats
    error_normality_plots = {}
    errors = sf_df.with_column("difference",col(pred_cn)-col(true_cn)) \
                            .select("difference").to_pandas().squeeze().tolist()
    sorted_errors = np.sort(np.array(errors))
    n = len(sorted_errors)

    theoretical_quantiles = stats.norm.ppf((np.arange(1,n+1) - 0.5)/n)
    error_normality_plots['theoretical_quantiles'] = theoretical_quantiles.tolist()
    error_normality_plots['prediction_errors'] = sorted_errors.tolist()
    return error_normality_plots


def execute_regression_drift(drift_configs,
                             sf_current,
                             sf_reference):
    
    ####################################Regression problem ########################################

    metrics = []
    target_column = drift_configs['target_column']
    prediction_column = drift_configs['prediction_column']

    # if not is_numeric_col(sf_current,drift_configs['target_column']):
    #     # print('Target col is non-numeric')
    #     mapped_target_col_name = drift_configs['target_column'] + '_NUMERIC'
    #     sf_current = map_to_numeric_col(sf_current,
    #                                     drift_configs['target_column'],
    #                                     drift_configs['predict_probability_columns'],
    #                                     mapped_target_col_name)
    #     sf_reference = map_to_numeric_col(sf_reference,
    #                                     drift_configs['target_column'],
    #                                     drift_configs['predict_probability_columns'],
    #                                     mapped_target_col_name)
    #     drift_configs['target_column'] = mapped_target_col_name
    #     target_column = mapped_target_col_name

    # if not is_numeric_col(sf_current,drift_configs['prediction_column']):
    #     # print('Prediction col is non-numeric')
    #     mapped_prediction_col_name = drift_configs['prediction_column'] + '_NUMERIC'
    #     sf_current = map_to_numeric_col(sf_current,
    #                                     drift_configs['prediction_column'],
    #                                     drift_configs['predict_probability_columns'],
    #                                     mapped_prediction_col_name)
    #     sf_reference = map_to_numeric_col(sf_reference,
    #                                     drift_configs['prediction_column'],
    #                                     drift_configs['predict_probability_columns'],
    #                                     mapped_prediction_col_name)
    #     drift_configs['prediction_column'] = mapped_prediction_col_name
    #     prediction_column = mapped_prediction_col_name

    ## bins
    plot_bins = get_list_of_bins(sf_current.count())

    # binned dataframes
    binn_sf_current = get_binned_sf_dataframe(sf_current,plot_bins)
    binn_sf_reference = get_binned_sf_dataframe(sf_current,plot_bins)

    # performance metrics
    regression_quality_metrics = {}
    regression_quality_metrics['current'] = get_regression_metrics(sf_current,target_column,prediction_column)
    regression_quality_metrics['reference'] = get_regression_metrics(sf_reference,target_column,prediction_column)
    metrics.append({
        "regression_quality_metrics" : regression_quality_metrics
    })
    # print(regression_quality_metrics)

    # Prediction vs Actual
    prediction_vs_actual = {}
    prediction_vs_actual['current'] = get_prediction_vs_actual_data(binn_sf_current,target_column,prediction_column)
    prediction_vs_actual['reference'] = get_prediction_vs_actual_data(binn_sf_reference,target_column,prediction_column)
    metrics.append({
        "prediction_vs_actual" : prediction_vs_actual
    })
    # print(prediction_vs_actual)

    # Prediction vs Actual in time
    prediction_vs_actual_in_time = {}
    prediction_vs_actual_in_time['current'] = get_regression_plot_in_time(binn_sf_current,target_column,prediction_column,plot_bins)
    prediction_vs_actual_in_time['reference'] = get_regression_plot_in_time(binn_sf_reference,target_column,prediction_column,plot_bins)
    metrics.append({
        "prediction_vs_actual_in_time" : prediction_vs_actual_in_time
    })
    # print(prediction_vs_actual_in_time)

    # Errors predicted vs Actual in time
    errors_plot = {}
    errors_plot['current'] = get_errors_plot(binn_sf_current,target_column,prediction_column,plot_bins)
    errors_plot['reference'] = get_errors_plot(binn_sf_reference,target_column,prediction_column,plot_bins)
    metrics.append({
        "errors_plot" : errors_plot
    })
    # print(errors_plot)

    ## Error normality
    errors_normality_plot = {}
    errors_normality_plot['current'] = get_error_normality_plot(binn_sf_current,target_column,prediction_column,plot_bins)
    errors_normality_plot['reference'] = get_error_normality_plot(binn_sf_reference,target_column,prediction_column,plot_bins)
    metrics.append({
        "errors_normality_plot" : errors_normality_plot
    })
    # print(errors_normality_plot)

    return {
        "metrics" : metrics
    }


