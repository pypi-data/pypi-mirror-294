# Oauth signin
This is just a simple oauth login package

1) first install the package using the command "pip install my-oauth-package==1.0.4" in the terminal
2) After installing import this library to your views.py to use it using "from my_oauth_package.test import OAuthManager" where my_oauth_package is the package file name, test is python file in that folder and OAuthManager is the class name
3) After importing the library code your creditials which are client_id, client_secret, base_url, redirect_uri and certificate
4) As my library has two functions so to access that you have to create two functions. In that, you have to create the instance of the class for using the functionality. And then, return that instance of class to the library function <br/>
ex of the function  <br/>
def oauth_login(request):
    manager = OAuthManager(client_id, client_secret, base_url, redirect_uri, certificate)
    print("oauth login")
    return manager.oauth_login(request)
<br/>
def callback(request):
    manager = OAuthManager(client_id, client_secret, base_url, redirect_uri, certificate)
    print("xecurify callback")
    return manager.xecurify_callback(request)

5) Create the route to access in urls.py by giving url, view function and name
<br/>
   ('oauth_login/', views.oauth_login, name='oauth_login')
   <br/>
   ('auth/callback/', views.callback, name='callback')
6) Run the terminal using "python manage.py runserver" and then go to the 'xecurify_callback' route for oauth