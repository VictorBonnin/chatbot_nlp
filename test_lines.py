import csv
import os

input_filename = 'projet_data/train.csv'
temp_filename = 'projet_data/train_temp.csv'

valid_sentiments = {"neutral", "negative", "positive"}

with open(input_filename, encoding='latin1', newline='') as infile, \
     open(temp_filename, mode='w', encoding='latin1', newline='') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    kept = 0
    removed = 0

    for row in reader:
        sentiment = row.get('sentiment')
        # On ne garde que les clés valides (qui sont dans fieldnames et pas None)
        filtered_row = {k: v for k, v in row.items() if k in fieldnames and k is not None}
        if sentiment and sentiment.strip().lower() in valid_sentiments:
            writer.writerow(filtered_row)
            kept += 1
        else:
            removed += 1

print(f"Lignes gardées : {kept}")
print(f"Lignes supprimées : {removed}")

os.replace(temp_filename, input_filename)
print(f"Le fichier '{input_filename}' a été nettoyé et mis à jour.")
