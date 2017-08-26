import gspread, dropbox, json
from oauth2client.service_account import ServiceAccountCredentials

class Dropbox_sf:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.allfiles = []
        self.folder_metadata = {}
        with open('uqrtings_secret.json','r') as secret:
            data = json.load(secret)
            self.access_key = data['dropbox_secret']
        self.dbx = dropbox.Dropbox(self.access_key)

    def _get_folders(self, current_path):
        """ gets all direct children folders under current path
            metadata keys:
            -   property_groups
            -   shared_folder_id
            -   path_display
            -   sharing_info
            -   path_lower
            -   name
            -   parent_shared_folder_id
            -   id """
        
        for entry in self.dbx.files_list_folder(current_path).entries:
            if str(entry).startswith("Fo"):
                s = str(entry)
                metadata = {str(q.split('=')[0]).translate({32:None}):str(
                q.split('=')[1]) for q in s[s.find('(')+1:s.find(')')].split(
                ',')}
                print(metadata['name'])
                self.folder_metadata[metadata['path_display'].split(
                    '\'')[1]] = metadata

    def _get_files(self, current_path):
        """ gets all files under the current path """
        self.files = [x.name for x in self.dbx.files_list_folder(
        current_path).entries if str(x).startswith('File')]
        return self.files

    def get_entries(self, folder):
        print(folder)
        #adds folder name to the log file
        self.add_to_file('log.txt',folder)
        #refreshes the folder metadata
        self._get_folders(folder)
        current_set = self.folder_metadata
        self._get_files(folder)
        for x in self.files:
            self.allfiles.append(x)
            self.add_to_file('allfiles.txt', x)
        #performs this step for all folders in the current set
        print(current_set.keys())
        for folder, metadata in current_set.items():
            print(folder)
            self.get_entries(folder)

    def get_all_files(self):
        return self.allfiles

    def clear_all(self):
        self.allfiles = []
        with open('allfiles.txt','w') as allfiles:
            pass
        with open('log.txt','w') as allfiles:
            pass

    def add_to_file(self, tha_file, string):
        with open(tha_file,'a') as file_to_write:
            print(string)
            file_to_write.write(str(string))
            file_to_write.write('\n')

class Gsheet:
    def __init__(self, sheetname):
        self.sheetname = sheetname
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('uqrtings_secret.json', scope)
        self.client = gspread.authorize(credentials)
        self.sheet = self.client.open(self.sheetname).sheet1

    def _get_count(self):
        self.count = int(self.sheet.acell('I2').value)
        self.current_row = self.count + 1
        return self.count

    def append_row(self):
        self.sheet.update_cell(self._get_count()+2, 1, self.count+1)

    def batch_update(self, dropbox_sf_object):
        pass

jayden = Dropbox_sf('/Jayden Luu/')
jayden.get_entries('/Jayden Luu')
#jayden.clear_all()
#jayden.get_entries('/Jayden Luu/')
#jayden.get_all_files()
#idealsheet = Gsheet('IDEAL SPREADSHEET V1')
#idealsheet.append_row()
