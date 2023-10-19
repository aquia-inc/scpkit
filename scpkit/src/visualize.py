from graphviz import Digraph
from .util import create_session, paginate


def add_child_nodes(ou_id, org_client, graph):
    """Adds child nodes to the graph.

    Args:
        ou_id (str): The ID of the organizational unit.
        org_client (boto3.client): The AWS Organizations client.
        graph (Digraph): The Graphviz Digraph object.

    """
    accounts = list_children(org_client, ou_id, 'ACCOUNT')
    ous = list_children(org_client, ou_id, 'ORGANIZATIONAL_UNIT')

    children = accounts + ous

    if children:
        for child in children:
            child_id = child['Id']
            child_type = child['Type']

            if child_type == 'ACCOUNT':
                account = org_client.describe_account(AccountId=child_id).get('Account')
                account_name = account.get('Name')
                account_id = account.get('Id')

                graph.node(child_id, label=account_name, shape='ellipse')
                graph.edge(ou_id, child_id)

                policies = get_policies_for_entity(account_id, org_client)

                add_policies_to_graph(graph, child_id, policies=policies)

            # Get the name of the child (OU or Account)
            if child_type == 'ORGANIZATIONAL_UNIT':
                current_ou = org_client.describe_organizational_unit(OrganizationalUnitId=child_id).get('OrganizationalUnit')
                ou_name = current_ou.get('Name')
                current_ou_id = current_ou.get('Id')

                graph.node(child_id, label=ou_name, shape='box')
                graph.edge(ou_id, child_id)

                policies = get_policies_for_entity(current_ou_id, org_client)
                add_policies_to_graph(graph, child_id, policies=policies)

                add_child_nodes(child_id, org_client, graph)


def list_children(org_client, parent_id, child_type):
    """Lists the children of a parent entity.

    Args:
        org_client (boto3.client): The AWS Organizations client.
        parent_id (str): The ID of the parent entity.
        child_type (str): The type of the child entities to list.

    Returns:
        list: A list of child entities.
    """
    all_children = paginate(org_client, 'list_children', ParentId=parent_id, ChildType=child_type)
    children = [ child for page in all_children for child in page.get('Children')]
    return children


def get_policies_for_entity(entity_id, org_client, filter='SERVICE_CONTROL_POLICY'):
    """Gets the policies associated with an entity.

    Args:
        entity_id (str): The ID of the entity.
        org_client (boto3.client): The AWS Organizations client.
        filter (str): The filter to apply when retrieving policies.

    Returns:
        list: A list of policies associated with the entity.
    """
    policies = org_client.list_policies_for_target(
        TargetId=entity_id,
        Filter=filter
    )
    return policies.get('Policies')


def add_policies_to_graph(graph, entity_id, policies=None):
    """Adds policies to the graph.

    Args:
        graph (Digraph): The Graphviz Digraph object.
        entity_id (str): The ID of the entity.
        policies (list): A list of policies to add to the graph.
    """
    if policies:
        for policy in policies:
            policy_name = policy.get('Name')
            graph.node(policy_name, label=policy_name, shape='trapezium')
            graph.edge(entity_id, policy_name)


def visualize_policies(profile, outdir):
    session = create_session(profile)
    org_client = session.client('organizations')

    # Initialize a Graphviz Digraph object
    graph = Digraph('AWS_Organizations', graph_attr={'rankdir':'LR'})

    # Get the root information
    root_id = org_client.list_roots()['Roots'][0]['Id']
    graph.node(root_id, label="Root", shape='box')
    get_policies_for_entity(root_id, org_client)
    add_policies_to_graph(graph, root_id)

    # Start building the tree
    add_child_nodes(root_id, org_client, graph)

    # Output the graphical tree hierarchy to a file
    graph.render(directory=outdir, filename='aws_org_tree', view=True)

