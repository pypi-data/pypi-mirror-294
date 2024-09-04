import math
import time
import json
import sys
from pathlib import Path

# initial creation of the database
plans_storage_file_path = Path.home()/"plans.json"

if not plans_storage_file_path.exists():
    initial_data = {

    }

    with plans_storage_file_path.open("w") as file:
           json.dump(initial_data, file, indent=4)

# functions
## coloured text function
def print_red(text):
    print(f"\033[31m{text}\033[0m")

def print_blue(text):
    print(f"\033[34m{text}\033[0m")

def print_green(text):
    print(f"\033[32m{text}\033[0m")

## new plan mode
def new_plan_mode() :
    mode = (input('\n\033[34mfirst of all please let me know how you would like to manage your money \n\nyou can either use the default preset or create a custom one \033[0m\n\033[3mdefault/custom\033[0m\n\n')).lower()


    if mode == 'default':
        print('\n\033[34myou will be choosing the default scheme, which includes\033[0m \n\n \033[32mfood ~ 30% \n necessities ~ 30% \n transportation ~ 10% \n savings ~ 15% \n extra ~ 15% \n \033[0m')
        calculated_budget = default_calc()
    elif mode == 'custom':
        print('\n\033[34min the custom scheme, you can define the different categories and the proportion of money for them\033[0m')
        calculated_budget = custom_calc()
    else:
        print_red('please choose from either the default or custom mode')

## default calculation mode
def default_calc() :
    default_plan = {

    }
    try:
        budget = int(input('\033[34mwhat is your budget?\033[0m\n\n'))
        default_plan.update({'budget':budget})
        food_budget = budget*0.3
        default_plan.update({'food_budget':food_budget})
        necessities_budget = budget*0.3
        default_plan.update({'necessities_budget':necessities_budget})
        transportation_budget = budget*0.1
        default_plan.update({'transportation_budget':transportation_budget})
        savings_budget = budget*0.15
        default_plan.update({'savings_budget':savings_budget})
        extra_budget  = budget*0.15
        default_plan.update({'extra_budget':extra_budget})
        print_blue('\naccording to you budget, this is how much money you are able to spend on each category:')
        print('---------')
        print_green('food ~ ' + str(food_budget) + '$')
        print_green('necessities ~ ' + str(necessities_budget) + '$')
        print_green('transportation ~ ' + str(transportation_budget) + '$')
        print_green('savings ~ ' + str(savings_budget) + '$')
        print_green('extra ~ ' + str(extra_budget) + '$')
        print('---------')
        save_the_plan(default_plan)
    except ValueError:
       print_red('\nplease input numbers only\n')
       time.sleep(1)

## custom calculations mode

def custom_calc() :
    custom_categories = {

    }
    total_proportion = 0.0
    remaining = 100
    category_appender = ''
    # for updating the custom category dictionary
    while remaining > 0:
            category_appender = input('\n\033[34mwhat should the name of the category be?\033[0m\n\n')
            try:
                category_proportion = float(input('\n\033[34mwhat proportion of your budget should it receive? enter a whole number percentage\033[0m\n\n'))
                if total_proportion + category_proportion > 100:
                    print_red('\nthe total proportion exceeds 100%, please enter a smaller value')
                else:
                    custom_categories.update({category_appender: category_proportion})
                    total_proportion += category_proportion

                remaining = 100 - total_proportion
                print_red(f"\nremaining proportion = {remaining}%")
            except ValueError:
                print_red('\nplease enter numbers only\n')


    ### calculation of the proportions
    try:
       budget = int(input('\n\033[34mwhat is your budget?\n\n\033[0m'))
       print('\n---------')
       for custom_category_name, custom_category_value in custom_categories.items():
               custom_category_name_budget = budget *custom_category_value*0.01
               print_green(f'{custom_category_name} ~  {custom_category_name_budget} $')
    except ValueError:
       print_red('please input numbers only')

    save_the_plan(custom_categories)

## save function
def save_the_plan(save_plan_data):
    save = (input('\033[34mwould you like to save this file? y/n  \033[0m')).lower()
    if save == 'y' :
        new_saved_plan_name = input('\nwhat name would you like to give this plan?\n')
        saved_plans[new_saved_plan_name] = save_plan_data
        with plans_storage_file_path.open("w") as file:
                json.dump(saved_plans,file,indent=4)
        print_green('\nsaved!\n')


