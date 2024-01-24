from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
app = Flask(__name__)

# Cargar los datos de los invitados desde el archivo CSV
data = pd.read_csv("invitados_boda.csv")
df = pd.DataFrame(data)

# Configuración de las credenciales y acceso a la hoja de cálculo
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('my-project-boda-403921-4dfae347aeb3.json', scope)
client = gspread.authorize(creds)
# ID del archivo de Google Sheets
spreadsheet_id = '12nrk66AooZ6xUj2zd1WaOZvvmXSw5qMhcBu0scYCnpc'
# Acceder a la hoja de cálculo
sheet = client.open_by_key(spreadsheet_id).sheet1  # Cambia el nombre de la hoja si no se llama 'Sheet1'



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        codigo = int(request.form['codigo'])
        if codigo in df['codigo'].values:
            return redirect(url_for('seccion_dos', codigo=codigo))
        else:
            return "No existe el código."

    return render_template('index.html')

@app.route('/seccion_dos/<int:codigo>', methods=['GET', 'POST'])
def seccion_dos(codigo):
    row = df[df['codigo'] == codigo]
    nombre = row['invitados'].values[0]
    infantil_max = row['infantil'].values[0]
    adultos_max = row['adultos'].values[0]
    message = None

    if request.method == 'POST':
        infantil = int(request.form['infantil'])
        adultos = int(request.form['adultos'])
        nuevos_registros = [codigo, infantil, adultos]  # Modifica esta estructura si es necesario

        try:
            # Agregar los nuevos registros a la hoja de cálculo
            sheet.append_row(nuevos_registros)
            message = 'Asistencia registrada correctamente, ¡Te esperamos!'
        except Exception as e:
            message = 'Error al registrar la asistencia: ' + str(e)

    return render_template('seccion_dos.html', nombre=nombre, infantil_max=infantil_max, adultos_max=adultos_max, codigo=codigo, message=message)
if __name__ == '__main__':
    app.run()