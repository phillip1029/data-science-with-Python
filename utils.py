import pandas as pd

class CustomerJourneyTransformer:
    def __init__(self, activity_df):
        self.activity_df = activity_df
    
    def transform(self):
        # Sort the dataframe by 'id' and 'date'
        self.activity_df.sort_values(by=['id', 'date'], inplace=True)
        
        # Create a new dataframe with 'next_state_date', 'next_state', and 'journey_order_number' columns
        journey_df = self.activity_df.assign(
            next_state_date=self.activity_df.groupby('id')['date'].shift(-1),
            next_state=self.activity_df.groupby('id')['state'].shift(-1),
            total_purchase = self.activity_df.groupby('id')['purchase_amount'].transform('sum'),
            journey_order_number=self.activity_df.groupby('id').cumcount() + 1
        )
        
        return journey_df

import plotly.graph_objects as go

class CustomerJourneySankey:
    def __init__(self, journey_df):
        self.journey_df = journey_df
    
    def create_sankey_diagram(self):
        # Create a DataFrame with the required columns for Sankey diagram
        sankey_df = self.journey_df.groupby(['state', 'next_state']).size().reset_index(name='count')
        
        # Create a dictionary to map states to unique numeric labels
        state_labels = list(set(sankey_df['state'].unique()) | set(sankey_df['next_state'].unique()))
        state_labels = [str(label) for label in state_labels if pd.notnull(label)]
        state_dict = {label: i for i, label in enumerate(state_labels)}
        
        # Create the Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node = dict(
                pad = 15,
                thickness = 20,
                line = dict(color = "black", width = 0.5),
                label = state_labels,
                color = "blue"
            ),
            link = dict(
                source = [state_dict[state] for state in sankey_df['state']],
                target = [state_dict[state] for state in sankey_df['next_state']],
                value = sankey_df['count']
            )
        )])
        
        fig.update_layout(title_text="Customer Journey Sankey Diagram", font_size=10)
        fig.show()    