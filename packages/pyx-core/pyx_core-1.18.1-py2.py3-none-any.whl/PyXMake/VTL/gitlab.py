# -*- coding: utf-8 -*-
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %                                                         PyXMake - Build environment for PyXMake                                                                            %
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
Triple-use minimum working example for PyXMake. 
Technically, this script runs w/o PyXMake, but the default pipeline refers to the project..

@note: Execute a GitLab pipeline or a given pipeline job remotely w/o non-default packages.

@version:  1.0    
----------------------------------------------------------------------------------------------
@requires:
       - GitLab X-API-Token
       
@date:
       - 12.01.2021
   
@author: garb_ma                                      [DLR-FA,STM Braunschweig]
----------------------------------------------------------------------------------------------
"""
import time
import sys
import os
import getpass
import posixpath

def main(token=None, projectid=str(12702), **kwargs):
    """
    Main function to execute the script.
    """
    ## Add additional path to environment variable
    if os.path.exists(os.path.join(sys.prefix,"conda-meta")): os.environ["PATH"] = os.pathsep.join([os.path.join(sys.prefix,"Library","bin"),os.getenv("PATH","")])      
    # Now the requests module can be load w/o errors.
    import requests
    
    # Definition of CI job and the branch of the corresponding CI script 
    job = kwargs.get("job_name",None)
    data= {"ref": kwargs.get("branch", "master")}
    variables = kwargs.get("api_variables",{})
    
    # Definition of the header
    if not token: raise ValueError
    auth = {"PRIVATE-TOKEN": token}
    
    # Definition of the GitLab project ID (an integer number) and the API v4 URL 
    api_v4_url = posixpath.join(kwargs.get("base_url","https://gitlab.dlr.de/api/v4"),"projects",projectid)
    
    # Return all default values.
    if kwargs.get("datacheck",False): return [api_v4_url.split("projects")[0], auth]
    
    # Additional variables parsed to the CI job. Meaningful default values are only set for auto-installation of software on CARA.
    if job and job in ["stm_cara"]: 
        ## The default installation directory is the current user's home directory. This is only a meaningful 
        # default value if job refers to a CARA build requests
        cara_login_user = kwargs.get("cara_login_user",getpass.getuser())
        cara_login_credentials = kwargs.get("cara_login_credentials", getpass.getpass())
        install_directory = kwargs.get("cara_install_directory",posixpath.join("/home",cara_login_user,"software"))
        variables = kwargs.get("api_variables",
                            {"USER":cara_login_user,"CREDENTIALS":cara_login_credentials, "directory":install_directory,"feature":kwargs.get("package","all")})
    query = "&".join(["variables[][key]="+str(x)+"&variables[][value]="+str(y) for x, y in variables.items()])
    
    # Create a new dummy pipeline with the corresponding job. Terminate the pipeline immediately, since only one job is of interest.
    r = requests.post(api_v4_url+"/pipeline?"+query, data=data, headers=auth); 
    
    # Only meaningful if one job is requested in particular.
    if job: 
        ## If a specific job is given, create a new pipeline and run only this job. 
        # Remove the pipeline afterwards by default. Requires owner credentials.
        r = requests.post(api_v4_url+"/pipelines/%s/cancel" %  r.json()["id"], headers=auth)
        r = requests.get(api_v4_url+"/jobs", headers=auth)
        r = requests.post(api_v4_url+"/jobs/%s/play" % [x for x in r.json() if x["name"] in [job]][0]["id"], headers=auth)
        r = requests.get(api_v4_url+"/jobs", headers=auth)
        
        # Get the job ID of the running job
        JobID = [x for x in r.json() if x["name"] in [job]][0]["id"]
        while True:
            r = requests.get(api_v4_url+"/jobs/%s" % JobID, headers=auth)
            # Check status. Either return immediately or wait for job completion
            if r.json()["status"] in ["pending", "running"] and False: break
            if r.json()["status"] in ["success", "failure"]: 
                PipeID = requests.get(api_v4_url+"/jobs/%s" % r.json()["id"], headers=auth).json()["pipeline"]["id"]; 
                r = requests.get(api_v4_url+"/jobs/%s/trace" % r.json()["id"], headers=auth); 
                break
            time.sleep(2)
        ## Attempt to delete the pipeline. This is only successful when pipeline succeeded or failed.
        # Requires owner credentials.
        try: requests.delete(api_v4_url+"/pipelines/%s" % PipeID, headers=auth)
        except: pass
    
    # Obtain detailed information
    try: result = r.json()
    except: result = {"status_code":r.status_code,"content":r.text}
    
    # Return final result code and response
    return result
    
if __name__ == "__main__":
    main(); sys.exit()