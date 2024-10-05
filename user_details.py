# User details 

print("Hello! We are going to ask for details about you for a more personalised recommendation.")
print("If you prefer not to enter these details, that is fine!")
print("")

valid_age = False
print("Q1 of 3")
print("Please enter your age as a whole number:")
print("(You can also press enter without entering anything to skip this question.)")
age = input()
while valid_age == False:
    try:
        int(age)
        valid_age = True 
    except ValueError:
        if age.strip() == "":
            valid_age = True
        else: 
            print("Invalid input. Try again!")
            age = input()

print("")
valid_tone = False
print("Q2 of 3")
print("Please describe your skin tone. Is it Fair, Medium or Dark?") 
print("(You can also press enter without entering anything to skip this question.)")
skin_tone = input()
while valid_tone == False:
    if skin_tone.strip() == "":
        valid_tone = True 
    else:
        check = skin_tone.strip().upper()
        if check == "FAIR" or check == "MEDIUM" or check == "DARK":
            valid_tone = True 
        else:
            print("Invalid input. Try again!")
            skin_tone = input()




print("")
valid_fitness = False
print("Please describe your fitness level. Is it Good, Medium or Poor?")
print("(You can also press enter without entering anything to skip this question.)")
fitness = input()
while valid_fitness == False:
    if fitness.strip() == "":
        valid_fitness = True 
    else:
        check = fitness.strip().upper()
        if check == "GOOD" or check == "MEDIUM" or check == "POOR":
            valid_fitness = True 
        else:
            print("Invalid input. Try again!")
            fitness = input()


