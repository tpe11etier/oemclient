About this program.

Xpress API Client.  Short of needing this for work, it has zero value to anyone else that doesn't use the Varolii API.

Requirememnts.
Python 2.7
My forked version of Requests(Kenneth Reitz) - https://github.com/tpe11etier/requests
I made a change to the way the filepost is formatted because requests uses "file" for form encoded data as well as attachments.
In it's current form, there's no way to get the request properly formatted for the Xpress API to accept it.  Example of what I mean.

These are snips from posting an xml file with an attachment included.

--5d2b8568f940428b84b90fef1283c1d5
Content-Type: application/x-www-form-urlencoded; charset="ISO-8859-1"
Content-Disposition: form-data; name="PWF_MBML"

<Request version="EXAPI 2.0">
   <snipped>

--5d2b8568f940428b84b90fef1283c1d5
Content-Disposition: form-data; filename="attachment1.txt"; name="PWF_FILEPATH"
Content-Type:; name="attachment1.txt"

This is attachment 1


I had to override the encode_multipart_formdata to get it to format that way.  Probably a total hack job, but hey, it works!  :)


How to use:
 - First, you must install my version of requests I mention above.
 - The oemclient will read from the included properties file which has 4 attributes.
        - url (Any valid Varolii url will work)
        - file (specify an XML file you want to run.  The file *must* be places in the xmlfiles directory)
            *Note* - You may also specify None and it will run the embedded XML.
        - charset (I don't do any validation here, but not specifying one will work as well)
        - attachments - This is a comma separated list of file attachments.
 - Success messages as well as failures will be written to oemclient.log