# Step 1 — understand the mess before cleaning it
print("=== MISSING VALUES (top 20 columns) ===")
missing = df_raw.isnull().sum()
missing_pct = (missing / len(df_raw) * 100).round(1)
missing_df = pd.DataFrame({"count": missing, "pct": missing_pct})
print(missing_df[missing_df["count"] > 0].sort_values("pct", ascending=False).head(20))

print("\n=== DUPLICATES ===")
print(f"Duplicate rows: {df_raw.duplicated().sum()}")


## check columns each unique value
# Check one column first
#  .explode()

languages = df_clean["LanguageHaveWorkedWith"].dropna().str.split(";").explode()
print(languages.value_counts().head(15))

# filter keywords in all columns, especially if we have a lot of columns

# Search all column names containing your keywords
# obviously redo this on what  we're looking for
keywords = [
    "Language",
    "Database",
    "Platform",
    "Framework",
    "Age",
    "Country",
    "Employment",
    "Education",
    "Learn",
]

for keyword in keywords:
    matches = [col for col in df_clean.columns if keyword in col]
    if matches:
        print(f"\n{keyword}:")
        for col in matches:
            print(f"  {col}")
