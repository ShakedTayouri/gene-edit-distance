import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv('results/Esp3I_Obfuscation_3_fragments.csv')
    filtered_df = df.drop_duplicates(subset=['Toxin IDs'])[['Toxin IDs', 'GED score', 'Running Time (seconds)']]
    filtered_df.to_csv('results/Filteres_Esp3I_Obfuscation_3_fragments.csv', index=False)

    print("File saved successfully with unique IDs!")