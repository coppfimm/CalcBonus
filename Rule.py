#Python 3.6.3
class Rule:
    '''
    所有规则的基类
    '''
    ##模拟条件表 需要优化，现在的处理不够灵活
    ## Qty： 如果数量大于1600罐，启用条件，如果单价大于等于100，每罐奖励5元，单价小于100，每罐奖励3元
    ## Scaler: 按销售金额计算：
    ##低于或等于10万元时，奖金可提10%；
    ##利润高于10万元，低于20万元时，低于10万元的部分按10%提成，高于10万元的部分，可提成7.5%；
    ##20万到40万之间时，高于20万元的部分，可提成5%；
    ##40万到60万之间时高于40万元的部分，可提成3%；
    ##60万到100万之间时，高于60万元的部分，可提成1.5%，
    ##高于100万元时，超过100万元的部分按1%提成
    
    ##cases:
        ##套餐甲，3个A，2个B，1个C，奖励物
        ##套餐乙，3个A，4个D，1个E，奖励钱
        
    cfg = {'Qty':{'condition':['qty>1600'],'action':[{'match':'price>=100','do':'qty * 5'},{'match':'price<100','do':'qty * 3'}]},
           'Scaler':{'amount':[1000000,600000,400000,200000,100000,0],'rat':[0.01,0.015,0.03,0.05,0.075,0.1]}
          }
    def getConfig(self):
        '''
        模拟条件表
        取所有规则的配置表
        '''
        pass
    
    def condition(self,**kwargs):
        '''
        规则生效条件
        '''
        return False
    def action(self,**kwargs):
        '''
        规则生效后执行的动作
        '''
        return True
class Qty_Rule(Rule):
    name = 'Qty' #规则名称 跟配置表匹配
    def condition(self,**kwargs):
        '''
        规则生效条件 数量大于1600
        '''
        
        #qty = kwargs.get('qty',0)
        createVar = locals()
        for k,v in kwargs.items():
            createVar[k] = v

        #if qty > 1600:
        #    return True
        #else:
        #    return False
        conditions = self.cfg.get(Qty_Rule.name,None).get('condition',None)
        for condition in conditions:
            if not eval(condition): return False
        else:
            return True
        
    def action(self,**kwargs):
        '''
        计算方案
        单价小于100每罐3元
        单价大于100每罐5元
        '''
        price = 0 #价格
        qty = 0 #数量
        
        bonus  = kwargs.get('bonus',0) #奖金
        price = kwargs.get('price',0)
        qty = kwargs.get('qty',0)

        #if price >= 100:
        #    bonus += qty * 5
        #else:
        #    bonus += qty * 3
        actions = self.cfg.get(Qty_Rule.name,None).get('action',None)
        for action in actions:
            if eval(action.get('match',False)):
                bonus += eval(action.get('do',0))
        return bonus
    
class Scaler_Rule(Rule):
    name = 'Scaler'
    def condition(self,**kwargs):
        return True
    def action(self,**kwargs):
           
        bonus  = kwargs.get('bonus',0) #奖金
        price = kwargs.get('price',0)
        qty = kwargs.get('qty',0)
        
        amount = qty * price
        
        scaler = self.cfg.get(Scaler_Rule.name,None).get('amount',None)
        rat = self.cfg.get(Scaler_Rule.name,None).get('rat',None)
        
        for i in range(0,6):
            if amount>scaler[i]:
                bonus+=(amount-scaler[i])*rat[i]
                amount=scaler[i]
        return bonus