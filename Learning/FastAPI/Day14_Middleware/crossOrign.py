'''
Cross-Origin Resource Sharing

if react app is working on http://localhost:3000 and 
if backend is working on http://localhost:8000 

We cannot share resource by default because they are working on different origins
so, to have a better communication between backend and frontend 
we use Cross-Origin Resource Sharing,

# ========= real world example ========
let's say frontend is running in your browser at 
http://localhost:8080
and javascript trying to communicate with backend at 
http://localhost
because the browser will assume the default port 80. 

Frontend browser will send an HTTP OPTIONS request to :80 backend

If backend sends the appropriate Headers authorizing the communication 

from different origin, then communication is established. 

to achieve this, 80 -backend must have a list of "allowed origins" 

The list would have to include allowed origin, 
http://localhost:8000
'''