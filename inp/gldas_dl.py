import numpy as np
import requests
import glob

f = open("subset_GLDAS_CLSM025_D_2.0_20220622_200818.txt", "r")

lis = [i.strip() for i in f]
lis = lis[1:]
lis = np.asarray(lis)

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


destination_files = 'gldas__clip/*.nc'
y = [eeks[16:-3] for eeks in glob.glob(destination_files)]
# print(y)
not_dled = []
dled = []
for x in lis:
    if str(x[148:156]) not in y:
        not_dled.append(x)
    if str(x[148:156:])  in y:
        dled.append(x)


# this while loop keeps attempting to download all of the files in your list of NLDAS files until all 
# of them have been downloaded. it also presents an http message number associated with your request 
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
while True:
    for idx,i in enumerate(not_dled):
        try:

            # submit the request using the session
            response = session.get(i, stream=True)
            print(response.status_code)
            # raise an exception in case of http errors
            response.raise_for_status()
            # save the file
            with open(f'gldas__clip/ksa_{i[148:156]}.nc', 'wb') as fd:
                for data in response:
                    fd.write(data)
            fd.close()
        except requests.exceptions.HTTPError as e:
            # handle any errors here
            print('error',e)
    
    y = [eeks[16:-3] for eeks in glob.glob(destination_files)]
    # print(y)
    not_dled = []
    dled = []
    for x in lis:
        if str(x[148:156]) not in y:
            not_dled.append(x)
        if str(x[148:156:])  in y:
            dled.append(x)
    print(f'dled: \t \n \t')
    for x in dled:
        print('\t',x,'\t')
    print(f'not dled: \t \n \t')
    for x in not_dled:
        print('\t',x,'\t')

            
    if len(not_dled) == 0:
        import sys
        sys.exit('no more left to download')