
import re

def get_cmc(mana_cost):

    mana_cost_pips = re.findall('{.+?}', mana_cost)
    
    cmc = 0
    for pip in mana_cost_pips:
        mana = pip.strip('{}').split('/')
        
        possible_costs = [eval_mana(symbol) for symbol in mana]
        cmc += max(possible_costs)
            
        
    return cmc

def eval_mana(symbol):
    if re.match('[0-9]+', symbol):
        return int(symbol)
    
    if re.match('[Xx]', symbol):
        return 0
    
    if re.match('[WUBRGPCSwubrgpcs]', symbol):
        return 1
    
    raise Exception
