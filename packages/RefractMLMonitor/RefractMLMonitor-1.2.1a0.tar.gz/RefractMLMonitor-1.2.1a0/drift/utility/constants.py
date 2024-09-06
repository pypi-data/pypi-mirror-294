from email import parser
from typing import Final
import configparser

parser = configparser.ConfigParser()
parser.read('utility/properties.ini')

class DataType:
    TABULAR_DATA: Final = "Tabular"
    TEXT_DATA: Final = "Text"
    IMAGE_DATA: Final = "Image"
    VIDEO_DATA: Final = "Video"
    AUDIO_DATA: Final = "Audio"

class DriftType:
    FEATURE_DRIFT: Final = 'feature_drift'
    LABEL_DRIFT: Final = 'label_drift'
    MODEL_PERFORMANCE_DRIFT: Final = 'model_performance_drift'
    PREDICTION_DRIFT: Final = 'prediction_drift'

class ProblemType:
    CLASSIFICATION: Final = 'classification'
    REGRESSION: Final = 'regression'
    BINARY_CLASSIFICATION: Final = 'Binary Classification'
    MULTICLASS_CLASSIFICATION: Final = 'Multiclass Classification'
    MULTI_LABEL_CLASSIFICATION: Final = 'Multilabel Classification'

class DataConnector:
    SNOWFLAKE: Final = 'snowflake'

class AlertParams:
    DRIFT_SCORE: Final = 'drift_score'
    PERFORMANCE_DRIFT_SCORE: Final = 'performance_drift_score'

class SnowflakeTables:
    MODEL_MONITOR_TABLE: Final = 'MODEL_MONITOR'
    ALERT_TABLE: Final = 'ALERT'