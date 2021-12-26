import pandas as pd


data = pd.read_csv('persona.csv')
print(data)

# checking the data
data.head()
data.tail()
data.shape
data.describe().T
data.info()
data.isnull().sum()


#unique sources
unique = data["SOURCE"].nunique()
freuencies = data["SOURCE"].value_counts()
print("Number of unique value:",  unique)
print("Frequencies: ", freuencies)


#unique prices
price_unique = data['PRICE'].nunique()
print("Unique price:", price_unique)


# price counts
price_count = data['PRICE'].value_counts()
print('Total count of price:','\n', price_count)


# count of countries
countr = data['COUNTRY'].value_counts()
print("Number of in the sales of countries",'\n',countr)


# total sales
sales_total = data.groupby("COUNTRY")["PRICE"].sum()
print(sales_total)


# sales according to source
sal_of_sour = data.groupby("SOURCE")["PRICE"].count()
print('Source:', sal_of_sour)


# price mean according to countries
mean_of_countr = data.groupby("COUNTRY")["PRICE"].mean()
print(mean_of_countr)


# price mean according to source
mean_of_source = data.groupby("SOURCE")["PRICE"].mean()
print(mean_of_source)



# calculating the country-source as price.
groups = ["COUNTRY", "SOURCE"]
groups_values = data.groupby(groups)["PRICE"].mean()
print("group values of countries and sources",groups_values)


#2-country,sex,age,source
all_var = ['COUNTRY', 'SOURCE','AGE','SEX']
var_vals = data.groupby(all_var)["PRICE"].mean()
print("All values by mean: ",var_vals)


#3- preparing
agg_df = pd.DataFrame(data.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"mean"})).reset_index()
agg_df.columns = ["COUNTRY","SOURCE","SEX","AGE","PRICE"]
agg_df.sort_values("PRICE", ascending=False,inplace= True)


#5- splitting the all types of age
agg_df["AGE"].max()#66
agg_df["AGE"].min()#15
#0_18 , 19_23 , 24_30 , 31_40 , 41_66
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"],[0,18,23,30,40,66], labels=["1_18","19_23","24_30","31_40","41_66"], ordered=False)
print(agg_df)


#6-
#defining new customer(persona)
agg_df = pd.DataFrame([{"customers_level_based":str(i[0]+"_"+i[1]+"_"+i[2]+"_"+i[5]).upper(),
               "PRICE": i[4]} for i in agg_df.values])

agg_df = agg_df[:].groupby("customers_level_based").agg({"PRICE":"mean"})


#7 -
# splitting new customers for segmentation.
agg_df["SEGMENT"] = pd.cut(agg_df["PRICE"],4, labels=["D","C","B","A"])
agg_df = agg_df.reset_index()
print(agg_df.head(20))


#8-
# catch a new user
def new_customer(data, new_user):
    print(data[data["customers_level_based"] == new_user])


# Question: If we have a user information as;
# country: Turkey
# source: Android
# sex: Female
# age: 31-40
# how much money does she get?
new_customer(agg_df, "TUR_ANDROID_FEMALE_31_40")

# Like above question different type of person.
new_customer(agg_df, "FRA_IOS_FEMALE_31_40")
