from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle
import gspread, dropbox
from oauth2client.service_account import ServiceAccountCredentials
import datetime

access_key = '5AzdkqFSabAAAAAAAAAA2i2MkfJdwYMMxtfn3WJleulu7bTRDI5d__8ycX3LAsSi'
dbx = dropbox.Dropbox(access_key)
"""app_key = 'j4f97tu64yc04xi'
app_secret = 'qkp35yj67u9m3pw'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()

access_token, user_id = flow.finish(access_key)"""


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('uqrtings_secret.json', scope)
client = gspread.authorize(credentials)
sheet = client.open('UQR TINGS FILES').sheet1
files = sheet.get_all_records()

i  = 2



#print(files)

#for entry in files:

#    print(entry['COST']*entry['QUANTITY'])

#for entry in dbx.files_list_folder('/SHARED SPACE/UQR TINGS/Calculation Test').entries:

class shared_folder:
    def __init__(self, folder_name, access_key):
        self.folder_name = folder_name
        self.access_key = access_key
        self.dbx = dropbox.Dropbox(self.access_key)

    def list_folders(self):
        self.folders = [x.name for x in self.dbx.files_list_folder(self.folder_name).entries]
        return self.folders


def createPDF(canvas, files):

    logo = "UQRlogo.png"
    
    partNo = str(entry['Part Number'])
    creator = entry['Creators Name']

    while len(partNo) < 4:
        partNo = '0'+partNo
    
    canvas = canvas.Canvas("PartNo"+ partNo +".pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 12)
     
    canvas.drawString(30,750,'OFFICIAL PART')
    canvas.drawString(30,735,'OF UQ RACING')
    canvas.drawString(500,750, str(datetime.date.today()))
    canvas.line(480,747,580,747)
     
    canvas.drawString(275,725,'PART OF CAR:')
    canvas.drawString(500,725, 'EV42 2017' )
    canvas.line(378,723,580,723)
     
    canvas.drawString(30,703,'PART CREATED BY:')
    canvas.line(150,700,580,700)
    canvas.drawString(160,703, creator.upper() )

    canvas.drawImage(logo, 512, -15)
     
    canvas.save()

for entry in files:

    createPDF(canvas, entry)
