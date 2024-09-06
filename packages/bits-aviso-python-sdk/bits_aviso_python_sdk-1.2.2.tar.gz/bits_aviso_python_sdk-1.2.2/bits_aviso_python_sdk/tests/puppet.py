from bits_aviso_python_sdk.helpers import export_to_json, normalize_data_for_bigquery, initialize_logger, replace_invalid_keys
from bits_aviso_python_sdk.services.puppet import Puppet
from bits_aviso_python_sdk.services.google.storage import Storage


def authenticate_puppet():
    st = Storage()
    bucket_name = ''
    key_path = '/tmp/key.pem'
    cert_path = '/tmp/crt.pem'
    ca_path = '/tmp/ca.pem'
    # st.download_blob_to_file(bucket_name, '', key_path)
    # st.download_blob_to_file(bucket_name, '', cert_path)
    # st.download_blob_to_file(bucket_name, '', ca_path)
    p = Puppet(ssl_cert=cert_path, ssl_key=key_path, ssl_verify=ca_path)
    return p


def list_all_facts(p):
    """Lists all the facts."""
    facts = p.list_facts()
    export_to_json(facts, 'all_facts.json')


def list_facts_for_bigquery(p):
    """Lists the facts for BigQuery."""
    p = Puppet()
    facts = p.list_facts_for_bigquery()
    export_to_json(facts, 'bigquery_facts.json')


def list_hosts(p):
    """Lists all the hosts."""
    hosts = p.list_hosts()
    export_to_json(hosts, 'hosts.json')


def test():
    """Tests the Puppet class."""
    initialize_logger()
    p = authenticate_puppet()


if __name__ == '__main__':
    test()
