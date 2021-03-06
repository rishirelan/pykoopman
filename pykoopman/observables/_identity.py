from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.utils.validation import check_is_fitted


class Identity(TransformerMixin, BaseEstimator):
    """
    A dummy observables class that simply returns its input.
    """

    def __init__(self):
        pass

    def fit(self, x, y=None):
        """
        Fit to measurement data.

        Parameters
        ----------
        x: array-like, shape (n_samples, n_input_features)
            Measurement data to be fit.

        y: None
            Dummy parameter retained for sklearn compatibility.

        Returns
        -------
        self
        """
        # TODO: validate input
        self.n_input_features_ = self.n_output_features_ = x.shape[1]

        return self

    def transform(self, x):
        """
        Apply Identity transformation to data.

        Parameters
        ----------
        x: array-like, shape (n_samples, n_input_features)
            Measurement data to be transformed.

        Returns
        -------
        y: array-like, shape (n_samples, n_input_features)
            Transformed data (same as x in this case).
        """
        # TODO validate input
        check_is_fitted(self, "n_input_features_")
        return x

    def inverse(self, y):
        """
        Compute inverse mapping satisfying
        :code:`self.inverse(self.transform(x)) == x`

        Parameters
        ----------
        y: array-like, shape (n_samples, n_output_features)
            Data to which to apply the inverse.
            Must have the same number of features as the transformed data
        """
        # TODO: validate input
        check_is_fitted(self, "n_input_features_")
        return y
