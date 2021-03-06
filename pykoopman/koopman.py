from numpy import empty
from pydmd import DMD
from pydmd import DMDBase
from sklearn.pipeline import Pipeline
from sklearn.utils.validation import check_is_fitted

from pykoopman.differentiation import FiniteDifference
from pykoopman.observables import Identity
from pykoopman.regression import BaseRegressor
from pykoopman.regression import DMDRegressor


class Koopman:
    """Primary Koopman class."""

    def __init__(self, observables=None, differentiator=None, regressor=None):
        if observables is None:
            observables = Identity()
        if differentiator is None:
            differentiator = FiniteDifference()
        if regressor is None:
            regressor = DMD()

        self.observables = observables
        self.differentiator = differentiator
        self.regressor = regressor

    def fit(self, x, t=None):
        # TODO: validate data
        x_dot = self.differentiator(x, t)

        if isinstance(self.regressor, DMDBase):
            regressor = DMDRegressor(self.regressor)
        else:
            regressor = BaseRegressor(self.regressor)

        steps = [
            ("observables", self.observables),
            ("regressor", regressor),
        ]
        self.model = Pipeline(steps)

        # TODO: make this solve the correct problem
        self.model.fit(x, x_dot)

        self.n_input_features_ = self.model.steps[0][1].n_input_features_
        self.n_output_features_ = self.model.steps[0][1].n_output_features_

        return self

    def predict(self, x):
        check_is_fitted(self, "model")
        return self.observables.inverse(self._step(x))

    def simulate(self, x, n_steps=1):
        check_is_fitted(self, "model")
        # Could have an option to only return the end state and not all
        # intermediate states to save memory.
        output = empty((n_steps, self.n_input_features_))
        output[0] = self.predict(x)
        for k in range(n_steps - 1):
            output[k + 1] = self.predict(output[k])

        return output

    def _step(self, x):
        # TODO: rename this
        check_is_fitted(self, "model")
        return self.model.predict(x)

    @property
    def koopman_matrix(self):
        """
        Get the Koopman matrix K such that
        g(X') = g(X) * K
        """
        check_is_fitted(self, "model")
        return self.model.steps[-1][1].coef_
