from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class CrimeAnalyzer:
    def __init__(self, df):
        self.df = df
        self.model = RandomForestClassifier(n_estimators=150, random_state=42)
        self._train_model()
    
    def _train_model(self):
        # Prepare features and target for training
        X = self.df[['YEAR']].copy()
        X['STATE_CODE'] = self.df['STATE/UT'].astype('category').cat.codes
        y = self.df['CRIME_TYPE']
        
        # Split data and train the model
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
    
    def predict_crime_trend(self, state, year):
        # Ensure state exists in the dataset (case-insensitive)
        state_matches = self.df['STATE/UT'].str.upper() == str(state).upper()
        if not state_matches.any():
            available_states = sorted(self.df['STATE/UT'].unique())
            raise ValueError(f"State '{state}' not found in dataset. Available states: {', '.join(available_states)}")
        
        # Get the precomputed state code
        state_code = self.df[state_matches]['STATE/UT'].map(
            dict(zip(self.df['STATE/UT'], self.df['STATE/UT'].astype('category').cat.codes))
        ).iloc[0]
        
        # Prepare input data and predict
        try:
            input_data = [[int(year), state_code]]
            prediction = self.model.predict(input_data)[0]
        except ValueError as ve:
            raise ValueError(f"Invalid year '{year}': {str(ve)}. Year must be an integer.")
        except Exception as e:
            raise RuntimeError(f"Model prediction failed: {str(e)}")
        
        # Calculate historical dominant crime
        state_data = self.df[state_matches]
        if not state_data.empty:
            dominant_crime = state_data.groupby('CRIME_TYPE')['COUNT'].sum().idxmax()
            return f"{prediction} (Historical dominant: {dominant_crime})"
        return prediction