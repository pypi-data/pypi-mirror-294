from __future__ import annotations

from abc import ABC
from enum import Enum

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, f1_score, accuracy_score, \
    adjusted_rand_score, adjusted_mutual_info_score, v_measure_score, fowlkes_mallows_score

from psyke.schema import DiscreteFeature
from psyke.utils import get_default_random_seed, Target, get_int_precision
from tuprolog.theory import Theory
from typing import Iterable
import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger('psyke')


class EvaluableModel(object):
    class Task(Enum):
        CLASSIFICATION = 1,
        REGRESSION = 2,
        CLUSTERING = 3

    class Score(Enum):
        pass

    class ClassificationScore(Score):
        ACCURACY = 1
        F1 = 2,
        INVERSE_ACCURACY = 3

    class RegressionScore(Score):
        MAE = 1
        MSE = 2
        R2 = 3

    class ClusteringScore(Score):
        ARI = 1,
        AMI = 2,
        V = 3,
        FMI = 4

    def __init__(self, discretization=None, normalization=None):
        self.discretization = [] if discretization is None else list(discretization)
        self.normalization = normalization

    def predict(self, dataframe: pd.DataFrame) -> Iterable:
        """
        Predicts the output values of every sample in dataset.

        :param dataframe: is the set of instances to predict.
        :return: a list of predictions.
        """
        return self.__convert(self._predict(dataframe))

    def _predict(self, dataframe: pd.DataFrame) -> Iterable:
        raise NotImplementedError('predict')

    def __convert(self, ys: Iterable) -> Iterable:
        if self.normalization is not None and not isinstance([p for p in ys if p is not None][0], str):
            m, s = self.normalization[list(self.normalization.keys())[-1]]
            ys = [prediction if prediction is None else prediction * s + m for prediction in ys]
        return ys

    def brute_predict(self, dataframe: pd.DataFrame, criterion: str = 'corner', n: int = 2) -> Iterable:
        return self.__convert(self._brute_predict(dataframe, criterion, n))

    def _brute_predict(self, dataframe: pd.DataFrame, criterion: str = 'corner', n: int = 2) -> Iterable:
        raise NotImplementedError('brute_predict')

    def unscale(self, values, name):
        if self.normalization is None or name not in self.normalization or isinstance(values, LinearRegression):
            return values
        if isinstance(values, Iterable):
            values = [None if value is None else
                      value * self.normalization[name][1] + self.normalization[name][0] for value in values]
        else:
            values = values * self.normalization[name][1] + self.normalization[name][0]
        return values

    def score(self, dataframe: pd.DataFrame, predictor=None, fidelity: bool = False, completeness: bool = True,
              brute: bool = False, criterion: str = 'corners', n: int = 2,
              task: EvaluableModel.Task = Task.CLASSIFICATION,
              scoring_function: Iterable[EvaluableModel.Score] = [ClassificationScore.ACCURACY]):
        extracted = np.array(
            self.predict(dataframe.iloc[:, :-1]) if not brute else
            self.brute_predict(dataframe.iloc[:, :-1], criterion, n)
        )
        idx = [prediction is not None for prediction in extracted]
        y_extracted = extracted[idx]
        true = [dataframe.iloc[idx, -1]]

        if fidelity:
            if predictor is None:
                raise ValueError("Predictor must be not None to measure fidelity")
            true.append(predictor.predict(dataframe.iloc[idx, :-1]).flatten())

        if task == EvaluableModel.Task.REGRESSION:
            y_extracted = self.unscale(y_extracted, dataframe.columns[-1])
            true = [self.unscale(t, dataframe.columns[-1]) for t in true]

        res = {
                  score: EvaluableModel.__evaluate(true, y_extracted, score) for score in scoring_function
              }, sum(idx) / len(idx)
        return res if completeness else res[0]

    @staticmethod
    def __evaluate(y, y_hat, scoring_function):
        if scoring_function == EvaluableModel.ClassificationScore.ACCURACY:
            f = accuracy_score
        elif scoring_function == EvaluableModel.ClassificationScore.F1:
            def f(true, pred):
                return f1_score(true, pred, average='weighted')
        elif scoring_function == EvaluableModel.ClassificationScore.INVERSE_ACCURACY:
            def f(true, pred):
                return 1 - accuracy_score(true, pred)
        elif scoring_function == EvaluableModel.RegressionScore.R2:
            f = r2_score
        elif scoring_function == EvaluableModel.RegressionScore.MAE:
            f = mean_absolute_error
        elif scoring_function == EvaluableModel.RegressionScore.MSE:
            f = mean_squared_error
        elif scoring_function == EvaluableModel.ClusteringScore.ARI:
            f = adjusted_rand_score
        elif scoring_function == EvaluableModel.ClusteringScore.AMI:
            f = adjusted_mutual_info_score
        elif scoring_function == EvaluableModel.ClusteringScore.V:
            f = v_measure_score
        elif scoring_function == EvaluableModel.ClusteringScore.FMI:
            f = fowlkes_mallows_score
        else:
            raise ValueError("Scoring function not supported")
        return [f(yy, y_hat) for yy in y]


