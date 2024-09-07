import base64
import logging
import requests


class Isilon:
    """Class to interact with the Isilon PowerScale API."""

    def __init__(self, username, password, clusters, platform_api_version='15'):
        """Initializes the Isilon class.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.
            clusters (dict): A dictionary containing the cluster name as key and IP as value.
            platform_api_version (str, optional): The version of the Isilon API to use. Defaults to '15'.
        """
        self.clusters = clusters
        self.headers = {'Authorization': f'Basic {self._encode_credentials(username, password)}'}
        self.platform_api_version = platform_api_version

    @staticmethod
    def _encode_credentials(username,  password):
        """Encodes the username and password for use in the API.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.

        Returns:
            str: The encoded credentials.
        """
        return base64.b64encode(f'{username}:{password}'.encode()).decode()

    def build_url(self, cluster, api_endpoint=None):
        """Builds the URL for the given Isilon cluster with no trailing slash. If an API endpoint is provided,
        it will be appended to the URL.

        Args:
            cluster (str, optional): The cluster ip or name.
            api_endpoint (str, optional): The path to the API endpoint. Defaults to None.

        Returns:
            str: The URL for the Isilon API.
        """
        if api_endpoint:  # check if an API endpoint is provided
            if api_endpoint.startswith('/'):  # check for a leading slash
                api_endpoint = api_endpoint[1:]  # remove the leading slash bc imma put it MYSELF
            # return the URL with the API endpoint
            return f'https://{cluster}:8080/platform/{self.platform_api_version}/{api_endpoint}'

        else:
            return f'https://{cluster}:8080/platform/{self.platform_api_version}'

    def get_all_quotas(self, clusters=None):
        """Gets the quotas for all clusters.

        Args:
            clusters (dict, optional): A dictionary containing the cluster name as key and IP as value.
                Defaults to None.

        Returns:
            list[dict], dict: The quotas for all clusters and error payload if any.
        """
        # if no clusters are provided, use the clusters from the class
        if not clusters:
            clusters = self.clusters

        all_quotas = []
        error_payload = {}
        for name, ip in clusters.items():  # get the name and ip of each cluster
            cluster_quota, error_payload = self.get_quotas_for_cluster(name, ip)
            if cluster_quota:
                all_quotas.extend(cluster_quota)

            elif error_payload:
                error_payload.update(cluster_quota)

            else:
                error_payload['Error'] = f'Failed to get quota data for the cluster {name} with the IP {ip}.'

        return all_quotas, error_payload

    def get_all_network_pools(self, clusters=None):
        """Gets the network pools for all clusters.

        Args:
            clusters (dict, optional): A dictionary containing the cluster name as key and IP as value.
                Defaults to None.

        Returns:
            list[dict], dict: The network pools for all clusters and error payload if any.
        """
        # if no clusters are provided, use the clusters from the class
        if not clusters:
            clusters = self.clusters

        all_network_pools = []
        error_payload = {}
        for name, ip in clusters.items():
            cluster_network_pools, error_payload = self.get_network_pools_for_cluster(name, ip)
            if cluster_network_pools:
                all_network_pools.extend(cluster_network_pools)

            elif error_payload:
                error_payload.update(cluster_network_pools)

            else:
                error_payload['Error'] = f'Failed to get network pool data for the cluster {name} with the IP {ip}.'

        return all_network_pools, error_payload

    def get_network_pools_for_cluster(self, cluster_name, cluster_ip=None):
        """Gets the network pools for the given cluster.

        Args:
            cluster_name (str): The cluster's name.
            cluster_ip (str, optional): The cluster's ip address.

        Returns:
            list[dict], dict: The network pool data for the cluster and error payload if any.
        """
        # build the url
        if cluster_ip:
            url = self.build_url(cluster_ip, api_endpoint='/network/pools')
        else:
            url = self.build_url(cluster_name, api_endpoint='/network/pools')

        # get the network pool data
        network_pools = []
        try:
            response = requests.get(url, headers=self.headers, verify=False)
            response.raise_for_status()
            network_pool_data = response.json().get('pools', {})
            if not network_pool_data:
                raise ValueError(f'No network pools found for {cluster_name}. IP: {cluster_ip}')

            # add the cluster name to the data
            for np in network_pool_data:
                np['cluster'] = cluster_name
                network_pools.append(np)

            # return the network pool data
            return network_pools, {}

        except (requests.exceptions.RequestException, ValueError) as e:
            err_msg = f'Failed to get network pools for {cluster_name}. IP: {cluster_ip}\nException Message: {e}'
            logging.error(err_msg)
            return [], {"Error": err_msg}

    def get_quota_data(self, cluster_name, path, cluster_ip=None, list_of_quotas=None):
        """Gets the quota data for the given path.
        If a list of quotas is provided, it will be used instead of fetching the quotas from the cluster.

        Args:
            cluster_name (str): The cluster's name.
            path (str): The path to get the quota data for.
            cluster_ip (str, optional): The cluster's ip address.
            list_of_quotas (list[dict], optional): The list of quotas to search through. Defaults to None.

        Returns:
            dict, dict: The quota data for the path and error payload if any.
        """
        if list_of_quotas:  # if a list of quotas is provided, use it
            quotas = list_of_quotas

        else:  # if not, get the quota data for the cluster
            if cluster_ip:
                quotas, error_payload = self.get_quotas_for_cluster(cluster_name, cluster_ip)
            else:
                quotas, error_payload = self.get_quotas_for_cluster(cluster_name)

            # check if there are any quotas
            if not quotas:
                return {}, error_payload

        # find the quota data for the path
        for quota in quotas:
            if quota.get('path') == path:
                return quota, {}

        return {}, {"Error": f'No quota data found for the path {path}'}

    def get_quota_id(self, cluster_name, path, cluster_ip=None, list_of_quotas=None):
        """Gets the quota id for the given path.
        If a list of quotas is provided, it will be used instead of fetching the quotas from the cluster.

        Args:
            cluster_name (str): The cluster's name.
            path (str): The path to get the quota id for.
            cluster_ip (str, optional): The cluster's ip address.
            list_of_quotas (list[dict], optional): The list of quotas to search through. Defaults to None.

        Returns:
            str, dict: The quota id for the path and error payload if any.
        """
        if list_of_quotas:  # if a list of quotas is provided, use it
            quotas = list_of_quotas

        else:  # if not, get the quota data for the cluster
            if cluster_ip:
                quotas, error_payload = self.get_quotas_for_cluster(cluster_name, cluster_ip)
            else:
                quotas, error_payload = self.get_quotas_for_cluster(cluster_name)

            # check if there are any quotas
            if not quotas:
                return '', error_payload

        # find the quota id for the path
        for quota in quotas:
            if quota.get('path') == path:
                return quota.get('id'), {}

        return '', {"Error": f'No quota id found for the path {path}'}

    def get_quotas_for_cluster(self, cluster_name, cluster_ip=None):
        """Gets the quotas for the given cluster.

        Args:
            cluster_name (str): The cluster's name.
            cluster_ip (str, optional): The cluster's ip address.

        Returns:
            list[dict], dict: The quota data for the cluster and error payload if any.
        """
        # build the url
        if cluster_ip:
            url = self.build_url(cluster_ip, api_endpoint='/quota/quotas')
        else:
            url = self.build_url(cluster_name, api_endpoint='/quota/quotas')

        # get the quota data
        quotas = []
        try:
            response = requests.get(url, headers=self.headers, verify=False)
            response.raise_for_status()
            quota_data = response.json().get('quotas', {})
            if not quota_data:
                raise ValueError(f'No quotas found for {cluster_name}. IP: {cluster_ip}')

            # add the cluster name to the data
            for quota in quota_data:
                quota['cluster'] = cluster_name
                quotas.append(quota)

            # return the quota data
            return quotas, {}

        except (requests.exceptions.RequestException, ValueError) as e:
            err_msg = f'Failed to get quota for {cluster_name}. IP: {cluster_ip}\nException Message: {e}'
            logging.error(err_msg)
            return [], {"Error": err_msg}

    def update_quota(self, cluster_name, quota_id, cluster_ip=None, **kwargs):
        """Updates the quota data for the given quota id.

        Args:
            cluster_name (str): The cluster's name.
            cluster_ip  (str): The cluster's ip address.
            quota_id (str): The id of the quota to update.
            **kwargs: The quota data to update. The key should be the field to update and the value should the value.

        Returns:
            bool, dict: True if the quota was updated successfully and error payload if any.
        """
        # build the url
        if cluster_ip:
            url = self.build_url(cluster_ip, '/quota/quotas') + f'/{quota_id}'
        else:
            url = self.build_url(cluster_name, '/quota/quotas') + f'/{quota_id}'

        # parse the kwargs into a payload
        payload = {}
        for key, value in kwargs.items():
            payload[key] = value
        print(payload)

        try:  # update the quota data
            response = requests.put(url, headers=self.headers, verify=False, json=payload)
            response.raise_for_status()
            return True, {}

        except requests.exceptions.RequestException as e:
            err_msg = (f'Failed to update quota for {quota_id}. Cluster: {cluster_name} | IP: {cluster_ip}\n'
                       f'Exception Message: {e}')
            logging.error(err_msg)
            return {}, {"Error": err_msg}
