import numpy as np
import requests
import glob
import re

f = open("subset_GLDAS_NOAH025_3H_2.1_20220628_204611.txt", "r")

list_of_files_to_download = [i.strip() for i in f]
list_of_files_to_download = list_of_files_to_download[1:]
list_of_files_to_download = np.asarray(list_of_files_to_download)
# list_of_files_to_download[0]

class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    # Overrides from the library to keep headers when redirected to or from the NASA auth host.
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) and \
               redirect_parsed.hostname != self.AUTH_HOST and \
               original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return


# create session with the user credentials that will be used to authenticate access to the data

username="albertlarson" ###YOU THE READER OF FLUXTOFLOW NEED A NASA EARTHDATA ACCOUNT!!!
password="Andes27Hearts34!"
session = SessionWithHeaderRedirection(username, password)



# checks file folder to see if your destination folder for all these NLDAS files has any files in it, to
# prevent your code from downloading the same files multiple times.


destination_files = 'gldas__v21__clip/*.nc'

files_in_destination = []
for x in glob.glob(destination_files):
    numbers = list(set(re.findall('[0-9][0-9][0-9][0-9][0-9]+.[0-9][0-9][0-9][0-9]', x)))[0]
    files_in_destination.append(numbers)
print(f"length of destination folder array: {len(files_in_destination)}")
# import sys; sys.exit()

        
not_dled = []
dled = []


# lis is the text file containing links of all the files to be downloaded.
for x in list_of_files_to_download:
    numbers = list(set(re.findall('[0-9][0-9][0-9][0-9][0-9]+.[0-9][0-9][0-9][0-9]', x)))[0]
    if str(numbers) not in files_in_destination:
        not_dled.append(x)
    if str(numbers) in files_in_destination:
        dled.append(x)

# if len(not_dled) != 0:
#     while True:
#         print(not_dled[0])
#         quit=input('does this formatting looks good for links to download? (y/n) \t')
#         if quit not in ['y','n']:
#             print('try again:\n')
#         elif quit == 'n':
#             import sys
#             sys.exit()
#         else:
#             break
# else:
#     print('none left to download')
    
        
print(f"length of not downloaded array: {len(not_dled)}")
print(f"length of downloaded array: {len(dled)}")



# this while loop keeps attempting to download all of the files in your list of NLDAS files until all 
# of them have been downloaded. it also presents an http message number associated with your request 
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
while True:
    for idx,i in enumerate(not_dled):
        numbers = list(set(re.findall('[0-9][0-9][0-9][0-9][0-9]+.[0-9][0-9][0-9][0-9]', i)))[0]
        try:

            # submit the request using the session
            response = session.get(i, stream=True)
            print(response.status_code)
            # raise an exception in case of http errors
            response.raise_for_status()
            # save the file
            with open(f'gldas__v21__clip/ksa_{numbers}.nc', 'wb') as fd:
                for data in response:
                    fd.write(data)
            fd.close()
        except requests.exceptions.HTTPError as e:
            # handle any errors here
            print('error',e)
    
    files_in_destination = []
    for x in glob.glob(destination_files):
        numbers = list(set(re.findall('[0-9][0-9][0-9][0-9][0-9]+.[0-9][0-9][0-9][0-9]', x)))[0]
        files_in_destination.append(numbers)
    # print(y)
    not_dled = []
    dled = []
    for x in list_of_files_to_download:
        numbers = list(set(re.findall('[0-9][0-9][0-9][0-9][0-9]+.[0-9][0-9][0-9][0-9]', x)))[0]
        if str(numbers) not in files_in_destination:
            not_dled.append(x)
        if str(numbers) in files_in_destination:
            dled.append(x)
            
    print(f"length of downloaded items array after run:\t{len(dled)}")
    print(f"length of not yet downloaded items array after run: \t{len(not_dled)}")
    # print(f'dled: \t \n \t')
    # for x in dled:
    #     print('\t',x,'\t')
    # print(f'not dled: \t \n \t')
    # for x in not_dled:
    #     print('\t',x,'\t')

            
    if len(not_dled) == 0:
        import sys
        sys.exit('no more left to download')