import pandas as pd
import numpy as np
from faker import Faker
from ..data_version_diff import data_version_diff, display_data_version_diff

fake = Faker()
Faker.seed(123)
np.random.seed(123)

# --- TESTING USING DUMMY DATA ---

n_old = 100

df_old = pd.DataFrame({
    "user_id": range(1, n_old + 1),
    "age": np.random.randint(18, 70, size=n_old),
    "income": np.random.normal(loc=5000, scale=15000, size=n_old),
    "email": [fake.email() for _ in range(n_old)],
    "signup_date": [fake.date_between(start_date="-2y", end_date="today") for _ in range(n_old)],
    "country": [fake.country() for _ in range(n_old)],
})

#introduce missing values in df_old
age_missing_idx = np.random.choice(df_old.index, size=10, replace=False)
df_old.loc[age_missing_idx, "age"] = np.nan

email_missing_idx = np.random.choice(df_old.index, size=3, replace=False)
df_old.loc[email_missing_idx, "email"] = np.nan

#create df_new
df_new = df_old.copy()

#add rows for row count change
n_new_rows = 20

new_rows = pd.DataFrame({
    "user_id": range(df_old["user_id"].max() + 1, df_old["user_id"].max() + 1 + n_new_rows),
    "age": np.random.randint(18, 70, size=n_new_rows),
    "income": np.random.normal(loc=60000, scale=20000, size=n_new_rows),
    "email": [fake.email() for _ in range(n_new_rows)],
    "signup_date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(n_new_rows)],
    "country": [fake.country() for _ in range(n_new_rows)],
})
df_new = pd.concat([df_new, new_rows], ignore_index=True)

#column removal
df_new = df_new.drop(columns=["country"])

#column addition
df_new["last_login_date"] = [
    fake.date_between(start_date="-6m", end_date="today") for _ in range(len(df_new))
]

## missing value changes
#reduce missing ages (fill some)
df_new['age'] = df_new['age'].fillna(df_new['age'].median())

#introduce missing income values
income_missing_idx = np.random.choice(df_new.index, size=8, replace=False)
df_new.loc[income_missing_idx, "income"] = np.nan

## data type change
df_new["age"] = df_new["age"].astype(str)

## sanity checks
# df_old.info()
# df_new.info()

# df_old.head()
# df_new.head()

#result = data_version_diff(df_old, df_new)

result = data_version_diff(df_old, df_new)
display_data_version_diff(result)
