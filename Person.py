class Person:
    def __init__(self,age,height,weight,gender,activity,meals_calories_perc,weight_loss_plan):
        self.age=age
        self.height=height
        self.weight=weight
        self.gender=gender
        self.activity=activity
        self.meals_calories_perc=meals_calories_perc
        self.weight_loss_plan=weight_loss_plan

    def calculate_bmi(self,):
        bmi=round(self.weight/((self.height/100)**2),2)
        return bmi



