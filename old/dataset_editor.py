from flask import Flask, render_template, request
import pandas as pd
import csv

app = Flask(__name__)



@app.route('/dataset_editor', methods=["GET", "POST"])
def d_editor():
    display_table = []
    unique_tags = []
    if request.method == "POST":
        if "csv_file" in request.files:
            # Lese die hochgeladene csv-Datei ein
            csv_file = request.files["csv_file"]
            df = pd.read_csv(csv_file)

            display_table = df.values
        else:
            # Öffnen Sie die neue CSV-Datei im Schreibmodus
            with open('new_file.csv', 'w', newline='') as csvfile:
            # Erstellen Sie einen CSV-Schreiber
                writer = csv.writer(csvfile, delimiter=',')
                
                # head row 
                writer.writerow(["name", "text_1", "text_2", "image", "sound", "tags"])
                # Iterieren Sie über alle Einträge und schreiben Sie sie in die CSV-Datei
                for i in range(int(request.form['entry_count'])):
                    name = request.form['name_' + str(i)]
                    text_1 = request.form['text_1_' + str(i)]
                    text_2 = request.form['text_2_' + str(i)]
                    image = request.form['image_' + str(i)]
                    sound = request.form['sound_' + str(i)]
                    tags = request.form['tags_' + str(i)]
                

                    writer.writerow([name, text_1, text_2, image, sound, tags])
                    display_table.append([name, text_1, text_2, image, sound, tags])
                
   
    return render_template("dataset_editor.html", unique_tags=unique_tags, display_table=display_table)


