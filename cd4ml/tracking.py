import mlflow
import os

MLFLOW_TRACKING_URL = os.getenv('MLFLOW_TRACKING_URL')
TENANT = os.getenv('TENANT', 'local')
RUN_LABEL = os.getenv('BUILD_NUMBER', '0')
USE_MLFLOW = MLFLOW_TRACKING_URL is not None


class track:
    def __enter__(self):
        if USE_MLFLOW:
            mlflow.set_tracking_uri(uri=MLFLOW_TRACKING_URL)
            mlflow.set_experiment(TENANT)
            mlflow.start_run(run_name=RUN_LABEL)
        return self

    def __exit__(self, type, value, traceback):
        if USE_MLFLOW:
            mlflow.end_run()

    @staticmethod
    def log_param(key, val):
        if USE_MLFLOW:
            mlflow.log_param(key, val)

    def log_ml_params(self, ml_params):
        for key, val in ml_params.items():
            self.log_param(key, val)

    def log_pipeline_params(self, pipeline_params):
        excluded_keys = ['download_data_info']
        for key, val in pipeline_params.items():
            if key not in excluded_keys:
                self.log_param(key, val.__repr__())
