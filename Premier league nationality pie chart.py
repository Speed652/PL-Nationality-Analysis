# libraries
import pandas as pd
import matplotlib.pyplot as plt


# fbref table link
url_df = 'https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats#stats_gca'

df = pd.read_html(url_df)[0]
df.head()
# creating a data with the same headers but without multi indexing
df.columns = [' '.join(col).strip() for col in df.columns]

df = df.reset_index(drop=True)
df.head()

# creating a list with new names
new_columns = []
for col in df.columns:
  if 'level_0' in col:
      new_col = col.split()[-1]  # takes the last name
  else:
      new_col = col
  new_columns.append(new_col)

# rename columns
df.columns = new_columns
df = df.fillna(0)

df['Age'] = df['Age'].str[:2]
df['Position_2'] = df['Pos'].str[3:]
df['Position'] = df['Pos'].str[:2]
df['Nation'] = df['Nation'].str.split(' ').str.get(1)
df['League'] = df['Comp'].str.split(' ').str.get(1)
df['League_'] = df['Comp'].str.split(' ').str.get(2)
df['League'] = df['League'] + ' ' + df['League_']
df = df.drop(columns=['League_', 'Comp', 'Rk', 'Pos','Matches'])

df['Position'] = df['Position'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})
df['Position_2'] = df['Position_2'].replace({'MF': 'Midfielder', 'DF': 'Defender',
                                                 'FW': 'Forward', 'GK': 'Goalkeeper'})
df['League'] = df['League'].fillna('Bundesliga')

# Normalize the 'League' column and filter
df['League'] = df['League'].str.strip()  # Removes leading/trailing spaces
df = df[df['League'].str.contains('Premier League', case=False, na=False)]
print(df.info)

nation_counts = df['Nation'].value_counts()

# Define a threshold for major nationalities
threshold = 10  # Example threshold: nationalities with less than 5 players are considered minor
major_nations = nation_counts[nation_counts >= threshold]
minor_nations = nation_counts[nation_counts < threshold]
major_nations['Other'] = minor_nations.sum()  # Sum up all minor nationalities under 'Other'

# Plotting the pie chart
plt.figure(figsize=(10, 8))
plt.pie(major_nations, labels=major_nations.index, autopct='%1.1f%%', startangle=140)
plt.title('Share of Players by Nationality in the Premier League (Major Nationalities)')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Show the plot
plt.show()