# -*- coding: utf-8 -*-
"""The module :mod:`py_fatigue.damage.crack_growth` contains all the
damage models related to the crack growth approach.
"""
import datetime
import logging
from typing import Dict, List, Optional, Union

import pandas as pd
import requests as req
from pydantic import validate_call

# Local imports
from .. import utils as U
from . import schemas as S

try:
    # delete the accessor to avoid warning
    del pd.DataFrame.datasignals
except AttributeError:
    pass

BASE_URL = "https://api.24sea.eu/routes/v1/"


logging.basicConfig(format="%(message)s", level=logging.INFO)


def check_authentication(func):
    """Check authentication before making the request to the 24SEA API."""

    def wrapper(self, *args, **kwargs):
        """Wrapper function to check authentication."""
        # fmt: off
        if not isinstance(self.auth, req.auth.HTTPBasicAuth) or not self.authenticated:
            raise U.AuthenticationError(
                "\033[31;1mAuthentication needed before querying the metrics.\n"
                "\033[0mUse the \033[34;1mdatasignals.\033[0mauthenticate("
                "\033[32;1m<username>\033[0m, \033[32;1m<password>\033[0m) "
                "method."
            )
        return func(self, *args, **kwargs)
        # fmt: on

    return wrapper


@pd.api.extensions.register_dataframe_accessor("datasignals")
class DataSignals:
    """Accessor for working with data signals coming from the 24SEA API."""

    def __init__(self, pandasdata: pd.DataFrame):
        self._obj = pandasdata
        self.base_url: str = f"{BASE_URL}datasignals/"
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.auth: Optional[req.auth.HTTPBasicAuth] = None
        self.authenticated: bool = False
        self.metrics_overview: Optional[pd.DataFrame] = None
        self.selected_metrics: Optional[pd.DataFrame] = None

    @validate_call
    def authenticate(self, username: str, password: str) -> None:
        """Authenticate the user with the 24SEA API. Additionally, define
        the ``metrics_overview`` dataframe.

        Parameters
        ----------
        username : str
            The username to authenticate.
        password : str
            The password to authenticate.
        """
        # -- Step 1: Authenticate and check the credentials
        self.username = username
        self.password = password
        self.auth = req.auth.HTTPBasicAuth(self.username, self.password)
        # fmt: off
        try:
            r_profile = U.handle_request(
                f"{self.base_url}profile",
                {"username": self.username},
                self.auth,
                {"accept": "application/json"},
            )
            self.authenticated = True
            logging.info("\033[32;1mThis dataframe has now access to https://api.24sea.eu/.\033[0m")  # noqa: E501  # pylint: disable=C0301
        except req.exceptions.HTTPError:
            raise U.AuthenticationError("\033[31;1mThe username and/or password are incorrect.\033[0m")  # noqa: E501  # pylint: disable=C0301
        # fmt: on
        # -- Step 2: Define the metrics_overview dataframe
        if self.metrics_overview is not None:
            return None
        logging.info("Now getting your metrics_overview table...")
        r_metrics = U.handle_request(
            f"{self.base_url}metrics",
            {"project": None, "locations": None, "metrics": None},
            self.auth,
            {"accept": "application/json"},
        )
        # fmt: off
        if not isinstance(r_metrics, type(None)):
            try:
                m_ = pd.DataFrame(r_metrics.json())
            except Exception:
                raise U.ProfileError(f"\033[31;1mThe metrics overview is empty. This is your profile information:"  # noqa: E501  # pylint: disable=C0301
                                     f"\n {r_profile.json()}")
        if m_.empty:
            raise U.ProfileError(f"\033[31;1mThe metrics overview is empty. This is your profile information:"  # noqa: E501  # pylint: disable=C0301
                                 f"\n {r_profile.json()}")
        try:
            s_ = m_.apply(lambda x: x["metric"]
                        .replace(x["statistic"], "")
                        .replace(x["short_hand"], "")
                        .strip(), axis=1).str.strip("_").str.split("_", expand=True)   # noqa: E501  # pylint: disable=C0301
            s_.columns = ["site_id", "location_id"]
        # fmt: on
        except Exception:
            self.metrics_overview = m_
        self.metrics_overview = pd.concat([m_, s_], axis=1)
        return

    @check_authentication
    @validate_call
    def get_metrics(
        self,
        site: Optional[str] = None,
        locations: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Optional[List[Dict[str, Optional[str]]]]:
        """
        Get the metrics names for a site, provided the following parameters.

        Parameters
        ----------
        site : Optional[str]
            The site name. If None, the queryable metrics for all sites
            will be returned, and the locations and metrics parameters will be
            ignored.
        locations : Optional[Union[str, List[str]]]
            The locations for which to get the metrics. If None, all locations
            will be considered.
        metrics : Optional[Union[str, List[str]]]
            The metrics to get. They can be specified as regular expressions.
            If None, all metrics will be considered.

            For example:

            * | ``metrics=["^ACC", "^DEM"]`` will return all the metrics that
              | start with ACC or DEM,
            * Similarly, ``metrics=["windspeed$", "winddirection$"]`` will
              | return all the metrics that end with windspeed and
              | winddirection,
            * and ``metrics=[".*WF_A01.*",".*WF_A02.*"]`` will return all
              | metrics that contain WF_A01 or WF_A02.

        Returns
        -------
        Optional[List[Dict[str, Optional[str]]]]
            The metrics names for the given site, locations and metrics.

        .. note::
            This class method is legacy because it does not add functionality to
            the DataSignals pandas accessor.

        """
        url = f"{self.base_url}metrics"
        # fmt: on
        if headers is None:
            headers = {"accept": "application/json"}
        if site is None:
            params = {}
        if isinstance(locations, List):
            locations = ",".join(locations)
        if isinstance(metrics, List):
            metrics = ",".join(metrics)
        params = {
            "project": site,
            "locations": locations,
            "metrics": metrics,
        }

        r_ = U.handle_request(url, params, self.auth, headers)

        # Set the return type of the get_metrics method to the Metrics schema
        return r_.json()  # type: ignore

    @check_authentication
    @validate_call
    def get_data(
        self,
        sites: Optional[Union[List, str]],
        locations: Optional[Union[List, str]],
        metrics: Union[List, str],
        start_timestamp: Union[str, datetime.datetime],
        end_timestamp: Union[str, datetime.datetime],
        outer_join_on_timestamp: bool = False,
        headers: Optional[Union[Dict[str, str]]] = None,
    ):
        """Get the data signals from the 24SEA API.

        Parameters
        ----------
        sites : Optional[Union[List, str]]
            The site name or List of site names. If None, the site will be
            inferred from the metrics.
        locations : Optional[Union[List, str]]
            The location name or List of location names. If None, the location
            will be inferred from the metrics.
        metrics : Union[List, str]
            The metric name or List of metric names. It must be provided.
            They do not have to be the entire metric name, but can be a part
            of it. For example, if the metric name is
            ``"mean_WF_A01_windspeed"``, the user can equivalently provide
            ``sites="wf"``, ``locations="a01"``, ``metric="mean windspeed"``.
        start_timestamp : Union[str, datetime.datetime]
            The start timestamp for the query. It must be in ISO 8601 format,
            e.g., ``"2021-01-01T00:00:00Z"`` or a datetime object.
        end_timestamp : Union[str, datetime.datetime]
            The end timestamp for the query. It must be in ISO 8601 format,
            e.g., ``"2021-01-01T00:00:00Z"`` or a datetime object.
        outer_join_on_timestamp : bool, optional
            If True, the data will be joined on the timestamp which will be the
            index of the DataFrame. If False, the data will be concatenated
            without any join. Default is False.
        headers : Optional[Union[Dict[str, str]]], optional
            The headers to pass to the request. If None, the default headers
            will be used as ``{"accept": "application/json"}``. Default is None.

        Returns
        -------
        pd.DataFrame
            The DataFrame containing the data signals.
        """
        # Clean the DataFrame
        data_ = pd.DataFrame()
        # -- Step 1: Build the query object from GetData
        query = S.GetData(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            sites=sites,
            locations=locations,
            metrics=metrics,
            headers=headers,
            outer_join_on_timestamp=outer_join_on_timestamp,
        )

        if query.sites is None and query.locations is None:
            query_str = (
                "metric.str.contains(@query.metrics, case=False, regex=True)"
            )
        elif query.sites is None and query.locations is not None:
            query_str = (
                "(location.str.lower() == @query.locations or location_id.str.lower() == @query.locations) "
                "and metric.str.contains(@query.metrics, case=False, regex=True)"
            )
        elif query.locations is None and query.sites is not None:
            query_str = (
                "(site.str.lower() == @query.sites or site_id.str.lower() == @query.sites) "
                "and metric.str.contains(@query.metrics, case=False, regex=True)"
            )
        else:
            query_str = (
                "(site_id.str.lower() == @query.sites or site.str.lower() == @query.sites) "
                "and (location.str.lower() == @query.locations or location_id.str.lower() == @query.locations) "
                "and metric.str.contains(@query.metrics, case=False, regex=True)"
            )
        # match query.sites, query.locations:
        #     case None, None:
        #         query_str = "metric.str.contains(@query.metrics, case=False, regex=True)"
        #     case None, _:
        #         query_str = (
        #             "(location.str.lower() == @query.locations or location_id.str.lower() == @query.locations) "
        #             "and metric.str.contains(@query.metrics, case=False, regex=True)"
        #         )
        #     case _, None:
        #         query_str = (
        #             "(site.str.lower() == @query.sites or site_id.str.lower() == @query.sites) "
        #             "and metric.str.contains(@query.metrics, case=False, regex=True)"
        #         )
        #     case _, _:
        #         query_str = (
        #             "(site_id.str.lower() == @query.sites or site.str.lower() == @query.sites) "
        #             "and (location.str.lower() == @query.locations or location_id.str.lower() == @query.locations) "
        #             "and metric.str.contains(@query.metrics, case=False, regex=True)"
        #         )

        nl = "\n"
        l_ = f"\033[30;1mQuery:\033[0;34m {query_str.replace(' and ', f'{nl}       and ')}\n"
        logging.info(l_)

        self.selected_metrics = self.metrics_overview.query(query_str).pipe(  # type: ignore  # noqa: E501  # pylint: disable=E501
            lambda df: df.sort_values(
                ["site", "location", "data_group", "short_hand", "statistic"],
                ascending=[True, True, False, True, True],
            )
        )
        logging.info("\033[32;1mMetrics selected for the query:\033[0m\n")
        # fmt: off
        logging.info(self.selected_metrics[["metric", "unit_str", "data_group",
                                            "location", "site"]]
                                          .reset_index(drop=True))
        # fmt: on
        data_frames = []
        grouped_metrics = self.selected_metrics.groupby(["site", "location"])

        # return grouped_metrics
        logging.info(
            f"\n\033[32;1mRequested time range:\033[0;34m "
            f"From {str(query.start_timestamp)[:-4].replace('T', ' ')} "
            f"To {str(query.end_timestamp)[:-4].replace('T', ' ')}\n\033[0m"
        )
        import concurrent.futures

        def fetch_data(site, location, group):
            # fmt: off
            s_ = "• " + ",".join(group["metric"].tolist()).replace(",", "\n           • ")  # noqa: E501  # pylint: disable=C0301
            logging.info(f"\033[32;1m\033[32;1m⏳ Getting data for {site} - "
                         f"{location}...\n  Metrics: \033[0;34m{s_}\n\033[0m")
            # fmt: on
            r_ = U.handle_request(
                f"{self.base_url}data",
                {
                    "start_timestamp": query.start_timestamp,
                    "end_timestamp": query.end_timestamp,
                    "project": [site],
                    "location": [location],
                    "metrics": ",".join(group["metric"].tolist()),
                },
                self.auth,
                query.headers,
            )
            # Warn if empty
            if r_.json() == []:
                logging.warning(
                    f"\033[33;1mNo data found for {site} - {location}.\033[0m"
                )
            return pd.DataFrame(r_.json())

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # fmt: off
            future_to_data = {
                executor.submit(fetch_data,
                                site,
                                location,
                                group): (site, location)
                for (site, location), group in grouped_metrics
            }
            # fmt: on
            for future in concurrent.futures.as_completed(future_to_data):
                data_frames.append(future.result())
            # data_frames.append(pd.DataFrame(r_.json()))

        # if left_join_on_timestamp is True, lose the location and site columns
        # and join on timestamp
        if outer_join_on_timestamp:
            for i, df in enumerate(data_frames):
                if df.empty:
                    continue
                data_frames[i] = df.set_index("timestamp")
                # drop site and location
                data_frames[i].drop(["site", "location"], axis=1, inplace=True)
            data_ = pd.concat([data_] + data_frames, axis=1, join="outer")
        else:
            data_ = pd.concat([data_] + data_frames, ignore_index=True)
        # To access the data, use the .data attribute of the datasignals accessor
        logging.info("\033[32;1m✔️ Data successfully retrieved.\033[0m")
        print(
            "Your \033[30;1mpandas DataFrame\033[0m has been updated with the "
            "queried data."
        )
        self._obj.drop(self._obj.index, inplace=True)
        for col in data_.columns:
            if col in self._obj.columns:
                del self._obj[col]
            self._obj[col] = data_[col]
        return data_
