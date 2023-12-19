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

    def get_bmi_string_and_category(self,):
        bmi=self.calculate_bmi()
        bmi_string=f'{bmi} kg/m²'
        if bmi<18.5:
            category='Underweight'
        elif 18.5<=bmi<25:
            category='Normal'
        elif 25<=bmi<30:
            category='Overweight'
        else:
            category='Obesity'
        return bmi_string,category

    



