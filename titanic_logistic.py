import numpy as np 
import pandas as pd 

from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
import seaborn as sns
sns.set(style="white") #white background style for seaborn plots
sns.set(style="whitegrid", color_codes=True)


# Read CSV train data file into DataFrame
train_df = pd.read_csv("./datasets/train.csv")

# Read CSV test data file into DataFrame
test_df = pd.read_csv("./datasets/test.csv")


def density(column):
    plt.hist(train_df[column], bins=15,histtype=u'step',density=True)
    # ax = train_df[column].hist(bins=15, density=True, stacked=True, color='teal', alpha=0.6)
    train_df[column].plot(kind='density', color='red')
    # ax.set(xlabel=column)
    plt.xlabel(column)
    plt.ylabel('Density')
    plt.savefig(f'static/image/{column}.png')
    plt.cla()
    # plt.show()


def preprocessing():
    train_data = train_df.copy()
    train_data["Age"].fillna(train_df["Age"].median(skipna=True), inplace=True)
    train_data["Embarked"].fillna(train_df['Embarked'].value_counts().idxmax(), inplace=True)
    train_data.drop('Cabin', axis=1, inplace=True)

    ## Create categorical variable for traveling alone
    train_data['TravelAlone']=np.where((train_data["SibSp"]+train_data["Parch"])>0, 0, 1)
    train_data.drop('SibSp', axis=1, inplace=True)
    train_data.drop('Parch', axis=1, inplace=True)

    #create categorical variables and drop some variables
    training=pd.get_dummies(train_data, columns=["Pclass","Embarked","Sex"])
    training.drop('Sex_female', axis=1, inplace=True)
    training.drop('PassengerId', axis=1, inplace=True)
    training.drop('Name', axis=1, inplace=True)
    training.drop('Ticket', axis=1, inplace=True)

    final_train = training
    final_train.to_csv('static/csv_file/final_train.csv' , encoding='utf-8')
    test_data = test_df.copy()
    test_data["Age"].fillna(train_df["Age"].median(skipna=True), inplace=True)
    test_data["Fare"].fillna(train_df["Fare"].median(skipna=True), inplace=True)
    test_data.drop('Cabin', axis=1, inplace=True)

    test_data['TravelAlone']=np.where((test_data["SibSp"]+test_data["Parch"])>0, 0, 1)

    test_data.drop('SibSp', axis=1, inplace=True)
    test_data.drop('Parch', axis=1, inplace=True)

    testing = pd.get_dummies(test_data, columns=["Pclass","Embarked","Sex"])
    testing.drop('Sex_female', axis=1, inplace=True)
    testing.drop('PassengerId', axis=1, inplace=True)
    testing.drop('Name', axis=1, inplace=True)
    testing.drop('Ticket', axis=1, inplace=True)

    final_test = testing
    final_test.to_csv('static/csv_file/final_test.csv' , encoding='utf-8')
    return (final_train , final_test)
# density('Fare')

