'''
    Helper function that merges raw lists of grant information into a list
    of tuples.

    Args:
        [recipients] (int)
        [funders] (int)
        [contributions] (float)

    Returns:
        [ ( recipient (int), funder (int), contribution (float) ) ]
'''
def join_raw_data(recipients, funders, contributions):
    return list(zip(recipients, funders, contributions))

'''
    Helper function that aggregates contributions from the same funder
    to a given recipient.

    Args:
        grants: [ ( recipient (int), funder (int), contribution (float) ) ]

    Returns:
        { 'recipient' (int): { 'funder' (int): agg_contribution (float) } }
'''
def aggregate(grants):
    aggregated = {}
    for recipient, funder, contribution in grants:
        if recipient not in aggregated:
            aggregated[recipient] = {}
        aggregated[recipient][funder] = aggregated[recipient].get(funder, 0) + contribution
    return aggregated

'''
    Helper function that sums individual contributions to each recipient.

    Args:
        grants: { 'recipient' (int): { 'funder' (int): contribution (float) } }

    Returns:
        { 'recipient' (int): sum_contribution (float) }

'''
def recipient_grant_sum(grants):
    return {key:sum(value.values()) for key, value in grants.items()}

'''
    Helper function that calculates the unconstrained liberal radical match
    for each recipient.

    Args:
        grants: { 'recipient' (int): { 'funder' (int): contribution (float) } }

    Returns:
        { 'recipient' (int): lr_grant (float) }

'''
def calc_lr_matches(grants):
    matches = {}
    for recipient in grants:
        sum_sqrts = sum([i**(1/2) for i in grants[recipient].values()])
        squared = sum_sqrts**2
        matches[recipient] = squared
    return matches

'''
    Helper function that normalizes the liberal radical grants to the
    total matching budget.

    Args:
        { 'recipient' (int): lr_grant (float) }
        budget (float)

    Returns:
        { 'recipient' (int): lr_grant (float) }
'''
def constrain_by_budget(matches, budget):
    raw_total = sum(matches.values())
    constrained = {key:value/raw_total * budget for key, value in matches.items()}
    return constrained

'''
    Helper function that calculates constrained liberal radical matches and
    helpful info.

    Args:
        [recipients] (ints)
        [funders] (ints)
        [contributions] (floats)
        budget: (float)

    Returns:
        grants: { 'recipient' (int): { 'funder' (int): agg_contribution (float) } }
        recipient_grant_sums:  { 'recipient' (int): sum_contribution (float) }
        clr: { 'recipient' (int): lr_grant (float) }
'''
def clr(recipients, funders, contribution_amounts, budget):
    raw_grants = join_raw_data(recipients, funders, contribution_amounts)
    grants = aggregate(raw_grants)
    recipient_grant_sums = recipient_grant_sum(grants)
    lr_matches = calc_lr_matches(grants)
    clr = constrain_by_budget(lr_matches, budget)

    return grants, recipient_grant_sums, clr
