import flet as ft

'''
Health Calculators
omnicalculator.com/health#s-110
'''

class Input(ft.Container):
    def __init__(self, label, suffix_text=None, on_blur=None, width=100):
        super().__init__(
            width = width
        )
        
        self.content=ft.TextField(
            dense=True,
            content_padding=8,
            label=label,
            label_style=ft.TextStyle(size=15),
            suffix_text=suffix_text,
            on_blur=on_blur,
        )
        
class Result(ft.Column):
    def __init__(self, text, suffix_text, description=None, hint=None, info=None):
        super().__init__()
        
        self.name = ft.Container(
            width=100,
            padding=0,
            
            content=ft.Row(
                spacing=1,
                controls=[
                    ft.Container(
                        padding=ft.padding.only(right=5)),
                    ft.Text(
                        value=text,
                        weight=ft.FontWeight.BOLD,
                        size=12,
                        overflow=ft.TextOverflow.FADE
                    ),
                    # self.info_icon,
                ]
            )
        )
                
        if info:
            self.descriptionDialog = DetailsAlertDialog(info)
    
        if hint or info:
            self.info_icon = ft.IconButton(
                expand=True,
                icon=ft.Icons.INFO_OUTLINED, 
                icon_size=13,
                icon_color=ft.Colors.GREY,
                style=ft.ButtonStyle(padding=0),
                alignment=ft.Alignment(-1.0, -0.5),
            )
            if hint:
                self.info_icon.tooltip=hint
            if info:
                self.info_icon.selected_icon_color="black"
                self.info_icon.on_click=lambda _: self.page.open(DetailsAlertDialog(info))
                # self.info_icon.on_click=lambda _: self.page.open(self.descriptionDialog)
            self.name.content.controls.append(self.info_icon)
                
        self.result = ft.TextField(
            dense=True,
            text_size=14,
            content_padding=8,
            # suffix_text=suffix_text,
            # suffix_style=ft.TextStyle(size=13),
            read_only=True,
            border=ft.InputBorder.OUTLINE,
            border_width=1,
            text_align=ft.TextAlign.END,
            # helper_text=hint,
            # helper_style=ft.TextStyle(
            #     size=11, height=.5
            # ),
        )
        
        self.description = ft.Container(
            padding=ft.padding.only(left=10),
            content=ft.Text(
                description,
                size=10,
                color="#555555")
        )
                
        self.controls = [
            ft.Column(
                spacing=0,
                controls=[
                    ft.Row(
                        spacing=5,
                        controls=[
                            self.name,
                            ft.Container(
                                width=120, 
                                content=self.result
                            ),
                            ft.Text(
                                size=12,
                                value=suffix_text
                                ),                                          
                        ]
                    ),
                    ft.Container(
                        padding=ft.padding.only(left=110),
                        content=self.description
                    )
                ]
            )
        ]
        

class ResultUpper(Result):
    def __init__(self, text, suffix_text, icon=None, description=None, hint=None, info=None):
        super().__init__(text, suffix_text, description, hint, info)
                
        # self.name.width=100
        self.name.content.controls[0].content=ft.Icon(name=icon, color=ft.Colors.LIME, size=20)
                
        self.result.border_width=2

        self.controls[0].controls[0].controls[0] = self.name
        
         
class ResultLower(Result):
    def __init__(self, text, suffix_text, description=None, hint=None, info=None):
        super().__init__(text, suffix_text, description, hint, info)

class ResultLowerValueSet(Result):
    def __init__(self, text, suffix_text, value, description=None, hint=None, info=None):
        super().__init__(text, suffix_text, description, hint, info)
        
        self.result.value=value   
        
class ResultLowerNotAvailable(Result):
    def __init__(self, text, suffix_text, description=None, hint=None, info=None):
        super().__init__(text, suffix_text, description, hint, info)
        
        self.result.bgcolor="grey"   

class DetailsAlertDialog(ft.AlertDialog):
    def __init__(self, explanation):
        super().__init__(
            # open=True
        )
        # print(f"alert dialog clicked. explanation: {explanation}")
        
        self.content=ft.Text(
            value=explanation,
        )

        self.actions=[
            ft.TextButton("Close", on_click=self.handle_close),
        ]
        
    def handle_close(self, e):
        self.page.close(self)        
        