class Extractor(EvaluableModel, ABC):
    """
    An explanator capable of extracting rules from trained black box.

    Parameters
    ----------
    predictor : the underling black box predictor.
    discretization : A collection of sets of discretised features.
    Each set corresponds to a set of features derived from a single non-discrete feature.
    """

    def __init__(self, predictor, discretization: Iterable[DiscreteFeature] = None, normalization=None):
        super().__init__(discretization, normalization)
        self.predictor = predictor

    def extract(self, dataframe: pd.DataFrame) -> Theory:
        """
        Extracts rules from the underlying predictor.

        :param dataframe: is the set of instances to be used for the extraction.
        :return: the theory created from the extracted rules.
        """
        raise NotImplementedError('extract')

    def predict_why(self, data: dict[str, float], verbose=True):
        """
        Provides a prediction and the corresponding explanation.
        :param data: is the instance to predict.
        :param verbose: if the explanation has to be printed.
        """
        raise NotImplementedError('predict_why')

    def predict_counter(self, data: dict[str, float], verbose=True, only_first=True):
        """
        Provides a prediction and counterfactual explanations.
        :param data: is the instance to predict.
        :param verbose: if the counterfactual explanation has to be printed.
        :param only_first: if only the closest counterfactual explanation is provided for each distinct class.
        """
        raise NotImplementedError('predict_counter')

    def mae(self, dataframe: pd.DataFrame, predictor=None, brute: bool = False, criterion: str = 'center',
            n: int = 3) -> float:
        """
        Calculates the predictions' MAE w.r.t. the instances given as input.

        :param dataframe: is the set of instances to be used to calculate the mean absolute error.
        :param predictor: if provided, its predictions on the dataframe are taken instead of the dataframe instances.
        :param brute: if True, a brute prediction is executed.
        :param criterion: creterion for brute prediction.
        :param n: number of points for brute prediction with 'perimeter' criterion.
        :return: the mean absolute error (MAE) of the predictions.
        """
        return self.score(dataframe, predictor, predictor is not None, False, brute, criterion, n,
                          Extractor.Task.REGRESSION, [Extractor.RegressionScore.MAE])[Extractor.RegressionScore.MAE][-1]

    def mse(self, dataframe: pd.DataFrame, predictor=None, brute: bool = False, criterion: str = 'center',
            n: int = 3) -> float:
        """
        Calculates the predictions' MSE w.r.t. the instances given as input.

        :param dataframe: is the set of instances to be used to calculate the mean squared error.
        :param predictor: if provided, its predictions on the dataframe are taken instead of the dataframe instances.
        :param brute: if True, a brute prediction is executed.
        :param criterion: creterion for brute prediction.
        :param n: number of points for brute prediction with 'perimeter' criterion.
        :return: the mean squared error (MSE) of the predictions.
        """
        return self.score(dataframe, predictor, predictor is not None, False, brute, criterion, n,
                          Extractor.Task.REGRESSION, [Extractor.RegressionScore.MSE])[Extractor.RegressionScore.MSE][-1]

    def r2(self, dataframe: pd.DataFrame, predictor=None, brute: bool = False, criterion: str = 'center',
            n: int = 3) -> float:
        """
        Calculates the predictions' R2 score w.r.t. the instances given as input.

        :param dataframe: is the set of instances to be used to calculate the R2 score.
        :param predictor: if provided, its predictions on the dataframe are taken instead of the dataframe instances.
        :param brute: if True, a brute prediction is executed.
        :param criterion: creterion for brute prediction.
        :param n: number of points for brute prediction with 'perimeter' criterion.
        :return: the R2 score of the predictions.
        """
        return self.score(dataframe, predictor, predictor is not None, False, brute, criterion, n,
                          Extractor.Task.REGRESSION, [Extractor.RegressionScore.R2])[Extractor.RegressionScore.R2][-1]

    def accuracy(self, dataframe: pd.DataFrame, predictor=None, brute: bool = False, criterion: str = 'center',
            n: int = 3) -> float:
        """
        Calculates the predictions' accuracy classification score w.r.t. the instances given as input.

        :param dataframe: is the set of instances to be used to calculate the accuracy classification score.
        :param predictor: if provided, its predictions on the dataframe are taken instead of the dataframe instances.
        :param brute: if True, a brute prediction is executed.
        :param criterion: creterion for brute prediction.
        :param n: number of points for brute prediction with 'perimeter' criterion.
        :return: the accuracy classification score of the predictions.
        """
        return self.score(dataframe, predictor, predictor is not None, False, brute, criterion, n,
                          Extractor.Task.CLASSIFICATION,
                          [Extractor.ClassificationScore.ACCURACY])[Extractor.ClassificationScore.ACCURACY][-1]

    def f1(self, dataframe: pd.DataFrame, predictor=None, brute: bool = False, criterion: str = 'center',
            n: int = 3) -> float:
        """
        Calculates the predictions' F1 score w.r.t. the instances given as input.

        :param dataframe: is the set of instances to be used to calculate the F1 score.
        :param predictor: if provided, its predictions on the dataframe are taken instead of the dataframe instances.
        :param brute: if True, a brute prediction is executed.
        :param criterion: creterion for brute prediction.
        :param n: number of points for brute prediction with 'perimeter' criterion.
        :return: the F1 score of the predictions.
        """
        return self.score(dataframe, predictor, predictor is not None, False, brute, criterion, n,
                          Extractor.Task.CLASSIFICATION,
                          [Extractor.ClassificationScore.F1])[Extractor.ClassificationScore.F1][-1]

    @staticmethod
    def cart(predictor, max_depth: int = 3, max_leaves: int = 3, max_features=None,
             discretization: Iterable[DiscreteFeature] = None, normalization=None, simplify: bool = True) -> Extractor:
        """
        Creates a new Cart extractor.
        """
        from psyke.extraction.cart import Cart
        return Cart(predictor, max_depth, max_leaves, max_features,
                    discretization=discretization, normalization=normalization, simplify=simplify)

    @staticmethod
    def divine(predictor, k: int = 5, patience: int = 15, close_to_center: bool = True,
               discretization: Iterable[DiscreteFeature] = None, normalization=None,
               seed: int = get_default_random_seed()) -> Extractor:
        """
        Creates a new DiViNE extractor.
        """
        from psyke.extraction.hypercubic.divine import DiViNE
        return DiViNE(predictor, k=k, patience=patience, close_to_center=close_to_center,
                      discretization=discretization, normalization=normalization, seed=seed)

    @staticmethod
    def cosmik(predictor, max_components: int = 4, k: int = 5, patience: int = 15, close_to_center: bool = True,
               output: Target = Target.CONSTANT, discretization: Iterable[DiscreteFeature] = None, normalization=None,
               seed: int = get_default_random_seed()) -> Extractor:
        """
        Creates a new COSMiK extractor.
        """
        from psyke.extraction.hypercubic.cosmik import COSMiK
        return COSMiK(predictor, max_components=max_components, k=k, patience=patience, close_to_center=close_to_center,
                      output=output, discretization=discretization, normalization=normalization, seed=seed)

    @staticmethod
    def iter(predictor, min_update: float = 0.1, n_points: int = 1, max_iterations: int = 600, min_examples: int = 250,
             threshold: float = 0.1, fill_gaps: bool = True, ignore_dimensions=None,
             normalization: dict[str, tuple[float, float]] = None, output=None,
             seed: int = get_default_random_seed()) -> Extractor:
        """
        Creates a new ITER extractor.
        """
        from psyke.extraction.hypercubic.iter import ITER
        return ITER(predictor, min_update, n_points, max_iterations, min_examples, threshold, fill_gaps,
                    ignore_dimensions, normalization, output, seed)

    @staticmethod
    def gridex(predictor, grid, min_examples: int = 250, threshold: float = 0.1, output: Target = Target.CONSTANT,
               discretization=None, normalization: dict[str, tuple[float, float]] = None,
               seed: int = get_default_random_seed()) -> Extractor:
        """
        Creates a new GridEx extractor.
        """
        from psyke.extraction.hypercubic.gridex import GridEx
        return GridEx(predictor, grid, min_examples, threshold, output, discretization, normalization, seed)

    @staticmethod
    def hex(predictor, grid, min_examples: int = 250, threshold: float = 0.1, output: Target = Target.CONSTANT,
            discretization=None, normalization: dict[str, tuple[float, float]] = None,
            seed: int = get_default_random_seed()) -> Extractor:
        """
        Creates a new HEx extractor.
        """
        from psyke.extraction.hypercubic.hex import HEx
        return HEx(predictor, grid, min_examples, threshold, output, discretization, normalization, seed)

    @staticmethod
    def gridrex(predictor, grid, min_examples: int = 250, threshold: float = 0.1,
                normalization: dict[str, tuple[float, float]] = None,
                seed: int = get_default_random_seed()) -> Extractor:
        """
        Creates a new GridREx extractor.
        """
        from psyke.extraction.hypercubic.gridrex import GridREx
        return GridREx(predictor, grid, min_examples, threshold, normalization, seed)

    @staticmethod
    def creepy(predictor, clustering, depth: int, error_threshold: float, output: Target = Target.CONSTANT,
               gauss_components: int = 2, ranks: [(str, float)] = [], ignore_threshold: float = 0.0,
               discretization=None, normalization: dict[str, tuple[float, float]] = None,
               seed: int = get_default_random_seed()) -> Extractor:
        """
        Creates a new CReEPy extractor.
        """
        from psyke.extraction.hypercubic.creepy import CReEPy
        return CReEPy(predictor, clustering, depth, error_threshold, output, gauss_components, ranks, ignore_threshold,
                      discretization, normalization, seed)

    @staticmethod
    def real(predictor, discretization=None) -> Extractor:
        """
        Creates a new REAL extractor.
        """
        from psyke.extraction.real import REAL
        return REAL(predictor, [] if discretization is None else discretization)

    @staticmethod
    def trepan(predictor, discretization=None, min_examples: int = 0, max_depth: int = 3,
               split_logic=None) -> Extractor:
        """
        Creates a new Trepan extractor.
        """
        from psyke.extraction.trepan import Trepan, SplitLogic
        if split_logic is None:
            split_logic = SplitLogic.DEFAULT
        return Trepan(predictor, [] if discretization is None else discretization, min_examples, max_depth, split_logic)


class Clustering(EvaluableModel, ABC):
    def __init__(self, discretization=None, normalization=None):
        super().__init__(discretization, normalization)

    def fit(self, dataframe: pd.DataFrame):
        raise NotImplementedError('fit')

    def explain(self):
        raise NotImplementedError('explain')

    @staticmethod
    def exact(depth: int = 2, error_threshold: float = 0.1, output: Target = Target.CONSTANT, gauss_components: int = 2,
              discretization=None, normalization=None, seed: int = get_default_random_seed()) -> Clustering:
        """
        Creates a new ExACT instance.
        """
        from psyke.clustering.exact import ExACT
        return ExACT(depth, error_threshold, output, gauss_components, discretization, normalization, seed)

    @staticmethod
    def cream(depth: int = 2, error_threshold: float = 0.1, output: Target = Target.CONSTANT, gauss_components: int = 2,
              discretization=None, normalization=None, seed: int = get_default_random_seed()) -> Clustering:
        """
        Creates a new CREAM instance.
        """
        from psyke.clustering.cream import CREAM
        return CREAM(depth, error_threshold, output, gauss_components, discretization, normalization, seed)
