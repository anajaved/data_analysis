import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename = 'titanic-data.csv'
titanic_df = pd.read_csv(filename)
#titanic_df.info()

###examining factors influence survival###

#1 = pclass & age based on survival
'''
age_data=titanic_df.groupby(['Survived','Age'], as_index=False)[['Pclass']].mean()
died= plt.scatter(age_data.iloc[:77]['Age'],age_data.iloc[:77]['Pclass'], label='Deceased', c='green', marker='s' )
lived= plt.scatter(age_data.iloc[77:]['Age'],age_data.iloc[77:]['Pclass'], label='Survived', c='orange' )

#line of best fit
x=age_data.iloc[:77]['Age']
y=age_data.iloc[:77]['Pclass']
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), c='green')

w=age_data.iloc[77:]['Age']
z=age_data.iloc[77:]['Pclass']
plt.plot(np.unique(w), np.poly1d(np.polyfit(w, z, 1))(np.unique(w)), c='orange')

plt.grid()
plt.title('Effects of Age and Class on Survival')
plt.xlabel("Age")
plt.ylabel("Average Class (1= upper, 3=lower)")
plt.yticks([1,2,3])
plt.legend()
plt.show()
'''

#2= age and survival 
'''
living_data=titanic_df.groupby(['Survived'], as_index=False)['Age'].get_group(1).dropna() 
dead_data = titanic_df.groupby(['Survived'], as_index=False)['Age'].get_group(0).dropna() 
#passengers w/no age were dropped

lived= plt.hist(living_data, label='Survived', color='orange')
died= plt.hist(dead_data, label='Deceased', alpha=0.5, color='gray')

plt.grid()
plt.title('Number of Living/Deceased Passengers by Age')
plt.xlabel("Age (in years)")
plt.ylabel("Frequency")
plt.legend()
plt.show()
'''

#3= survival and sex
'''
dead=titanic_df.groupby(['Survived'], as_index=False)['Sex'].get_group(0)
living=titanic_df.groupby(['Survived'], as_index=False)['Sex'].get_group(1)


def create_bar (life_status):
    
    men_total = len(life_status[life_status == 'male'])
    women_total = len(life_status[life_status == 'female'])   
    y = [men_total, women_total]
    x = [0, 1]
    D = {'male': men_total, 'female': women_total}
    plt.bar(range(len(D)), D.values(), align='center',alpha=0.5, width=.60, color='green') 
        #bar color was manipulated for each bar chart 
    plt.xticks(range(len(D)), D.keys())
    plt.xlabel("Gender")
    plt.ylabel("Frequency")
    plt.grid()
    
create_bar(living)
plt.title('Number of Passengers who Survived by Gender')
plt.show()

create_bar(dead)
plt.title('Number of Passengers who Died by Gender')
plt.show()
'''