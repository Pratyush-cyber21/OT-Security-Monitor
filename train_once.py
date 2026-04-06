from ai_engine import train_models
print("Training ClearCatchICS models on BATADAL normal data...")
cols = train_models('data/batadal_train1.csv')
print(f"Features used: {cols}")
print("PKL files saved to models/ folder.")
print("DONE. Commit models/ folder to GitHub before demo.")
