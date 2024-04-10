
import pandas as pd

data = {'Standard price entries & exits': '89,588', 'Reduced price entries & exits': '113,780', 'Season ticket entries & exits': '27,184', 'Total entries & exits': '230,552', 'Interchanges made between connecting services': '0'}
dat2 = {'Stan price entries & exits': '89,588', 'Reduced price entries & exits': '113,780', 'Season ticket entries & exits': '27,184', 'Total entries & exits': '230,552', 'Interchanges made between connecting services': '0'}
print(type(data))

df = pd.DataFrame([data])

df3 = pd.DataFrame([dat2])



df2 = df 


df2 = df3

# Print the DataFrame
print(df2)
