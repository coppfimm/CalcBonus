#Python 3.6.3
from Rule import *    
class CalcBonus:
    def __init__(self):
        self.rules = []
        
    def addRule(self,rule):
        self.rules.append(rule)
        
    def calcBonus(self,**kwargs):
        bonus = 0
        for rule in self.rules:
            if rule.condition(bonus=bonus,**kwargs):
                bonus = rule.action(bonus=bonus,**kwargs)
        return bonus
                
myBonus = CalcBonus()
#模拟条件的存取过程
myBonus.addRule(Qty_Rule())
#myBonus.addRule(Scaler_Rule())
#
print('My bonus is ',myBonus.calcBonus(qty=2000,price=200))