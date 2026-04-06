import os
import sys

from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import (DataTransformationArtifact,DataValidationArtifact, ModelTrainerArtifact)
from networksecurity.entity.config_entity import ModelTrainerConfig
import mlflow
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import evaluate_models, save_object,load_object,load_np_array
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score    
import dagshub


class ModelTrainer:
    def __init__(self,model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            dagshub.init(repo_owner='agbirhade1', repo_name='MLOps-NetworkSecurity', mlflow=True)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def track_mlflow(self, best_model, classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score
            mlflow.log_metric('f1_score', f1_score)
            mlflow.log_metric('precision_score', precision_score)
            mlflow.log_metric('recall_score', recall_score)
            mlflow.sklearn.log_model(best_model, 'model')

    '''
        Does hyperparameter tuning, trains the model, find the best model among several and saves the best one as well.
    
    '''
    def train_model(self,X_train,X_test,y_train,y_test):
            models = {
                    'Random Forest': RandomForestClassifier(verbose=1),
                      'Decision Tree': DecisionTreeClassifier(),
                      'Gradient Boosting': GradientBoostingClassifier(),
                      'Logistic Regression': LogisticRegression(),
                      'AdaBoost': AdaBoostClassifier()
                    }
            params = {
                'Decision Tree':{
                    'criterion':['gini','entropy','log_loss'],
                },
                'Random Forest': {
                    'n_estimators': [8,16,32,64,128,256]
                },
                'Gradient Boosting': {
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    'n_estimators': [8,16,32,64,128,256]
                },
                'Logistic Regression': {
                },
                'AdaBoost': {
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
            }
            model_report: dict = evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,params=params)
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]
            best_model_score = model_report[best_model_name]
            y_train_pred = best_model.predict(X_train)
            train_classification_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

            self.track_mlflow(best_model,train_classification_metric)

            y_test_pred = best_model.predict(X_test)
            test_classification_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path) #set the preprocessor
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True) #create dir to save the best model 
            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model) #save the best model for future predictions

            modelTrainerArtifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                        train_metric_artifact=train_classification_metric,
                                                        test_metric_artifact=test_classification_metric)
            logging.info(f'Model trainer artifact: {modelTrainerArtifact}')
            return modelTrainerArtifact

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #load train and test array
            train_arr = load_np_array(file_path=train_file_path)
            test_arr = load_np_array(file_path=test_file_path)

            X_train, y_train = train_arr[:,:-1], train_arr[:,-1]
            X_test, y_test = test_arr[:,:-1], test_arr[:,-1]
            return self.train_model(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