## plan modification funciton
def plan_modification(plan_of_choice):
    while True:
        category_to_modify = input('\nwhich category do you want to change?\n')
        if category_to_modify in saved_plans[plan_of_choice].keys():
            plan_modder_dictionary = saved_plans[plan_of_choice]
            money_change = input('add or subtract? ')
            # adding
            if money_change == 'add' or money_change == '+':
                money = float(input('by how much? '))
                plan_modder_dictionary[category_to_modify] += money
                plan_modder_dictionary['budget'] +=money
                print(f'\nsuccess! The new budget for {category_to_modify} is {plan_modder_dictionary[category_to_modify]}')
                print(f'\nsince you have added funds to a category, the total budget has been updated to {plan_modder_dictionary['budget']} $')
            # subtaction
            elif money_change == 'subtract' or money_change == '-':
                money = float(input('by how much? '))
                plan_modder_dictionary[category_to_modify] -= money
                print(f'\nsuccess! The new budget for {category_to_modify} is {plan_modder_dictionary[category_to_modify]}')
                print(f'\nsince you have removed funds from a category, the total budget remains unchanged at {plan_modder_dictionary['budget']} $')
                if plan_modder_dictionary[category_to_modify] < 0:
                    print(f'be aware that you have gone overbudget for the "{category_to_modify}" category, by {plan_modder_dictionary[category_to_modify]} $!')

                # saving the user's changes to the plan
            with plans_storage_file_path.open('w') as file:
                json.dump(saved_plans, file, indent=4)
        # allow user to exit
        elif category_to_modify == 'exit' or category_to_modify == 'none':
            print('\n\nthank you for using eduwallet!')
            time.sleep(1)
            sys.exit()
        # in case of an invalid category
        else:
            print_red('please enter a valid category to modify')
            time.sleep(1)

# dictionaries
saved_plans = {
   'plan1' : {

   }
}


# opening the database
with open(plans_storage_file_path, 'r') as file:
   saved_plans = json.load(file)

# Initial plan picker and welcome message
print_blue('welcome to eduwallet!\n')
while True :
    plan_mode = (input('\033[34mwould you like to create a new plan, continue with a saved plan or delete a saved plan?\033[0m \n\033[3mnew plan/saved plan/delete plan\033[0m\n\n')).lower()

    if plan_mode in ['new plan','new'] :
        new_plan_mode()
    elif plan_mode == 'saved plan' or plan_mode == 'saved':
        print_blue('\nhere is a list of the available plans:')
        for plan in saved_plans.keys():
            print(plan)
        while True:
            chosen_plan = input('\n\033[34mwhich plan would you like to choose? \n\033[0m')
            if chosen_plan in saved_plans:
                print_blue(f'\nthe budget info for {chosen_plan} is:\n')
                for saved_key, saved_value in saved_plans[chosen_plan].items():
                    print_green(f'{saved_key} ~  {saved_value} $')
                    if saved_value < 0:
                        print_red(f'\033[31mbe aware that you have gone overbudget for the "{saved_key}" category, by {saved_value} $!\033[0m')
                # ask user if they wanna change the info in their plan
                wanna_modify_plan = input('\n\033[34mwould you like to make any adjustments to the plan? y/n \033[0m')
                if wanna_modify_plan == 'y' or wanna_modify_plan == 'yes':
                   plan_modification(chosen_plan)
            elif chosen_plan in ['show','show plans']:
                print('\n')
                for plan in saved_plans.keys():
                    print(plan)

            elif chosen_plan in ['exit','quit','none']:
                sys.exit()

            else:
             print_red('\nyou have not chosen a valid plan. please try again')
             time.sleep(1)

    elif plan_mode in ['delete plan','delete','del','remove','rm']:
        print_blue('\nhere is a list of the available plans:')
        for plan in saved_plans.keys():
            print(plan)
        while True:
            chosen_plan_to_delete = input('\n\033[31mwhich plan would you like to remove? \n\033[0m')
            if chosen_plan_to_delete in saved_plans:
                confirm_delete = input(f'\033[31mare you sure you want to remove the {chosen_plan_to_delete} plan? y/n \033[0m')
                if confirm_delete in ['y','yes']:
                    del saved_plans[chosen_plan_to_delete]
                    print_red(f'\nthe plan {chosen_plan_to_delete} has been removed\n')
                elif confirm_delete in ['n','no']:
                    print_red(f'\nthe plan {chosen_plan_to_delete} was not deleted\n')
                else:
                    print_red('\nplease confirm your choice\n')
                    time.sleep(1)
                with plans_storage_file_path.open('w') as file:
                    json.dump(saved_plans,file,indent=4)
            elif chosen_plan_to_delete in ['exit','quit','stop','cancel','none']:
                break
            elif chosen_plan_to_delete in ['show','show plans']:
                print('\n')
                for plan in saved_plans.keys():
                    print(plan)
            else:
                print_red('\nyou have not chosen a valid plan. please try again')
                time.sleep(1)


    elif plan_mode == 'quit' or plan_mode == 'exit':
        sys.exit()

    else:
        print_red('\nplease select the mode you would like to use\n')
        time.sleep(1)
