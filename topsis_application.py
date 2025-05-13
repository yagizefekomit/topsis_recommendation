import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('Finalized_numeric.csv')

# beneficial criteria for our matrix
benefit_criteria = ['benefit', 'benefit', 'benefit', 'benefit', 'benefit', 'benefit', 'cost', 'cost']


# TOPSIS recommendation function
# Weight will be assigned from the user
def topsis_recommendation(df: pd.DataFrame, weights: list, criteria: list):
    """
    data: pd.DataFrame, alternatives x criteria
    weights: list of 8 numeric values (importance of each criterion)
    WEIGHT LIST ORDER: [NR - Display,NR - Performance,NR - Battery,NR - Camera,RAM_Kapasitesi_int,Hafiza_Kapasitesi_GB,Agirlik_int,Fiyat_int]
    criteria: list of 'benefit' or 'cost' strings for each criterion
    returns: index of the best alternative
    """
    # Weights distribution
    weights = np.array(weights) / np.sum(weights)  # Total of weights should be 1

    # Normalize the data using vector normalization
    norm_data = df.iloc[:,2:] / np.sqrt((df.iloc[:,2:]**2).sum())

    # Apply weights to the normalized data
    weighted_data = norm_data * weights

    # Identify the ideal and anti-ideal solutions
    ideal = np.where(np.array(criteria) == 'benefit', weighted_data.max(), weighted_data.min())  # if it is beneficial, take max, else min
    anti_ideal = np.where(np.array(criteria) == 'benefit', weighted_data.min(), weighted_data.max()) # if it is beneficial for ideal, take min, else max

    # Calculate the distance to the ideal and anti-ideal solutions
    dist_to_ideal = np.sqrt(((weighted_data - ideal) ** 2).sum(axis=1))
    dist_to_anti_ideal = np.sqrt(((weighted_data - anti_ideal) ** 2).sum(axis=1))

    # Calculate the TOPSIS Score
    topsis_scores = dist_to_anti_ideal / (dist_to_ideal + dist_to_anti_ideal)

    best_index = topsis_scores.idxmax()

    return best_index, topsis_scores[best_index]


user_weights = [7, 8, 7, 9, 4, 5, 6, 10]  # Example weights
# Excel'deki dosyaya göre ağırlık denemesi
user_weights = [0.053522102,0.135796266, 0.054543895, 0.094948131, 0.124045032, 0.221139148, 0.099421148, 0.216584278]

recommended_index = topsis_recommendation(df, user_weights, benefit_criteria)
#print(df.iloc[recommended_index, [0,1]])
print(recommended_index)