from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score


def get_classification_score(y_true, y_pred)->ClassificationMetricArtifact:
    try:
        f1 = f1_score(y_true,y_pred)
        model_recall_score = recall_score(y_true,y_pred)
        model_precision_score = precision_score(y_true,y_pred)
        classification_metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision_score=model_precision_score, recall_score=model_recall_score)
        return classification_metric_artifact
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
