import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess_data():

    # Load the data
    df = pd.read_csv('./enterpret.csv')

    #  Remove rows where 'Content' is '<AUDIO_CONTENT>' or empty string
    df = df[(df['Content'] != '<AUDIO_CONTENT>') & (df['Content'].str.strip() != '')]

    # Remove rows where 'Reasons' and 'Content' is NaN
    df = df[df['Reasons'].notna()]  # Remove rows where 'reason' is NaN
    df = df[df['Content'].notna()]  # Remove rows where 'reason' is NaN

    df = df[(df['Reasons'].str.strip() != '') & (df['Reasons'].str.strip() != float('NaN')) ]

    # Handle missing values in 'source', 'sentiment', and 'type'
    # Fill missing values with the mode
    for column in ['Source', 'Type', 'Record Sentiment']:
        mode_value = df[column].mode()[0]
        df[column] = df[column].fillna(mode_value)

    # Convert 'source', 'sentiment', and 'type' into categorical classes
    label_encoders = {}
    for column in ['Source', 'Type', 'Record Sentiment']:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le  # Store the label encoder if you need to inverse transform later


    data = pd.DataFrame()
    for column in ['Source', 'Type', 'Record Sentiment','Content','Reasons']:
        data[column]=df[column]
    df=data


    # Remove rows where 'Reasons' is empty
    df = df[df['Reasons'].map(len)>0]

    # Pre-process the strings of df['Reasons']
    temp = pd.DataFrame()
    i=0
    temp['Reasons']=df['Reasons']
    for it in df['Reasons']:
        if(len(it[0])>2):
            temp['Reasons'][i]=it[0]
            i+=1
    #     print(it[0])
    temp.head()
    df['Reasons']=temp['Reasons']
    return df





