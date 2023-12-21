class Person:
    def __init__(self, age, height, weight, gender, activity, meals_calories_perc, weight_loss_plan):
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
        self.activity = activity
        self.meals_calories_perc = meals_calories_perc
        self.weight_loss_plan = weight_loss_plan

    def calculate_bmi(self,):
        bmi = round(self.weight/((self.height/100)**2), 2)
        return bmi

    def get_bmi_string_and_category(self,):
        bmi = self.calculate_bmi()
        bmi_string = f'{bmi} kg/m²'
        if bmi < 18.5:
            category = 'Underweight'
        elif 18.5 <= bmi < 25:
            category = 'Normal'
        elif 25 <= bmi < 30:
            category = 'Overweight'
        else:
            category = 'Obesity'
        return bmi_string, category

    def calculate_bmr(self):
        bmr = 10*self.weight + 6.25*self.height - 5*self.age
        if self.gender == 'Male':
            bmr += 5
        else:
            bmr -= 161
        return bmr

    def calories_calculator(self):
        activites = ['Little/no exercise', 'Light exercise',
                     'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
        weights = [1.2, 1.375, 1.55, 1.725, 1.9]
        weight = weights[activites.index(self.activity)]
        maintain_calories = self.calculate_bmr()*weight
        return maintain_calories
