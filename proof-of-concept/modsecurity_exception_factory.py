#!/usr/bin/env python2

import orange, orngAssoc


ruleSubsetList = []

data = orange.ExampleTable('sample')

for leftAttributeCount in range(len(data.domain),0,-1):
    support = 0
    if len(data) > 0:
        support = 27.0 / len(data)
    
    rules = orange.AssociationRulesInducer(data, support = support, classification_rules = True)
    rules = rules.filter(lambda rule: rule.n_left == leftAttributeCount)
    ruleSubsetList.append(rules)
    for rule in rules:
        attributeDict = {}
        for attribute in data.domain:
            attributeName = attribute.name
            attributeValue = rule.left[attribute].value
            if attributeValue != '~':
                attributeDict[attributeName] = attributeValue
        data = data.filter_ref(attributeDict, negate = True)

parameterList = ['n_left', 'support']
for ruleSubset in ruleSubsetList:
    orngAssoc.sort(ruleSubset, parameterList)
    orngAssoc.printRules(ruleSubset, parameterList)

