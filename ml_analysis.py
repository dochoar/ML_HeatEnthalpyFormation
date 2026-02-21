import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import os

# Set style for plots
sns.set_theme(style="whitegrid")

def run_analysis(file_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Load Data
    df = pd.read_excel(file_path)
    
    # Target and features (computational methods)
    target = 'Expt'
    # Exclude Sl and System names from features
    feature_cols = [c for c in df.columns if c not in ['Sl', 'System', 'Expt']]
    
    # Data Cleaning: Convert all computational columns and target to numeric, coercing errors to NaN
    for col in feature_cols + [target]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop rows where target is missing or all features are missing (any 'failed')
    original_len = len(df)
    df = df.dropna(subset=[target])
    df = df.dropna(subset=feature_cols, how='any')
    new_len = len(df)
    
    if original_len != new_len:
        print(f"Dropped {original_len - new_len} rows containing 'failed' or NaN values.")
        print(f"Remaining entries: {new_len}")

    # 2. Benchmark Existing Methods
    maes = {}
    for col in feature_cols:
        maes[col] = mean_absolute_error(df[target], df[col])
    
    mae_df = pd.DataFrame(list(maes.items()), columns=['Method', 'MAE']).sort_values('MAE')
    print("\nTop 10 Computational Methods by MAE:")
    print(mae_df.head(10))
    
    # 3. Machine Learning Models
    X = df[feature_cols]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    
    ml_results = []
    best_model = None
    best_mae = float('inf')
    predictions = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        ml_results.append({'Method': f'ML_{name}', 'MAE': mae})
        predictions[name] = y_pred
        
        if mae < best_mae:
            best_mae = mae
            best_model = (name, model)
            
        print(f"{name} -> MAE: {mae:.4f}, R2: {r2:.4f}")

    # Combine all results for comparison
    all_results = pd.concat([mae_df, pd.DataFrame(ml_results)]).sort_values('MAE')
    
    # 4. Plots
    
    # Plot 1: MAE Comparison (Top 15)
    plt.figure(figsize=(12, 8))
    sns.barplot(data=all_results.head(20), x='MAE', y='Method', palette='viridis')
    plt.title('Top 20 Methods/Models by Mean Absolute Error (MAE)')
    plt.xlabel('MAE (kcal/mol or applicable unit)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'mae_comparison.png'))
    plt.close()

    # Plot 2: Predicted vs Experimental for Best ML Model
    name, model = best_model
    y_pred = model.predict(X_test)
    
    plt.figure(figsize=(10, 8))
    plt.scatter(y_test, y_pred, alpha=0.5, edgecolors='w')
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    plt.title(f'Experimental vs Predicted ({name})')
    plt.xlabel('Experimental Value')
    plt.ylabel('Predicted Value')
    plt.text(y_test.min(), y_test.max() * 0.9, f'MAE: {best_mae:.4f}\nR2: {r2_score(y_test, y_pred):.4f}', 
             bbox=dict(facecolor='white', alpha=0.5))
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'predicted_vs_experimental.png'))
    plt.close()

    # Plot 3: Correlation Matrix of Top Methods
    top_methods = mae_df.head(10)['Method'].tolist()
    plt.figure(figsize=(12, 10))
    sns.heatmap(df[top_methods + [target]].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix of Top 10 Methods and Experimental Data')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'))
    plt.close()

    print(f"\nAnalysis complete. Plots saved in {output_dir}")
    return all_results

if __name__ == "__main__":
    file_path = "/home/david/Escritorio/ML_HeatEnthalpyFormation/data/raw/SI_data_2020.xlsx"
    output_dir = "/home/david/Escritorio/ML_HeatEnthalpyFormation/analysis_results"
    results = run_analysis(file_path, output_dir)