class Landing(ft.Container):
    def __init__(self):
        super().__init__(
            margin=ft.margin.symmetric(vertical=5)
        )

        self.title = ft.Text(
            value="Dietary Calculator",
            size=20
        )

        self.subtitle = ft.Text(
            value="(Mifflin-St Jeor equation)",
            size=15
        )

        self.content = ft.Row(
            vertical_alignment = ft.CrossAxisAlignment.END,
            controls=[
                self.title, 
                # self.subtitle
            ],
        )


### APP CLASS ###
class DietaryCalculator(ft.Column):
    def __init__(self, window_size):
        super().__init__(
            expand=True,
            opacity=0.8,
        )

        self.hasValue = {"height": False, "weight": False, "age": False, "sex": False}

        self.height = Input("Height", "cm", self.height_entered)
        self.weight = Input("Weight", "kg", self.weight_entered)
        self.age = Input("Age", "", self.age_entered)
        self.height = Input("Height", "cm", self.height_entered)

        self.sex = ft.Dropdown(
            content_padding=8,
            label="Sex",
            width=100,
            dense=True,
            options=[
                ft.dropdown.Option("Female"),
                ft.dropdown.Option("Male"),
            ],
            on_change=self.sex_selected,
        )
        
        self.pal = ft.Container(
            width=260,
            content=ft.Dropdown(
                content_padding=8,
                label="PAL (Physical Activity Level)",
                label_style=ft.TextStyle(size=15),
                dense=True,
                options=[
                    ft.dropdown.Option("Little/no exercise"),
                    ft.dropdown.Option("Exercise 1-2 times/week"),
                    ft.dropdown.Option("Exercise 2-3 times/week"),
                    ft.dropdown.Option("Exercise 3-5 times/week"),
                    ft.dropdown.Option("Exercise 6-7 times/week"),
                ],
                on_change=self.pal_selected,
            )
        )   
        
        self.bmr = ResultUpper("BMR", "kcal/day", ft.Icons.ENERGY_SAVINGS_LEAF_OUTLINED, "Calories used when body is completely at rest", "Basal metabolic rate\n by Mifflin-St Jeor equation", "Info for BMR")
        self.tdee = ResultUpper("TDEE", "kcal/day", ft.Icons.ENERGY_SAVINGS_LEAF, "Calories needed to maintain the current weight", "Total daily energy expenditure")


        # ResultLower - DRI: Dietary reference intake
        self.protein = ResultLower("Protein", " g/day", "USDA Dietary Guideline (2020) - 10-30% energy", None, "This is info for Protein")
        self.carb = ResultLower("Carbohydrates", " g/day")
        self.fiber = ResultLower("Fiber", " g/day")
        self.fat = ResultLower("Fat", " g/day")
        self.water = ResultLower("Water", " l/day")
        self.vitaminA = ResultLower("Vitamin A", " μg/day", None, "based on Vitamin Calculator:\nhttps://www.omnicalculator.com/health/vitamin")
        self.vitaminC = ResultLower("Vitamin C", " mg/day", None, "based on Vitamin Calculator:\nhttps://www.omnicalculator.com/health/vitamin")
        self.vitaminD = ResultLower("Vitamin D", " μg/day", None, "based on Vitamin Calculator:\nhttps://www.omnicalculator.com/health/vitamin")
        self.vitaminE = ResultLower("Vitamin E", " mg/day", None, "based on Vitamin Calculator:\nhttps://www.omnicalculator.com/health/vitamin")
        self.calcium = ResultLower("Calcium", " mg/day", None, "based on National Institutes of Health:\nhttps://ods.od.nih.gov/factsheets/Calcium-Consumer/")
        self.iron = ResultLower("Iron", " mg/day", None, "based on National Institutes of Health:\nhttps://ods.od.nih.gov/factsheets/Iron-Consumer/")
        self.magnesium = ResultLower("Mangesium", " mg/day", None, "based on National Institutes of Health:\nhttps://ods.od.nih.gov/factsheets/Magnesium-Consumer/")

        self.dri = ft.ExpansionTile(
            title=ft.Text(
                "DRI: Dietary reference intake", 
                size=14, 
                style=ft.TextStyle(weight=ft.FontWeight.BOLD)
            ),
            affinity=ft.TileAffinity.LEADING,
            maintain_state=True,
            tile_padding=ft.padding.symmetric(vertical=0),
            controls=[
                ft.ListView(
                    spacing=8,
                    padding=ft.padding.only(bottom=40),
                    controls=[
                        self.protein,
                        self.carb,
                        self.fiber,
                        self.fat,
                        self.vitaminA,
                        self.vitaminC,
                        self.vitaminD,
                        self.vitaminE,
                        self.calcium,
                        self.iron,
                        self.magnesium,
                    ],
                ),
            ],
        )
        
        self.controls=[
            ft.Container(
                margin=10,
                expand=True,
                bgcolor="white",
                border_radius=20,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(20, 20, 20, 0),
                            gradient=ft.LinearGradient(
                                begin=ft.Alignment(0, -0.6),
                                end=ft.alignment.bottom_center,
                                colors=[
                                    # ft.Colors.ORANGE_300,
                                    # ft.Colors.ORANGE_200,
                                    # ft.Colors.ORANGE_100,
                                    # ft.Colors.ORANGE_50,
                                    ft.Colors.LIME_300,
                                    ft.Colors.LIME_200,
                                    ft.Colors.LIME_100,
                                    ft.Colors.LIME_50,
                                    ft.Colors.WHITE,                                    
                                ],
                            ),                          
                            content=ft.Column(
                                controls=[
                                    Landing(),

                                    ft.Row(
                                        spacing=10,
                                        wrap=True,
                                        controls = [
                                            self.height,
                                            self.weight,
                                            self.age,
                                            self.sex,
                                        ]
                                    ),
                                    ft.Row(
                                        wrap=True,
                                        spacing=0,
                                        vertical_alignment=ft.CrossAxisAlignment.END,
                                        controls = [
                                            self.pal,
                                            ft.Text(
                                                "   * PAL is used to calculate TDEE",
                                                size=10,
                                                ),                                         
                                        ]
                                    ),                                    
                                ]
                            )
                        ),

                        # ft.Divider(height=5, color="lime", leading_indent=20, trailing_indent=20),
                        
                        # Results (scrollable)
                        ft.Container(
                            expand=True,
                            padding=20,
                            content=ft.Column(
                                scroll=ft.ScrollMode.ALWAYS,
                                controls=[
                                    self.bmr,
                                    self.tdee,
                                    self.dri,
                                ]  
                            ),                            
                        )

                    ]
                )
            ),
        ]

    
    # Calculate results
    def calc_bmr(self, height, weight, age, sex):
        if sex == "Male":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        elif sex == "Female":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        self.bmr.result.value = bmr

        self.calc_protein(bmr)
        self.calc_carb(bmr)
        self.calc_fiber(bmr)
        self.calc_fat(bmr)
        self.calc_vitamin(age, sex)
        self.calc_calcium(age,sex)
        self.calc_iron(age,sex)
        self.calc_magnesium(age,sex)
        
        self.page.update()
        
        try: 
            self.calc_tdee(bmr, self.pal.value)
            self.page.update()
        except: pass


    def calc_tdee(self, bmr, pal):
        tdee = round(bmr * pal, 2)
        self.tdee.result.value = tdee
        
    def calc_protein(self, bmr):
        (min_perc, max_perc) = (5, 20) if self.age.value <= 3 else (10, 30)
        min = round(bmr * min_perc / 400, 2)
        max = round(bmr * max_perc / 400, 2)
        self.protein.result.value = str(min) + "-" + str(max)

    def calc_carb(self, bmr):
        (min_perc, max_perc) = (45, 65)
        min = round(bmr * min_perc / 400, 2)
        max = round(bmr * max_perc / 400, 2)
        self.carb.result.value = str(min) + "-" + str(max)

    def calc_fiber(self, bmr):
        self.fiber.result.value = round(bmr / 1000 * 14, 2)

    def calc_fat(self, bmr):
        if self.age.value <= 3:
            (min_perc, max_perc) = (30, 40)
        elif self.age.value <= 18:
            (min_perc, max_perc) = (25, 35)
        else:
            (min_perc, max_perc) = (20, 35)

        min = round(bmr * min_perc / 900, 2)
        max = round(bmr * max_perc / 900, 2)
        self.fat.result.value = str(min) + "-" + str(max)

    def calc_vitamin(self, age, sex):
        if age <= 3:
            self.vitaminA.result.value = 300
            self.vitaminC.result.value = 15
            self.vitaminD.result.value = 15
            self.vitaminE.result.value = 6
        elif age <= 8:
            self.vitaminA.result.value = 400
            self.vitaminC.result.value = 25
            self.vitaminD.result.value = 15
            self.vitaminE.result.value = 7
        elif age <= 13:
            self.vitaminA.result.value = 600
            self.vitaminC.result.value = 45
            self.vitaminD.result.value = 15
            self.vitaminE.result.value = 11
        elif sex == "Female":
            self.vitaminA.result.value = 700
            self.vitaminC.result.value = 65
            self.vitaminD.result.value = 15
            self.vitaminE.result.value = 15
        else:
            self.vitaminA.result.value = 900
            self.vitaminC.result.value = 75
            self.vitaminD.result.value = 15
            self.vitaminE.result.value = 15
        
        
    def calc_vitaminA(self, age, sex):
        if age <= 3:
            amount = 500
        elif age <= 8:
            amount = 400
        elif age <= 13:
            amount = 600
        elif sex == "Female":
            amount = 700
        else: amount = 900
        
        self.vitaminA.result.value = amount

    def calc_vitaminC(self, age, sex):
        if age <=3:
            amount = 15
        elif age <= 8:
            amount = 25
        elif age <= 13:
            amount = 45
        elif age <= 18:
            if sex == "Female":
                amount = 65
            else: amount = 75
        else: amount = 75
                    
        self.vitaminC.result.value = amount
        
    def calc_calcium(self, age, sex):
        if age <= 1:
            amount = 260
        elif age <= 3:
            amount = 700
        elif age <= 8:
            amount = 1000
        elif age <= 18:
            amount = 1300
        elif age <= 50:
            amount = 1000
        elif age <= 70:
            if sex == "Female":
                amount = 1200
            else: amount = 1000
        else:
            amount = 1200
        
        self.calcium.result.value = amount

    def calc_iron(self, age, sex):
        if age <= 1:
            amount = 11
        elif age <= 3:
            amount = 7
        elif age <= 8:
            amount = 10
        elif age <= 18:
            if sex == "Female":
                amount = 15
            else: amount = 11
        elif age <= 50:
            if sex == "Female":
                amount = 18
            else: amount = 8
        else:
            amount = 8
        
        self.iron.result.value = amount

    def calc_magnesium(self, age, sex):
        if age <= 1:
            amount = 75
        elif age <= 3:
            amount = 8
        elif age <= 8:
            amount = 130
        elif age <= 18:
            if sex == "Female":
                amount = "360"
            else: amount = "410"
        elif sex == "Female":
            amount = "310–320"
        else:
            amount = "400–420"
        
        self.magnesium.result.value = amount
        
                        
    # Check if all the input values are valid
    def valueEntered(self, key):
        self.hasValue[key] = True
        if all(value == True for value in self.hasValue.values()):
            self.calc_bmr(self.height.value, self.weight.value, self.age.value, self.sex.value)


    # Show Snackbar when an input value is invalid
    def value_invalid(self):
        self.page.open(ft.SnackBar(
            content=ft.Text(
                "Value must be a number",
                text_align=ft.TextAlign.CENTER,
                ),
            behavior=ft.SnackBarBehavior.FLOATING,
            width=220,
            duration=1500,
            ))
        
    def value_entered(self, param, value_name, value):
        try:
            param.value = float(value)
            self.valueEntered(value_name)
        except:
            param.value = None
            self.value_invalid()
                        
    def height_entered(self, e):
        if e.control.value:
            value = e.control.value
            self.value_entered(self.height, "height", value)                        

    def weight_entered(self, e):
        if e.control.value:
            value = e.control.value
            self.value_entered(self.weight, "weight", value)

    def age_entered(self, e):
        if e.control.value:
            try:
                value = int(e.control.value)
                self.value_entered(self.age, "age", value)
            except: self.value_invalid()

    def sex_selected(self, e):
        self.sex.value = e.control.value
        self.valueEntered("sex")

    def pal_selected(self, e):
        if e.control.value == "Little/no exercise":
            self.pal.value = 1.2
        elif e.control.value == "Exercise 1-2 times/week":
            self.pal.value = 1.4
        elif e.control.value == "Exercise 2-3 times/week":
            self.pal.value = 1.6
        elif e.control.value == "Exercise 3-5 times/week":
            self.pal.value = 1.75
        elif e.control.value == "Exercise 6-7 times/week":
            self.pal.value = 2
            
        self.valueEntered("pal")        

  

### MAIN ###

def main(page: ft.Page):
    
    # page.window.width = 600
    # page.window.height = 800
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.theme=ft.Theme(color_scheme_seed="lime")
    page.padding=0

    app = ft.SafeArea(
        DietaryCalculator([page.window.height, page.window.width]),
    )

    page.add(ft.Container(
        expand=True,
        content=ft.Stack(
            controls=[
                ft.Image(
                    src="background.png",
                    fit=ft.ImageFit.FILL,
                    height=page.window.height,
                    width=page.window.width
                    ),
                app,
            ]),
        )
    )

ft.app(main)

