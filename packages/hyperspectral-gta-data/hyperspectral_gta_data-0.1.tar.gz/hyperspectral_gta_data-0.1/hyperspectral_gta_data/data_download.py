from zipfile import ZipFile 
import gdown
import os
        

class download:
    def __init__(self, data_name):
        # Dictionary to hold filenmae-id-data_type information
        self.image_dict = {
            'WashingtonDC': ['WashingtonDC_Ref_156bands', '13NGtcTWsViteI1J46IDXldlMPPOnTNLz', 'image'],
            'MicroscenePolymers': ['Microscene_Polymers', '1SjIToGJwkkWyBZER5Wv-1v1-I22Y-EBI', 'image']
        }
        
        # determine the file information
        fname, fid, file_type = self.image_dict[data_name]
        
        # Check if the spectral image or librRY directory exists, and create it if needed
        if file_type=='image':
            if not os.path.isdir('spectral_images'):
                os.mkdir('spectral_images')  
        if file_type=='library':
            if not os.path.isdir('spectral_libraries'):
                os.mkdir('spectral_libraries')  
        
        self.download_unzip(fname, fid);
        
            
    def download_unzip(self, fname, fid):
            
        if not os.path.isdir('spectral_images/'+fname):
            # Download the zip files of the image.
            fnameZip = 'spectral_images/'+fname+'.zip'
            if not os.path.isfile(fnameZip):
                gdown.download(id=fid, output=fnameZip)
            else:
                print(f'File {fnameZip} exists.')
            
            # Unzip the images
            with ZipFile(fnameZip, 'r') as zObject: 
                zipped_filenames = zObject.namelist()
                zObject.extractall( 
                    path='spectral_images/'+fname) 
            for zfname in zipped_filenames:
                print(f'File saved as: spectral_images/{fname}/{zfname}')
            
            # Delete the zip file
            os.remove(fnameZip)
    
    
    
    