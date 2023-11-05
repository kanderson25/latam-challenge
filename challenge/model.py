import pandas as pd
import xgboost as xgb
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.utils import resample
from sklearn.model_selection import train_test_split

from typing import Tuple, Union, List

class DelayModel:

    def __init__(self):
        self._model = None  # El modelo se guardará en este atributo.

    def preprocess(self, data: pd.DataFrame, target_column: str = None) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or prediction.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        if target_column is not None:
            # Separar las características y el objetivo si se proporciona el nombre de la columna objetivo.
            features = data.drop(columns=[target_column])
            target = data[target_column]
            return features, target
        else:
            # Si no se proporciona una columna objetivo, devolver solo las características.
            return data

    def fit(self, features: pd.DataFrame, target: pd.DataFrame, scale: float) -> None:
        """
        Fit the model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
            scale (float): Valor para la variable `scale_pos_weight` para abordar el desequilibrio de clases.
        """
        # Aplicar balanceo de clases antes de ajustar el modelo.
        features_balanced, target_balanced = resample(features, target, random_state=1, stratify=target)
        
        xgb_model_2 = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight=scale)
        xgb_model_2.fit(features_balanced, target_balanced)

        # Guardar el modelo entrenado en el atributo _model.
        self._model = xgb_model_2

    def predict(self, features: pd.DataFrame) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        # Implementar la lógica para hacer predicciones con el modelo entrenado.
        if self._model is not None:
            return self._model.predict(features)
        else:
            raise ValueError("Model has not been trained. Please call the fit method first.")

